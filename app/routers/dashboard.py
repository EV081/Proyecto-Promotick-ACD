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
