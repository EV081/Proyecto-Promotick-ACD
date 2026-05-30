from fastapi import APIRouter, Query, status

from app.routers._common import (
    get_clean_df,
    parse_date_range,
    require_columns,
    trio_temporal,
)

router = APIRouter(prefix="/dashboard/gerencial", tags=["Dashboard Gerencial"])


@router.get(
    "/tendenciaTickets",
    summary="Evolución del volumen de tickets por período (semanal, mensual, trimestral)",
    status_code=status.HTTP_200_OK,
)
async def tendencia_tickets(
    fechaInicio: str = Query(..., description="Fecha de inicio (YYYY-MM-DD)."),
    fechaFin: str = Query(..., description="Fecha de fin (YYYY-MM-DD)."),
):
    df = get_clean_df()
    require_columns(df, ["tiempo_de_creación"])
    inicio, fin = parse_date_range(fechaInicio, fechaFin)
    series = trio_temporal(df["tiempo_de_creación"], inicio, fin, "tickets")
    return {
        "rango": {"inicio": inicio.date().isoformat(), "fin": fin.date().isoformat()},
        **series,
    }


@router.get(
    "/backlogCritico",
    summary="Recuento de tickets de alta prioridad pendientes",
    status_code=status.HTTP_200_OK,
)
async def backlog_critico():
    df = get_clean_df()
    require_columns(df, ["backlog_critico"])
    return {"backlogCritico": int(df["backlog_critico"].fillna(0).sum())}


@router.get(
    "/incidentesRecurrentes",
    summary="Categorías de origen que más se repiten",
    status_code=status.HTTP_200_OK,
)
async def incidentes_recurrentes(
    limit: int = Query(default=10, ge=1, le=100, description="Top-N categorías a devolver."),
):
    df = get_clean_df()
    require_columns(df, ["origen_categoria"])
    counts = df["origen_categoria"].dropna().value_counts().head(limit)
    return {
        "recurrentes": [
            {"categoria": str(k), "ocurrencias": int(v)} for k, v in counts.items()
        ]
    }


@router.get(
    "/categoriasMayorIncidencia",
    summary="Categoría (tipo) con mayor incidencia y ranking completo",
    status_code=status.HTTP_200_OK,
)
async def categorias_mayor_incidencia():
    df = get_clean_df()
    require_columns(df, ["tipo"])
    counts = df["tipo"].dropna().value_counts()
    if counts.empty:
        return {"top": None, "ranking": []}
    ranking = [{"categoria": str(k), "ocurrencias": int(v)} for k, v in counts.items()]
    return {"top": ranking[0], "ranking": ranking}


@router.get(
    "/saturacionOperativa",
    summary="Relación entre demanda y capacidad (totales / atendidos)",
    status_code=status.HTTP_200_OK,
)
async def saturacion_operativa():
    df = get_clean_df()
    require_columns(df, ["esta_abierto"])
    totales = int(len(df))
    atendidos = int((df["esta_abierto"] == 0).sum())
    saturacion = round(totales / atendidos, 4) if atendidos > 0 else None
    return {
        "totales": totales,
        "atendidos": atendidos,
        "saturacion": saturacion,
    }


@router.get(
    "/demandaPorArea",
    summary="Áreas de negocio con mayor volumen de solicitudes",
    status_code=status.HTTP_200_OK,
)
async def demanda_por_area():
    df = get_clean_df()
    require_columns(df, ["grupo"])
    grupos = (
        df["grupo"]
        .fillna("Sin clasificar")
        .replace({"No Group": "Sin clasificar"})
    )
    counts = grupos.value_counts()
    return {
        "demanda": [
            {"area": str(k), "tickets": int(v)} for k, v in counts.items()
        ]
    }


@router.get(
    "/comparativoMensualAtencion",
    summary="Tickets atendidos por período (semanal, mensual, trimestral)",
    status_code=status.HTTP_200_OK,
)
async def comparativo_mensual_atencion(
    fechaInicio: str = Query(..., description="Fecha de inicio (YYYY-MM-DD)."),
    fechaFin: str = Query(..., description="Fecha de fin (YYYY-MM-DD)."),
):
    df = get_clean_df()
    require_columns(df, ["tiempo_de_creación", "tiempo_de_resolución"])
    inicio, fin = parse_date_range(fechaInicio, fechaFin)
    mask = (
        df["tiempo_de_creación"].between(inicio, fin)
        & df["tiempo_de_resolución"].between(inicio, fin)
    )
    atendidos = df.loc[mask, "tiempo_de_resolución"]
    series = trio_temporal(atendidos, inicio, fin, "ticketsAtendidos")
    return {
        "rango": {"inicio": inicio.date().isoformat(), "fin": fin.date().isoformat()},
        "totalAtendidos": int(mask.sum()),
        **series,
    }


@router.get(
    "/mejoraContinua",
    summary="Indicadores de prevención y optimización del servicio",
    status_code=status.HTTP_200_OK,
)
async def mejora_continua():
    df = get_clean_df()
    total = int(len(df))
    indicadores: dict = {}

    if "estado" in df.columns and total > 0:
        reabiertos = int(df["estado"].astype(str).str.contains("reabiert", case=False, na=False).sum())
        indicadores["tasaReaperturaPct"] = round(reabiertos * 100 / total, 2)
        indicadores["ticketsReabiertos"] = reabiertos

    if "cumple_sla" in df.columns:
        sla_vals = df["cumple_sla"].dropna()
        if len(sla_vals) > 0:
            indicadores["cumplimientoSlaPct"] = round(float(sla_vals.mean()) * 100, 2)

    if "lead_time_horas" in df.columns:
        lt = df["lead_time_horas"].dropna()
        if len(lt) > 0:
            indicadores["leadTimeMedianoHoras"] = round(float(lt.median()), 4)
            indicadores["leadTimePromedioHoras"] = round(float(lt.mean()), 4)
            indicadores["resueltosMenos24hPct"] = round(float((lt < 24).mean()) * 100, 2)
            indicadores["resueltosMenos72hPct"] = round(float((lt < 72).mean()) * 100, 2)

    return {"totalTickets": total, "indicadores": indicadores}
