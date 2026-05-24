from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import upload, clean

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
        },
    }


@app.get("/health", tags=["Root"])
async def health():
    return {"status": "ok"}
