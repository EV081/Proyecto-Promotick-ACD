from fastapi import APIRouter, File, UploadFile, HTTPException, status
from fastapi.responses import JSONResponse

from app.core.cleaner import load_raw_dataframe
from app.state import uploaded_store

router = APIRouter(prefix="/upload", tags=["Upload"])

ALLOWED_EXTENSIONS = {".xls", ".xlsx", ".csv"}
MAX_FILE_SIZE_MB = 50


@router.post(
    "/file",
    summary="Subir archivo XLS / XLSX / CSV",
    response_description="Confirmación con metadatos básicos del archivo cargado",
    status_code=status.HTTP_200_OK,
)
async def upload_file(file: UploadFile = File(..., description="Archivo .xls, .xlsx o .csv a subir")):
    filename: str = file.filename or ""
    ext = "." + filename.rsplit(".", 1)[-1].lower() if "." in filename else ""
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Formato '{ext}' no soportado. Use: {', '.join(ALLOWED_EXTENSIONS)}",
        )

    content = await file.read()

    size_mb = len(content) / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"El archivo excede el límite de {MAX_FILE_SIZE_MB} MB (recibido: {size_mb:.2f} MB).",
        )

    try:
        df_raw = load_raw_dataframe(content, filename)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"No se pudo leer el archivo: {exc}",
        )

    # Guardar en el store global
    uploaded_store[filename] = {"content": content, "df_raw": df_raw}

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Archivo cargado exitosamente.",
            "filename": filename,
            "size_mb": round(size_mb, 3),
            "filas_detectadas": int(df_raw.shape[0]),
            "columnas_detectadas": int(df_raw.shape[1]),
            "columnas": df_raw.columns.tolist(),
            "archivos_disponibles": list(uploaded_store.keys()),
        },
    )


@router.get(
    "/files",
    summary="Listar archivos cargados",
    response_description="Lista de archivos disponibles en memoria",
    status_code=status.HTTP_200_OK,
)
async def list_uploaded_files():
    """Retorna los nombres de todos los archivos actualmente cargados en memoria."""
    files_info = []
    for fname, store in uploaded_store.items():
        df = store.get("df_raw")
        files_info.append({
            "filename": fname,
            "filas": int(df.shape[0]) if df is not None else None,
            "columnas": int(df.shape[1]) if df is not None else None,
        })
    return {"archivos": files_info, "total": len(files_info)}
