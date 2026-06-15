from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import upload, clean, dashboard, gerencial

app = FastAPI(
    title="Promotick Data API",
    description=(
        "Backend para la gestión y limpieza de datos de tickets Promotick. "
        "Soporta la carga de archivos XLS/XLSX/CSV y aplica el pipeline completo"
    ),
    version="1.0.0",
    contact={
        "name": "Equipo ACD - UTEC",
    },
    license_info={
        "name": "MIT",
    },
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(upload.router)
app.include_router(clean.router)
app.include_router(dashboard.router)
app.include_router(gerencial.router)


@app.get("/", tags=["Root"])
async def root():
    return {
        "message": "Promotick Data API corriendo",
        "docs": "/docs",
        "endpoints": {
            "upload_file": "POST /upload/file",
            "list_files": "GET /upload/files",
            "run_cleaning": "POST /clean/run",
            "download_clean": "GET /clean/download",
            "clean_status": "GET /clean/status",
            "dashboard_info_tickets": "GET /dashboard/getInfoTickets",
            "dashboard_tiempo_promedio": "GET /dashboard/getTiempoPromedio",
            "dashboard_primera_respuesta": "GET /dashboard/getTiempoPrimeraRespuesta",
            "dashboard_sla": "GET /dashboard/getCumplimientoSLA",
            "dashboard_tickets_by": "GET /dashboard/getTicketsBy",
            "dashboard_rango_fechas": "GET /dashboard/getRangoFechas",
            "dashboard_reporte_operacional": "GET /dashboard/getReporteOperacional",
            "gerencial_tendencia_tickets": "GET /dashboard/gerencial/tendenciaTickets",
            "gerencial_backlog_critico": "GET /dashboard/gerencial/backlogCritico",
            "gerencial_incidentes_recurrentes": "GET /dashboard/gerencial/incidentesRecurrentes",
            "gerencial_categorias_mayor_incidencia": "GET /dashboard/gerencial/categoriasMayorIncidencia",
            "gerencial_saturacion_operativa": "GET /dashboard/gerencial/saturacionOperativa",
            "gerencial_demanda_por_area": "GET /dashboard/gerencial/demandaPorArea",
            "gerencial_comparativo_mensual_atencion": "GET /dashboard/gerencial/comparativoMensualAtencion",
            "gerencial_mejora_continua": "GET /dashboard/gerencial/mejoraContinua",
        },
    }


@app.get("/health", tags=["Root"])
async def health():
    return {"status": "ok"}
