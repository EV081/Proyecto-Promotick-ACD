from lxml import etree
import pandas as pd
import numpy as np
import io
import csv

def _parse_xls_xml(content: bytes) -> pd.DataFrame:
    parser = etree.XMLParser(recover=True, huge_tree=True)
    root = etree.fromstring(content, parser=parser)

    ns = {'ss': 'urn:schemas-microsoft-com:office:spreadsheet'}
    data = []

    for row in root.findall('.//ss:Row', namespaces=ns):
        row_data = []
        for cell in row.findall('.//ss:Cell', namespaces=ns):
            data_elem = cell.find('ss:Data', namespaces=ns)
            row_data.append(data_elem.text if data_elem is not None else None)
        if any(row_data):
            data.append(row_data)

    if len(data) > 1:
        return pd.DataFrame(data[1:], columns=data[0])
    raise ValueError("El archivo XLS/XML no contiene datos válidos.")


def _parse_csv(content: bytes) -> pd.DataFrame:
    sample = content[:4096].decode('utf-8', errors='replace')
    dialect = csv.Sniffer().sniff(sample, delimiters=',;\t|')
    return pd.read_csv(io.BytesIO(content), sep=dialect.delimiter, encoding='utf-8', on_bad_lines='skip')


def _parse_xlsx(content: bytes) -> pd.DataFrame:
    return pd.read_excel(io.BytesIO(content), engine='openpyxl')


def load_raw_dataframe(content: bytes, filename: str) -> pd.DataFrame:
    lower_name = filename.lower()

    if lower_name.endswith('.csv'):
        return _parse_csv(content)

    if lower_name.endswith('.xlsx'):
        return _parse_xlsx(content)

    if lower_name.endswith('.xls'):
        # Intentamos primero como XML Spreadsheet 2003 (Freshdesk/Zendesk)
        try:
            return _parse_xls_xml(content)
        except Exception:
            # Si falla, intentamos como Excel binario clásico
            try:
                return pd.read_excel(io.BytesIO(content), engine='xlrd')
            except Exception:
                pass
        return _parse_csv(content)

    raise ValueError(f"Formato de archivo no soportado: {filename}. Use .xls, .xlsx o .csv")



# Transform + Load
def clean_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    df = df_raw.copy()
    pd.set_option('display.max_columns', None)

    # Estandarizamos nombres de columnas
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(' ', '_', regex=False)
        .str.replace('(', '', regex=False)
        .str.replace(')', '', regex=False)
    )

    df = df.replace(r'^\s*$', np.nan, regex=True)
    # Eliminamos columnas con atributos nulos
    df = df.dropna(axis=1, how='all')
    # Eliminamos columnas que consideramos basura
    columnas_basura = ['firma_del_cliente', 'resultados_de_la_encuesta']
    df = df.drop(columns=[c for c in columnas_basura if c in df.columns], errors='ignore')

    # Estandarizamos
    for campo in ('tipo', 'prioridad'):
        if campo in df.columns:
            df[campo] = df[campo].astype(str).str.strip().str.capitalize()

    # Normalizar prioridad: el origen exporta valores en inglés.
    if 'prioridad' in df.columns:
        df['prioridad'] = df['prioridad'].replace({
            'Low': 'Baja',
            'Medium': 'Media',
            'High': 'Alta',
            'Urgent': 'Urgente',
        })

    # Tiempos y Fechas
    cols_fechas_principales = [
        'tiempo_de_creación',
        'tiempo_de_resolución',
        'hora_de_cierre',
        'última_hora_de_la_actualización',
    ]
    for col in cols_fechas_principales:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Tiempo promedio de resolución
    if 'tiempo_de_resolución' in df.columns and 'tiempo_de_creación' in df.columns:
        df['lead_time_horas'] = (
            (df['tiempo_de_resolución'] - df['tiempo_de_creación'])
            .dt.total_seconds() / 3600
        ).round(4)

    # Ticket abierto (Backlog)
    if 'estado' in df.columns:
        df['esta_abierto'] = df['estado'].apply(
            lambda x: 1 if str(x).lower() not in ['cerrado', 'resuelto', 'closed', 'resolved'] else 0
        )
    else:
        df['esta_abierto'] = np.nan

    # Backlog Crítico: Alta o Urgente + Abierto
    if 'prioridad' in df.columns and 'esta_abierto' in df.columns:
        df['backlog_critico'] = np.where(
            (df['esta_abierto'] == 1) & (df['prioridad'].isin(['Alta', 'Urgente'])), 1, 0
        )

    # Cumplimiento de SLA
    if 'estado_de_resolución' in df.columns:
        df['incumple_sla'] = df['estado_de_resolución'].apply(
            lambda x: 1 if str(x).lower() in ['sla violated'] else 0
        )
        df['cumple_sla'] = 1 - df['incumple_sla']

    # Mes y día de la semana de creación
    if 'tiempo_de_creación' in df.columns:
        df['mes_creacion'] = df['tiempo_de_creación'].dt.to_period('M').astype(str)
        df['dia_semana_creacion'] = df['tiempo_de_creación'].dt.day_name()

    cols_a_eliminar = [
        'tiempo_de_seguimiento',
        'estado_de_la_aprobación',
        'jefe_de_ti_que_aprueba_la_solicitud',
        'producto',
        'id_de_contacto',
    ]
    df.drop(columns=[c for c in cols_a_eliminar if c in df.columns], inplace=True)

    cols_numericas = [
        'interacciones_de_agente',
        'interacciones_de_cliente',
        'tiempo_empleado',
        'lead_time_horas',
    ]
    for col in cols_numericas:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Fechas completas
    cols_fechas_completas = [
        'inicio_de_atencion',
        'fin_de_atencion',
        'tiempo_de_respuesta_inicial',
        'tiempo_de_creación',
        'tiempo_de_resolución',
        'hora_de_cierre',
        'última_hora_de_la_actualización',
        'vencidas_hasta_ahora',
    ]
    for col in cols_fechas_completas:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')

    # Duraciones
    cols_duracion = [
        'primer_tiempo_de_respuesta_en_horas',
        'tiempo_de_resolución_en_horas',
    ]
    for col in cols_duracion:
        if col in df.columns:
            df[col] = pd.to_timedelta(df[col], errors='coerce')

    # Binarias (SLA / backlog)
    cols_sla = ['esta_abierto', 'backlog_critico', 'incumple_sla', 'cumple_sla']
    for col in cols_sla:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce').astype('Int64')

    return df


def build_summary(df: pd.DataFrame) -> dict:
    summary = {
        "filas": int(df.shape[0]),
        "columnas": int(df.shape[1]),
        "columnas_lista": df.columns.tolist(),
        "nulos_por_columna": df.isnull().sum().to_dict(),
        "tipos_de_dato": {col: str(dtype) for col, dtype in df.dtypes.items()},
    }

    # Métricas de negocio si existen
    if 'backlog_critico' in df.columns:
        summary['total_backlog_critico'] = int(df['backlog_critico'].sum())
    if 'esta_abierto' in df.columns:
        summary['total_tickets_abiertos'] = int(df['esta_abierto'].sum())
    if 'cumple_sla' in df.columns:
        summary['total_cumple_sla'] = int(df['cumple_sla'].sum())
    if 'incumple_sla' in df.columns:
        summary['total_incumple_sla'] = int(df['incumple_sla'].sum())

    return summary
