from fastapi import APIRouter

from services.metrics_service import *

router = APIRouter(
    prefix="/metrics",
    tags=["Metrics"]
)

@router.get("/operational")
def operational():

    return get_operational_metrics()

@router.get("/priorities")
def priorities():

    return tickets_por_prioridad()

@router.get("/categories")
def categories():

    return tickets_por_categoria()

@router.get("/analysts")
def analysts():

    return tickets_por_analista()

@router.get("/trend")
def trend():

    return tendencia_tickets()

@router.get("/monthly-comparison")
def monthly():

    return comparativo_mensual()

@router.get("/critical-backlog")
def critical():

    return backlog_critico()

@router.get("/demand-by-area")
def demand_by_area():

    return demanda_por_area()


@router.get("/top-categories")
def top_categories():

    return categorias_mayor_incidencia()


@router.get("/operational-saturation")
def operational_saturation():

    return nivel_saturacion_operativa()

@router.get("/saturation")
def saturation():

    return saturacion_operativa()

@router.get("/recurrent-incidents")
def recurrent():

    return incidentes_recurrentes()

