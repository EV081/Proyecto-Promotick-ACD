from fastapi import APIRouter, UploadFile, File

from services.storage_service import save_file
from services.cleaning_service import process_csv

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

@router.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...)
):

    file_path = save_file(file)

    resultado = process_csv(file_path)

    return {
        "message": "Archivo procesado correctamente",
        "data": resultado
    }