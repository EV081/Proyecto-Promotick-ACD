from datetime import datetime
from typing import Literal, Optional
from fastapi import APIRouter, HTTPException, Query, status
import pandas as pd

from app.routers._common import get_clean_df

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


@router.get(
    "/getInfoTickets",
    summary="Tickets abiertos, cerrados y backlog",
    status_code=status.HTTP_200_OK,
)
async def get_info_tickets():
    df = get_clean_df()
    if "esta_abierto" not in df.columns:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Columna 'esta_abierto' no encontrada. El archivo debe contener la columna 'estado'.",
        )
    abiertos = int(df["esta_abierto"].sum())
    cerrados = len(df) - abiertos
    return {
        "ticketsAbiertos": abiertos,
        "ticketsCerrados": cerrados,
        "backlogTickets": abiertos - cerrados,
    }


@router.get(
    "/getTiempoPromedio",
    summary="Tiempo promedio de atención en horas",
    status_code=status.HTTP_200_OK,
)
async def get_tiempo_promedio():
    df = get_clean_df()
    if "lead_time_horas" not in df.columns:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                "Columna 'lead_time_horas' no disponible. "
                "El archivo debe contener 'tiempo_de_creación' y 'tiempo_de_resolución'."
            ),
        )
    mean_val = df["lead_time_horas"].mean()
    return {"tiempoPromedio": None if pd.isna(mean_val) else round(float(mean_val), 4)}


@router.get(
    "/getTiempoPrimeraRespuesta",
    summary="Tiempo de primera respuesta en horas (promedio global o por ticket)",
    status_code=status.HTTP_200_OK,
)
async def get_tiempo_primera_respuesta(
    idTicket: Optional[str] = Query(default=None, description="ID del ticket. Si se omite, retorna el promedio global.")
):
    df = get_clean_df()
    col = "primer_tiempo_de_respuesta_en_horas"
    if col not in df.columns:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Columna '{col}' no encontrada en los datos limpios.",
        )

    if idTicket is not None:
        if "id_del_ticket" not in df.columns:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Columna 'id_del_ticket' no disponible.",
            )
        row = df[df["id_del_ticket"].astype(str) == str(idTicket)]
        if row.empty:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Ticket '{idTicket}' no encontrado.",
            )
        val = row.iloc[0][col]
        if pd.isna(val):
            return {"tiempoPrimeraRespuesta": None}
        return {"tiempoPrimeraRespuesta": round(val.total_seconds() / 3600, 4)}

    mean_td = df[col].mean()
    if pd.isna(mean_td):
        return {"tiempoPrimeraRespuesta": None}
    return {"tiempoPrimeraRespuesta": round(mean_td.total_seconds() / 3600, 4)}


@router.get(
    "/getCumplimientoSLA",
    summary="Tickets dentro y fuera del SLA",
    status_code=status.HTTP_200_OK,
)
async def get_cumplimiento_sla():
    df = get_clean_df()
    missing = [c for c in ("cumple_sla", "incumple_sla") if c not in df.columns]
    if missing:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Columnas SLA no disponibles: {missing}. "
                "El archivo debe contener 'estado_de_resolución'."
            ),
        )
    return {
        "withinSLA": int(df["cumple_sla"].sum()),
        "violatedSLA": int(df["incumple_sla"].sum()),
    }


@router.get(
    "/getTicketsBy",
    summary="Distribución de tickets por prioridad, categoría, reabiertos o analista",
    status_code=status.HTTP_200_OK,
)
async def get_tickets_by(
    by: Literal["prioridad", "categoria", "reabiertos", "analista"] = Query(
        ..., description="Criterio de agrupación."
    )
):
    df = get_clean_df()

    if by == "prioridad":
        if "prioridad" not in df.columns:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Columna 'prioridad' no encontrada.")
        result = df.groupby("prioridad").size()

    elif by == "categoria":
        if "tipo" not in df.columns:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Columna 'tipo' (categoría) no encontrada.")
        result = df.groupby("tipo").size()

    elif by == "reabiertos":
        if "estado" not in df.columns:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Columna 'estado' no encontrada.")
        mask = df["estado"].str.contains("reabiert", case=False, na=False)
        result = df[mask].groupby("estado").size()

    elif by == "analista":
        if "agente" not in df.columns:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=(
                    f"Columna 'agente' no encontrada. "
                    f"Columnas disponibles: {df.columns.tolist()}"
                ),
            )
        result = df.groupby("agente").size()

    return {"diccionario": {str(k): int(v) for k, v in result.items()}}


@router.get(
    "/getRangoFechas",
    summary="Fecha del primer y último ticket disponible",
    status_code=status.HTTP_200_OK,
)
async def get_rango_fechas():
    df = _get_clean_df()
    if "tiempo_de_creación" not in df.columns:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Columna 'tiempo_de_creación' no encontrada en los datos limpios.",
        )

    creacion = pd.to_datetime(df["tiempo_de_creación"], errors="coerce").dropna()
    if creacion.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay fechas de creación válidas en los datos limpios.",
        )

    return {
        "fechaInicio": creacion.min().date().isoformat(),
        "fechaFin": creacion.max().date().isoformat(),
        "totalTickets": int(creacion.shape[0]),
    }


