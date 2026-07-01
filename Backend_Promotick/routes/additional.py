from fastapi import APIRouter, HTTPException
from pathlib import Path
import pandas as pd

router = APIRouter(
    prefix="/additional",
    tags=["Additional"]
)


@router.get("/dataset-status")
async def dataset_status():

    processed_folder = Path("processed")

    if not processed_folder.exists():
        return {
            "dataset_loaded": False
        }

    csv_files = list(processed_folder.glob("*.csv"))

    if len(csv_files) == 0:
        return {
            "dataset_loaded": False
        }

    latest_file = max(
        csv_files,
        key=lambda file: file.stat().st_mtime
    )

    try:
        df = pd.read_csv(latest_file)

        return {
            "dataset_loaded": True,
            "filename": latest_file.name,
            "rows": len(df),
            "columns": len(df.columns)
        }

    except Exception:
        return {
            "dataset_loaded": True,
            "filename": latest_file.name
        }


@router.get("/processed-dataset")
async def get_processed_dataset():

    processed_folder = Path("processed")

    if not processed_folder.exists():
        raise HTTPException(
            status_code=404,
            detail="No existe la carpeta processed"
        )

    csv_files = list(processed_folder.glob("*.csv"))

    if len(csv_files) == 0:
        raise HTTPException(
            status_code=404,
            detail="No existe dataset procesado"
        )

    latest_file = max(
        csv_files,
        key=lambda file: file.stat().st_mtime
    )

    try:
        df = pd.read_csv(latest_file)

        return {
            "filename": latest_file.name,
            "rows": len(df),
            "columns": list(df.columns),
            "data": df.to_dict(orient="records")
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error leyendo dataset: {str(e)}"
        )