from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.upload import router as upload_router
from routes.metrics import router as metrics_router
from routes.auth import router as auth_router
from routes.additional import router as additional_router
from services.storage_service import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

init_db()

app.include_router(upload_router)
app.include_router(metrics_router)
app.include_router(auth_router)
app.include_router(additional_router)