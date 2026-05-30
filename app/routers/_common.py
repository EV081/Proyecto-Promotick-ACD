from typing import Tuple, List
from fastapi import HTTPException, status
import pandas as pd

from app.state import clean_store


def get_clean_df() -> pd.DataFrame:
    if not clean_store:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No hay datos limpios. Ejecute POST /clean/run primero.",
        )
    return clean_store[list(clean_store.keys())[-1]]


def require_columns(df: pd.DataFrame, columnas: List[str]) -> None:
    faltantes = [c for c in columnas if c not in df.columns]
    if faltantes:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Columnas requeridas no encontradas: {faltantes}",
        )


def parse_date_range(fecha_inicio: str, fecha_fin: str) -> Tuple[pd.Timestamp, pd.Timestamp]:
    try:
        inicio = pd.to_datetime(fecha_inicio).normalize()
        fin = pd.to_datetime(fecha_fin).normalize() + pd.Timedelta(days=1) - pd.Timedelta(seconds=1)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Fechas inválidas. Use el formato YYYY-MM-DD.",
        )
    if inicio > fin:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="fechaInicio debe ser menor o igual a fechaFin.",
        )
    return inicio, fin


def serie_semanal(serie_fechas: pd.Series, inicio: pd.Timestamp, fin: pd.Timestamp, value_key: str) -> list:
    inicio_d = inicio.normalize()
    fin_d = fin.normalize()
    serie = serie_fechas.dropna()
    serie = serie[(serie >= inicio) & (serie <= fin)]
    total_days = (fin_d - inicio_d).days + 1
    num_bins = (total_days + 6) // 7
    if num_bins == 0:
        return []
    bin_idx = ((serie - inicio_d).dt.days // 7).astype(int)
    counts = bin_idx.value_counts().reindex(range(num_bins), fill_value=0).sort_index()
    result = []
    for i, c in counts.items():
        ini_p = (inicio_d + pd.Timedelta(days=int(i) * 7)).date()
        fin_raw = inicio_d + pd.Timedelta(days=(int(i) + 1) * 7 - 1)
        fin_p = min(fin_raw, fin_d).date()
        result.append({"periodo": f"{ini_p} a {fin_p}", value_key: int(c)})
    return result


def serie_periodos(serie_fechas: pd.Series, inicio: pd.Timestamp, fin: pd.Timestamp, freq: str, value_key: str) -> list:
    full_range = pd.period_range(start=inicio.to_period(freq), end=fin.to_period(freq), freq=freq)
    serie = serie_fechas.dropna()
    serie = serie[(serie >= inicio) & (serie <= fin)]
    periodos = serie.dt.to_period(freq)
    counts = periodos.value_counts().reindex(full_range, fill_value=0).sort_index()
    return [{"periodo": str(p), value_key: int(c)} for p, c in counts.items()]


def trio_temporal(serie_fechas: pd.Series, inicio: pd.Timestamp, fin: pd.Timestamp, value_key: str) -> dict:
    return {
        "semanal": serie_semanal(serie_fechas, inicio, fin, value_key),
        "mensual": serie_periodos(serie_fechas, inicio, fin, "M", value_key),
        "trimestral": serie_periodos(serie_fechas, inicio, fin, "Q", value_key),
    }