def _empty_reporte(fecha_inicio_str: str, fecha_fin_str: str) -> dict:
    return {
        "periodo": {"fechaInicio": fecha_inicio_str, "fechaFin": fecha_fin_str},
        "ticketsCreados": 0,
        "ticketsAbiertos": 0,
        "ticketsCerrados": 0,
        "backlogTickets": 0,
        "promedioPrimeraRespuestaHoras": None,
        "promedioAtencionHoras": None,
        "cumplimientoSLA": {"porcentaje": None, "withinSLA": 0, "violatedSLA": 0},
        "ticketsPorPrioridad": {},
        "ticketsPorTipo": {},
        "ticketsPorAnalista": {},
        "sinDatos": True,
    }


@router.get(
    "/getReporteOperacional",
    summary="Reporte operacional consolidado para un periodo de fechas",
    status_code=status.HTTP_200_OK,
)
async def get_reporte_operacional(
    fecha_inicio: str = Query(..., description="Fecha de inicio del periodo en formato ISO YYYY-MM-DD."),
    fecha_fin: str = Query(..., description="Fecha de fin del periodo en formato ISO YYYY-MM-DD."),
):
    # 1. Validación del periodo
    try:
        inicio = datetime.strptime(fecha_inicio, "%Y-%m-%d")
        fin = datetime.strptime(fecha_fin, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Formato de fecha inválido. Use 'YYYY-MM-DD' (ej: 2026-05-30).",
        )

    if inicio > fin:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=(
                f"La fecha de inicio ({fecha_inicio}) no puede ser posterior "
                f"a la fecha de fin ({fecha_fin})."
            ),
        )

    # Incluir todo el día final
    fin_inclusivo = fin + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)

    # 2. Filtrado del dataframe
    df = _get_clean_df()
    if "tiempo_de_creación" not in df.columns:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Columna 'tiempo_de_creación' no encontrada en los datos limpios.",
        )

    df = df.copy()
    df["tiempo_de_creación"] = pd.to_datetime(df["tiempo_de_creación"], errors="coerce")
    df_f = df[
        (df["tiempo_de_creación"] >= inicio) & (df["tiempo_de_creación"] <= fin_inclusivo)
    ]

    if df_f.empty:
        return _empty_reporte(fecha_inicio, fecha_fin)

    # 3. Cálculo de métricas
    # Volumen y backlog
    abiertos = int((df_f["esta_abierto"] == 1).sum()) if "esta_abierto" in df_f.columns else 0
    cerrados = int((df_f["esta_abierto"] == 0).sum()) if "esta_abierto" in df_f.columns else 0
    backlog = abiertos - cerrados

    # Promedio de primera respuesta (timedelta -> horas)
    promedio_primera_resp = None
    col_resp = "primer_tiempo_de_respuesta_en_horas"
    if col_resp in df_f.columns:
        if pd.api.types.is_timedelta64_dtype(df_f[col_resp]):
            horas = df_f[col_resp].dt.total_seconds() / 3600
        else:
            horas = pd.to_numeric(df_f[col_resp], errors="coerce")
        horas_validas = horas[horas > 0]
        if not horas_validas.empty:
            promedio_primera_resp = round(float(horas_validas.mean()), 4)

    # Promedio de atención (registro -> cierre, en horas)
    promedio_atencion = None
    if "lead_time_horas" in df_f.columns:
        mean_atencion = pd.to_numeric(df_f["lead_time_horas"], errors="coerce").mean()
        if not pd.isna(mean_atencion):
            promedio_atencion = round(float(mean_atencion), 4)

    # Cumplimiento de SLA
    sla_pct = None
    within_sla = 0
    violated_sla = 0
    if "cumple_sla" in df_f.columns:
        total_sla = int(df_f["cumple_sla"].count())
        within_sla = int(df_f["cumple_sla"].sum())
        violated_sla = total_sla - within_sla
        if total_sla > 0:
            sla_pct = round(within_sla / total_sla * 100, 2)

    # Distribuciones
    por_prioridad = {}
    if "prioridad" in df_f.columns:
        por_prioridad = {str(k): int(v) for k, v in df_f["prioridad"].value_counts().items()}

    por_tipo = {}
    if "tipo" in df_f.columns:
        por_tipo = {str(k): int(v) for k, v in df_f["tipo"].value_counts().head(5).items()}

    por_analista = {}
    if "agente" in df_f.columns:
        df_ag = df_f.dropna(subset=["agente"])
        df_ag = df_ag[df_ag["agente"].astype(str).str.lower().str.strip() != "no agent"]
        por_analista = {str(k): int(v) for k, v in df_ag["agente"].value_counts().head(5).items()}

    return {
        "periodo": {"fechaInicio": fecha_inicio, "fechaFin": fecha_fin},
        "ticketsCreados": int(len(df_f)),
        "ticketsAbiertos": abiertos,
        "ticketsCerrados": cerrados,
        "backlogTickets": backlog,
        "promedioPrimeraRespuestaHoras": promedio_primera_resp,
        "promedioAtencionHoras": promedio_atencion,
        "cumplimientoSLA": {
            "porcentaje": sla_pct,
            "withinSLA": within_sla,
            "violatedSLA": violated_sla,
        },
        "ticketsPorPrioridad": por_prioridad,
        "ticketsPorTipo": por_tipo,
        "ticketsPorAnalista": por_analista,
        "sinDatos": False,
    }
