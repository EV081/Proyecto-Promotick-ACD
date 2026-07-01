import pandas as pd
import os
import numpy as np

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
        return {"error": "No dataset loaded. Please upload a CSV first."}

    df["tiempo_de_creacion"] = pd.to_datetime(df["tiempo_de_creacion"])
    df["mes"] = df["tiempo_de_creacion"].dt.to_period("M").astype(str)

    tendencia = (
        df.groupby("mes")
        .size()
        .reset_index(name="tickets")
        .sort_values("mes")
    )

    registros = tendencia.to_dict(orient="records")
    for r in registros:
        r["name"] = str(r["mes"])  
        r["mes"] = str(r["mes"]) 
        r["tickets"] = int(r["tickets"])

    return registros

def comparativo_mensual(): 
    df = load_data()
    if df is None:
        return {"error": "No dataset loaded. Please upload a CSV first."}

    df["tiempo_de_creacion"] = pd.to_datetime(df["tiempo_de_creacion"])
    df["mes"] = df["tiempo_de_creacion"].dt.to_period("M").astype(str)

    columna_sla = None
    for col in df.columns:
        if col.lower() in ["within_sla", "withinsla", "cumple_sla", "cumple sla", "within sla"]:
            columna_sla = col
            break

    if columna_sla:
        if df[columna_sla].dtype == object:
            df["sla_numerico"] = df[columna_sla].astype(str).str.lower().isin(["1", "true", "si", "sí", "s"]).astype(int)
        else:
            df["sla_numerico"] = df[columna_sla].astype(int)
    else:
        df["sla_numerico"] = 1 

    resumen = (
        df.groupby("mes")
        .agg(
            tickets=("id_del_ticket", "count"),
            tiempo_prom_resolucion=("tiempo_de_resolucion_en_horas", "mean"),
            pct_sla=("sla_numerico", "mean") 
        )
        .reset_index()
        .sort_values("mes") 
    )

    resumen["variacion_tickets_pct"] = resumen["tickets"].pct_change() * 100
    resumen["pct_sla"] = resumen["pct_sla"] * 100

    resumen = resumen.replace([float('inf'), float('-inf')], 0).fillna(0)

    resumen["tiempo_prom_resolucion"] = resumen["tiempo_prom_resolucion"].round(1)
    resumen["pct_sla"] = resumen["pct_sla"].round(1)
    resumen["variacion_tickets_pct"] = resumen["variacion_tickets_pct"].round(1)

    resumen = resumen.rename(columns={"mes": "name"})

    registros_limpios = resumen.to_dict(orient="records")
    for r in registros_limpios:
        r["name"] = str(r["name"])
        r["mes"] = str(r["name"]) 
        r["tickets"] = int(r["tickets"])
        r["tiempo_prom_resolucion"] = float(r["tiempo_prom_resolucion"])
        r["pct_sla"] = float(r["pct_sla"])
        r["variacion_tickets_pct"] = float(r["variacion_tickets_pct"])

    return registros_limpios

def backlog_critico():
    df = load_data()
    if df is None:
        return {"error": "No dataset loaded. Please upload a CSV first."}

    return {
        "backlog_critico": int(
            ((df["Urgent"] == 1) & (df["Open"] == 1)).sum()
        )
    }

def demanda_por_area():
    df = load_data()
    if df is None:
        return {"error": "No dataset loaded. Please upload a CSV first."}

    df["grupo"] = df["grupo"].fillna("No Especificado").replace("", "No Especificado")
    counts = df["grupo"].value_counts()
    
    datos_formateados = [
        {"name": str(index), "value": int(val)} 
        for index, val in counts.items()
    ]
    return datos_formateados

def categorias_mayor_incidencia():
    df = load_data()
    if df is None:
        return {"error": "No dataset loaded. Please upload a CSV first."}

    counts = df["tipo"].value_counts().head(5)
    
    datos_formateados = [
        {"name": str(index), "value": int(val)} 
        for index, val in counts.items()
    ]
    return datos_formateados

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
