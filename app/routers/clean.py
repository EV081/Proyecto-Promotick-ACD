import io
from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import StreamingResponse, JSONResponse
from app.core.cleaner import clean_dataframe, build_summary
from app.state import uploaded_store, clean_store

router = APIRouter(prefix="/clean", tags=["Clean"])


def _get_latest_filename() -> str:
    if not uploaded_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay archivos cargados. Usar POST /upload/file primero.",
        )
    return list(uploaded_store.keys())[-1]


@router.post(
    "/run",
    summary="Ejecutar pipeline de limpieza completo",
    response_description="Resumen del proceso de limpieza + URL de descarga del CSV",
    status_code=status.HTTP_200_OK,
)
async def run_cleaning(
    filename: str = Query(
        default=None,
        description="Nombre del archivo a limpiar (debe haber sido subido vía /upload/file). Si se omite, se usa el último archivo subido.",
    )
):
    target = filename or _get_latest_filename()

    if target not in uploaded_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Archivo '{target}' no encontrado. Archivos disponibles: {list(uploaded_store.keys())}",
        )

    df_raw = uploaded_store[target]["df_raw"]

    # Ejecutar limpieza
    try:
        df_clean = clean_dataframe(df_raw)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error durante la limpieza de datos: {exc}",
        )

    clean_store[target] = df_clean

    summary = build_summary(df_clean)
    nulos = {k: (None if str(v) == 'nan' else int(v)) for k, v in summary["nulos_por_columna"].items()}

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Limpieza completada exitosamente",
            "archivo_origen": target,
            "output_filename": "tickets_promotick_clean.csv",
            "download_url": f"/clean/download?filename={target}",
            "resumen": {
                "filas": summary["filas"],
                "columnas": summary["columnas"],
                "columnas_lista": summary["columnas_lista"],
                "tipos_de_dato": summary["tipos_de_dato"],
                "nulos_por_columna": nulos,
                "metricas_negocio": {
                    k: summary[k]
                    for k in [
                        "total_backlog_critico",
                        "total_tickets_abiertos",
                        "total_cumple_sla",
                        "total_incumple_sla",
                    ]
                    if k in summary
                },
            },
        },
    )


@router.get(
    "/download",
    summary="Descargar CSV limpio",
    response_description="Archivo CSV limpio",
    status_code=status.HTTP_200_OK,
)
async def download_clean_csv(
    filename: str = Query(
        default=None,
        description="Nombre del archivo original subido. Si se omite, usa el último procesado.",
    )
):
    target = filename or (list(clean_store.keys())[-1] if clean_store else None)

    if not target or target not in clean_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay datos limpios disponibles. Ejecute POST /clean/run primero.",
        )

    df_clean = clean_store[target]
    df_export = df_clean.copy()
    for col in df_export.select_dtypes(include=['timedelta64[ns]']).columns:
        df_export[col] = df_export[col].astype(str)

    for col in df_export.columns:
        if hasattr(df_export[col], 'dt') and hasattr(df_export[col].dt, 'to_period'):
            pass
        if str(df_export[col].dtype).startswith('period'):
            df_export[col] = df_export[col].astype(str)

    buffer = io.StringIO()
    df_export.to_csv(buffer, index=False, encoding='utf-8')
    buffer.seek(0)

    return StreamingResponse(
        io.BytesIO(buffer.getvalue().encode('utf-8')),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=tickets_promotick_clean.csv"},
    )


@router.get(
    "/status",
    summary="Estado de archivos limpios disponibles",
    status_code=status.HTTP_200_OK,
)
async def clean_status():
    results = []
    for fname, df in clean_store.items():
        results.append({
            "filename": fname,
            "filas_limpias": int(df.shape[0]),
            "columnas_limpias": int(df.shape[1]),
            "columnas": df.columns.tolist(),
        })
    return {"archivos_limpios": results, "total": len(results)}
