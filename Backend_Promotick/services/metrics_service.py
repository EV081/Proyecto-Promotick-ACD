import pandas as pd
import os

PROCESSED_FILE = "processed/tickets_clean.csv"

import os
import pandas as pd

def load_data():
    if not os.path.exists(PROCESSED_FILE):
        return None

    try:
        df = pd.read_csv(PROCESSED_FILE)

        if df is None or df.empty:
            return None

        return df

    except Exception:
        return None
    
def get_operational_metrics():

    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }
    
    print(df.columns.tolist())
    
    abiertos = int(df["Open"].sum())

    cerrados = int(df["Closed"].sum())

    resueltos = int(df["Resolved"].sum())
    
    backlog = abiertos - cerrados

    tiempo_atencion = round(
        df["tiempo_de_resolucion_en_horas"].mean(),
        2
    )

    primera_respuesta = round(
        df["primer_tiempo_de_respuesta_en_horas"].mean(),
        2
    )

    sla = round(
    df["Within SLA"].mean() * 100,
    2)

    return {

        "tickets_abiertos": int(abiertos),

        "tickets_cerrados": int(cerrados),

        "tickets_resueltos": int(resueltos),

        "backlog": int(backlog),

        "tiempo_promedio_atencion": tiempo_atencion,

        "tiempo_primera_respuesta": primera_respuesta,

        "cumplimiento_sla": sla
    }

def tickets_por_prioridad():

    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }

    return {
        "Low": int(df["Low"].sum()),
        "Medium": int(df["Medium"].sum()),
        "High": int(df["High"].sum()),
        "Urgent": int(df["Urgent"].sum())
    }

def tickets_por_categoria():

    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }
    
    return (
        df["tipo"]
        .value_counts()
        .head(10)
        .to_dict()
    )

def tickets_por_analista():

    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }

    return (
        df["agente"]
        .value_counts()
        .to_dict()
    )

def tendencia_tickets():

    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }

    df["tiempo_de_creacion"] = pd.to_datetime(
        df["tiempo_de_creacion"]
    )

    df["mes"] = (
        df["tiempo_de_creacion"]
        .dt.to_period("M")
        .astype(str)
    )

    tendencia = (
        df.groupby("mes")
        .size()
        .reset_index(name="tickets")
    )

    return tendencia.to_dict(
        orient="records"
    )

def comparativo_mensual():

    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }

    df["tiempo_de_creacion"] = pd.to_datetime(
        df["tiempo_de_creacion"]
    )

    df["mes"] = (
        df["tiempo_de_creacion"]
        .dt.to_period("M")
        .astype(str)
    )

    resumen = (

        df.groupby("mes")

        .agg(

            tickets=(
                "id_del_ticket",
                "count"
            ),

            tiempo_prom_resolucion=(
                "tiempo_de_resolucion_en_horas",
                "mean"
            )

        )

        .reset_index()

    )

    resumen[
        "variacion_tickets_pct"
    ] = (

        resumen["tickets"]

        .pct_change()

        * 100

    )

    return resumen.fillna(0).to_dict(
        orient="records"
    )

def backlog_critico():

    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }

    return {
        "backlog_critico": int(
            (
                (df["Urgent"] == 1)
                &
                (df["Open"] == 1)
            ).sum()
        )
    }

def demanda_por_area():

    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }

    datos = (
        df["grupo"]
        .value_counts()
        .to_dict()
    )

    return datos

def categorias_mayor_incidencia():

    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }

    datos = (
        df["tipo"]
        .value_counts()
        .head(10)
        .to_dict()
    )

    return datos

def nivel_saturacion_operativa():

    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }

    resultado = []

    for periodo, grupo in df.groupby(
        "tiempo_creacion_anio_mes"
    ):

        agentes = sorted(
            grupo["agente"]
            .dropna()
            .unique()
            .tolist()
        )

        resultado.append({

            "periodo": str(periodo),

            "tickets": int(
                len(grupo)
            ),

            "cantidad_agentes": len(
                agentes
            ),

            "agentes": agentes,

            "tickets_por_agente": round(
                len(grupo) / len(agentes),
                2
            ) if len(agentes) > 0 else 0

        })

    return resultado

def saturacion_operativa():
    
    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }

    df["tiempo_de_creacion"] = pd.to_datetime(
        df["tiempo_de_creacion"]
    )

    df["mes"] = (

        df["tiempo_de_creacion"]

        .dt.to_period("M")

        .astype(str)

    )

    demanda = (

        df.groupby("mes")

        .size()

    )

    analistas = (

        df.groupby("mes")["agente"]

        .nunique()

    )

    saturacion = (

        demanda / analistas

    )

    return (

        saturacion

        .reset_index(name="tickets_por_analista")

        .to_dict(orient="records")

    )

def incidentes_recurrentes():

    df = load_data()

    if df is None:
        return {
            "error": "No dataset loaded. Please upload a CSV first."
        }

    recurrentes = (

        df["asunto"]

        .value_counts()

    )

    recurrentes = (

        recurrentes[
            recurrentes > 1
        ]

        .head(10)

    )

    return recurrentes.to_dict()