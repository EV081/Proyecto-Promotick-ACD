import pandas as pd
import numpy as np
import re
import unicodedata
from scipy.spatial.distance import mahalanobis
from scipy.stats import chi2

from lxml import etree

def extract_data(file_path):

    parser = etree.XMLParser(
        recover=True,
        huge_tree=True
    )

    tree = etree.parse(
        file_path,
        parser=parser
    )

    root = tree.getroot()

    ns = {
        'ss':
        'urn:schemas-microsoft-com:office:spreadsheet'
    }

    data = []

    for row in root.findall(
        './/ss:Row',
        namespaces=ns
    ):

        row_data = []

        for cell in row.findall(
            './/ss:Cell',
            namespaces=ns
        ):

            data_elem = cell.find(
                'ss:Data',
                namespaces=ns
            )

            row_data.append(
                data_elem.text
                if data_elem is not None
                else None
            )

        if any(row_data):
            data.append(row_data)

    if len(data) <= 1:
        raise Exception(
            "No se encontraron datos en el archivo"
        )

    df = pd.DataFrame(
        data[1:],
        columns=data[0]
    )

    return df

def clean_column_name(name):

    name = ''.join(
        c for c in unicodedata.normalize(
            'NFD',
            name
        )
        if unicodedata.category(c) != 'Mn'
    )

    name = name.lower().strip()

    name = re.sub(
        r'[\s\-/\\\(\)\.,\?]+',
        '_',
        name
    )

    name = re.sub(
        r'_+',
        '_',
        name
    )

    return name.strip('_')

def clean_level_1(df):

    df = df.copy()

    df.columns = [
        clean_column_name(col)
        for col in df.columns
    ]

    df = df.apply(
        lambda s:
        s.str.strip()
        if s.dtype == "object"
        else s
    )

    placeholders_nulos = [
        "None",
        "NaN",
        "nan",
        "",
        "null",
        "Null"
    ]

    df.replace(
        placeholders_nulos,
        np.nan,
        inplace=True
    )

    df.dropna(
        how='all',
        axis=1,
        inplace=True
    )

    columnas_descontinuadas = [

        "tiempo_de_seguimiento",

        "estado_de_la_aprobacion",

        "jefe_de_ti_que_aprueba_la_solicitud",

        "producto",

        "id_de_contacto"
    ]

    df.drop(
        columns=columnas_descontinuadas,
        errors="ignore",
        inplace=True
    )

    return df

def clean_level_2(df):

    df = df.copy()

    cols_fechas = [

        'tiempo_de_creacion',

        'vencidas_hasta_ahora',

        'hora_de_cierre',

        'ultima_hora_de_la_actualizacion',

        'inicio_de_atencion',

        'fin_de_atencion'
    ]

    for col in cols_fechas:

        if col in df.columns:

            df[col] = pd.to_datetime(
                df[col],
                errors='coerce'
            )

    if 'id_del_ticket' in df.columns:

        df['id_del_ticket'] = (
            df['id_del_ticket']
            .astype(str)
        )

    cols_enteros = [

        'interacciones_de_agente',

        'interacciones_de_cliente'
    ]

    for col in cols_enteros:

        if col in df.columns:

            df[col] = (
                pd.to_numeric(
                    df[col],
                    errors='coerce'
                )
                .astype('Int64')
            )

    cols_duracion_texto = [

        'primer_tiempo_de_respuesta_en_horas',

        'tiempo_de_resolucion_en_horas'
    ]

    for col in cols_duracion_texto:

        if col in df.columns:

            temp = pd.to_timedelta(
                df[col],
                errors='coerce'
            )

            df[col] = (
                temp.dt.total_seconds()
                / 3600.0
            )

    if 'tiempo_empleado' in df.columns:

        df['tiempo_empleado'] = (
            pd.to_numeric(
                df['tiempo_empleado'],
                errors='coerce'
            )
        )

    return df

def audit_quality(df):

    missing_summary = pd.DataFrame({
        'total_nulos': df.isna().sum(),
        'porcentaje':
        (df.isna().sum()/len(df))*100
    })

    missing_summary = missing_summary[
        missing_summary['total_nulos'] > 0
    ]

    estados_sin_cierre = {}

    if (
        'hora_de_cierre' in df.columns
        and
        'estado' in df.columns
    ):

        estados_sin_cierre = (
            df[
                df['hora_de_cierre'].isna()
            ]['estado']
            .value_counts()
            .to_dict()
        )

    nulos_simultaneos = 0

    cols_ti = [
        'origen',
        'origen_categoria'
    ]

    if all(
        col in df.columns
        for col in cols_ti
    ):

        nulos_simultaneos = (
            df[cols_ti]
            .isna()
            .all(axis=1)
            .sum()
        )

    report = {

        "missing_summary":
        missing_summary.to_dict(),

        "estados_sin_cierre":
        estados_sin_cierre,

        "nulos_simultaneos":
        int(nulos_simultaneos)
    }

    return df, report

def impute_missing_values(df):

    df = df.copy()

    cols_ti = [
        'origen',
        'origen_categoria'
    ]

    for col in cols_ti:

        if col in df.columns:

            df[col] = (
                df[col]
                .fillna('No aplica')
            )

    replacements = {

        'etiquetas':
        'Sin etiqueta',

        'resultados_de_la_encuesta':
        'Sin encuesta',

        'dependencias':
        'Ninguna',

        'tipo_de_solicitud':
        'No especificado',

        'tiempo_de_respuesta_inicial':
        'Sin respuesta',

        'estado_de_la_primera_respuesta':
        'Sin respuesta'
    }

    for col, value in replacements.items():

        if col in df.columns:

            df[col] = (
                df[col]
                .fillna(value)
            )

    cols_cat_menores = [

        'tipo_de_programa',

        'empresa',

        'tipo',

        'asunto'
    ]

    for col in cols_cat_menores:

        if col in df.columns:

            df[col] = (
                df[col]
                .fillna('No especificado')
            )

    if (
        'hora_de_cierre' in df.columns
        and
        'ultima_hora_de_la_actualizacion'
        in df.columns
    ):

        df['hora_de_cierre'] = (
            df['hora_de_cierre']
            .fillna(
                df[
                    'ultima_hora_de_la_actualizacion'
                ]
            )
        )

    if (
        'inicio_de_atencion'
        in df.columns
        and
        'tiempo_de_creacion'
        in df.columns
    ):

        df['inicio_de_atencion'] = (
            df['inicio_de_atencion']
            .fillna(
                df['tiempo_de_creacion']
            )
        )

    if (
        'fin_de_atencion'
        in df.columns
        and
        'hora_de_cierre'
        in df.columns
    ):

        df['fin_de_atencion'] = (
            df['fin_de_atencion']
            .fillna(
                df['hora_de_cierre']
            )
        )

    if (
        'prioridad' in df.columns
        and
        'tiempo_empleado' in df.columns
    ):

        mediana = (

            df.groupby('prioridad')
            ['tiempo_empleado']
            .transform('median')

        )

        df['tiempo_empleado'] = (
            df['tiempo_empleado']
            .fillna(mediana)
        )

    return df

def strict_casting(df):

    df = df.copy()

    df['tiempo_de_resolucion'] = (
        pd.to_datetime(
            df['tiempo_de_resolucion'],
            errors='coerce'
        )
    )

    df['tiempo_de_respuesta_inicial'] = (
        pd.to_datetime(
            df['tiempo_de_respuesta_inicial'],
            errors='coerce'
        )
    )

    df['tiempo_de_respuesta_inicial'] = (

        df['tiempo_de_respuesta_inicial']

        .fillna(
            df['tiempo_de_creacion']
        )
    )

    df['id_del_ticket'] = (
        df['id_del_ticket']
        .astype(str)
    )

    cols_categoricas = [

        'asunto',
        'estado',
        'prioridad',
        'fuente',
        'tipo',
        'agente',
        'grupo',
        'estado_de_resolucion',
        'estado_de_la_primera_respuesta',
        'etiquetas',
        'resultados_de_la_encuesta',
        'tipo_de_solicitud',
        'empresa',
        'tipo_de_programa',
        'origen',
        'origen_categoria',
        'dependencias',
        'nombre_completo'
    ]

    for col in cols_categoricas:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype('category')
            )

    cols_floats = [

        'primer_tiempo_de_respuesta_en_horas',

        'tiempo_de_resolucion_en_horas',

        'tiempo_empleado'
    ]

    for col in cols_floats:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype('float64')
            )

    cols_enteros = [

        'interacciones_de_agente',

        'interacciones_de_cliente'
    ]

    for col in cols_enteros:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype('Int64')
            )

    return df

def quality_control(df):

    report = {}

    report["duplicados_totales"] = int(
        df.duplicated().sum()
    )

    report["duplicados_id"] = int(
        df.duplicated(
            subset=['id_del_ticket']
        ).sum()
    )

    matriz = pd.crosstab(
        df['estado'],
        df['estado_de_resolucion'],
        margins=True
    )

    report["matriz_coherencia"] = (
        matriz.to_dict()
    )

    viajeros_del_tiempo = int(
        (
            df['hora_de_cierre']
            <
            df['tiempo_de_creacion']
        ).sum()
    )

    report["viajeros_del_tiempo"] = (
        viajeros_del_tiempo
    )

    return df, report

def fix_physical_errors(df):

    df = df.copy()

    negativos = int(
        (
            df['tiempo_empleado']
            < 0
        ).sum()
    )

    df.loc[
        df['tiempo_empleado'] < 0,
        'tiempo_empleado'
    ] = np.nan

    mediana = (

        df.groupby(
            'prioridad',
            observed=True
        )['tiempo_empleado']

        .transform('median')

    )

    df['tiempo_empleado'] = (

        df['tiempo_empleado']

        .fillna(mediana)

    )

    invertidos = int(
        (
            df['fin_de_atencion']
            <
            df['inicio_de_atencion']
        ).sum()
    )

    report = {

        "tiempos_negativos":
        negativos,

        "atenciones_invertidas":
        invertidos
    }

    return df, report

def identify_project_tickets(df):

    df = df.copy()

    patron = r'cambio|proyecto|implementaci'

    tipo_es_proyecto = (

        df['tipo']
        .astype(str)
        .str.lower()

        .str.normalize('NFD')

        .str.encode(
            'ascii',
            'ignore'
        )

        .str.decode('utf-8')

        .str.contains(
            patron,
            regex=True,
            na=False
        )

    )

    solicitud_es_proyecto = (

        df['tipo_de_solicitud']
        .astype(str)
        .str.lower()

        .str.normalize('NFD')

        .str.encode(
            'ascii',
            'ignore'
        )

        .str.decode('utf-8')

        .str.contains(
            patron,
            regex=True,
            na=False
        )

    )

    df['es_proyecto_largo'] = (

        tipo_es_proyecto

        |

        solicitud_es_proyecto

    )

    return df

def detect_univariate_outliers(df):

    df_no_proyectos = df[
        ~df['es_proyecto_largo']
    ].copy()

    vars_numericas = [

        'tiempo_empleado',

        'tiempo_de_resolucion_en_horas',

        'primer_tiempo_de_respuesta_en_horas',

        'interacciones_de_agente',

        'interacciones_de_cliente'
    ]

    report = {}

    for col in vars_numericas:

        serie = (
            df_no_proyectos[col]
            .astype(float)
        )

        q1 = serie.quantile(0.25)
        q3 = serie.quantile(0.75)

        iqr = q3 - q1

        upper = q3 + 1.5 * iqr
        lower = q1 - 1.5 * iqr

        cantidad = (
            (
                serie > upper
            ) |
            (
                serie < lower
            )
        ).sum()

        report[col] = {

            "outliers":
            int(cantidad),

            "porcentaje":
            round(
                cantidad /
                len(serie)
                * 100,
                2
            ),

            "lower":
            float(lower),

            "upper":
            float(upper)
        }

    return df, report

def detect_bivariate_outliers(df):

    df = df.copy()

    df_no_proyectos = df[
        ~df['es_proyecto_largo']
    ]

    sla_horas = {

        'Urgent': 4,

        'High': 8,

        'Medium': 24,

        'Low': 72
    }

    p99 = (

        df_no_proyectos

        .groupby(
            'prioridad',
            observed=True
        )

        ['tiempo_de_resolucion_en_horas']

        .quantile(0.99)

    )

    umbral_fila = (

        df['prioridad']

        .astype(str)

        .map(p99)

        .astype(float)

    )

    df['es_outlier_bivar'] = (

        (
            df[
                'tiempo_de_resolucion_en_horas'
            ]

            >

            umbral_fila
        )

        &

        (
            ~df['es_proyecto_largo']
        )

    )

    report = {

        "cantidad":
        int(
            df[
                'es_outlier_bivar'
            ].sum()
        ),

        "porcentaje":
        round(
            df[
                'es_outlier_bivar'
            ].mean() * 100,
            2
        ),

        "por_prioridad":

        df[
            df['es_outlier_bivar']
        ]

        .groupby(
            'prioridad',
            observed=True
        )

        .size()

        .to_dict()
    }

    return df, report

def detect_multivariate_outliers(df):

    df = df.copy()

    vars_numericas = [

        'tiempo_empleado',

        'tiempo_de_resolucion_en_horas',

        'primer_tiempo_de_respuesta_en_horas',

        'interacciones_de_agente',

        'interacciones_de_cliente'
    ]

    df_no_proyectos = df[
        ~df['es_proyecto_largo']
    ]

    Xs = (
        df_no_proyectos[
            vars_numericas
        ]
        .astype(float)
    )

    Xs = (

        Xs - Xs.min()

    ) / (

        Xs.max() - Xs.min()

    )

    cov = Xs.cov().values

    inv_cov = np.linalg.pinv(cov)

    media = Xs.mean().values

    distancias = []

    for i in range(Xs.shape[0]):

        distancias.append(

            mahalanobis(

                Xs.iloc[i, :],

                media,

                inv_cov

            ) ** 2

        )

    distancias = pd.Series(
        distancias,
        index=Xs.index
    )

    k = len(vars_numericas)

    umbral = chi2.ppf(
        0.997,
        df=k
    )

    df['dist_mahalanobis'] = np.nan

    df.loc[
        distancias.index,
        'dist_mahalanobis'
    ] = distancias.values

    df['es_outlier_multivar'] = (

        df[
            'dist_mahalanobis'
        ]

        >

        umbral

    ).fillna(False)

    report = {

        "cantidad":
        int(
            df[
                'es_outlier_multivar'
            ].sum()
        ),

        "porcentaje":
        round(
            df[
                'es_outlier_multivar'
            ].mean() * 100,
            2
        ),

        "umbral":
        float(umbral)
    }

    return df, report

def manage_outliers(df):

    df = df.copy()

    def clasificar(row):

        if row['es_proyecto_largo']:
            return 'proyecto_legitimo'

        if (
            row['es_outlier_bivar']
            and
            row['es_outlier_multivar']
        ):
            return 'outlier_ambos'

        if row['es_outlier_bivar']:
            return 'outlier_bivar'

        if row['es_outlier_multivar']:
            return 'outlier_multivar'

        return 'normal'

    df['tipo_outlier'] = (

        df.apply(
            clasificar,
            axis=1
        )

        .astype('category')
    )

    return df

def normalizar_clave(valor):

    if pd.isna(valor):
        return valor

    s = str(valor).strip().lower()

    s = ''.join(
        c
        for c in unicodedata.normalize(
            'NFD',
            s
        )
        if unicodedata.category(c) != 'Mn'
    )

    return s

def integrate_transform(df):

    df = df.copy()

    cols_categoricas = (

        df.select_dtypes(
            include='category'
        )

        .columns

        .tolist()
    )

    inconsistencias = {}

    for col in cols_categoricas:

        valores = (
            df[col]
            .dropna()
            .unique()
        )

        grupos = {}

        for v in valores:

            clave = normalizar_clave(v)

            grupos.setdefault(
                clave,
                []
            ).append(v)

        duplicados = {

            k:v

            for k,v

            in grupos.items()

            if len(v) > 1
        }

        if duplicados:

            inconsistencias[col] = (
                duplicados
            )

    return df, inconsistencias

def canonicalizar(serie):

    serie_str = serie.astype(str)

    claves = serie_str.map(
        normalizar_clave
    )

    aux = pd.DataFrame({

        'original':
        serie_str.values,

        'clave':
        claves.values

    })

    canonico = (

        aux.groupby('clave')

        ['original']

        .agg(
            lambda s:
            s.value_counts().idxmax()
        )

    )

    return claves.map(canonico)

def apply_canonicalization(
    df,
    inconsistencias
):

    df = df.copy()

    columnas = list(
        inconsistencias.keys()
    )

    for col in columnas:

        serie = canonicalizar(
            df[col]
        )

        if col == 'asunto':

            df[col] = (
                serie
                .astype('object')
            )

        else:

            df[col] = (
                serie
                .astype('category')
            )

    return df

def feature_engineering(df):

    df = df.copy().reset_index(drop=True)

    estados = [

        'Resolved',

        'Closed',

        'Open'
    ]

    df['estado'] = pd.Categorical(
        df['estado'],
        categories=estados
    )

    estado_dummies = pd.get_dummies(
        df['estado'],
        dtype=int
    )

    estado_dummies.columns = (
    estado_dummies.columns.astype(str)
    )

    print(type(estado_dummies))
    print(estado_dummies.head())
    print(estado_dummies.columns)
    print(df.index)
    print(estado_dummies.index)


    df = pd.concat(
    [
        df.drop(columns=['estado']),
        estado_dummies
    ],
    axis=1
    )

    sla_dummies = pd.get_dummies(
        df['estado_de_resolucion'],
    dtype=int
)

    sla_dummies.columns = (
        sla_dummies.columns.astype(str)
    )

    df = pd.concat(
    [
        df.drop(columns=['estado_de_resolucion']),
        sla_dummies
    ],
    axis=1
    )

    prioridad_dummies = pd.get_dummies(
    df['prioridad'],
    dtype=int
)

    prioridad_dummies.columns = (
        prioridad_dummies.columns.astype(str)
    )

    df = pd.concat(
    [
        df.drop(columns=['prioridad']),
        prioridad_dummies
    ],
    axis=1
    )

    df[
        'tiempo_creacion_anio_mes'
    ] = (

        df[
            'tiempo_de_creacion'
        ]

        .dt.to_period('M')

    )

    df[
        'tiempo_creacion_anio_semana'
    ] = (

        df[
            'tiempo_de_creacion'
        ]

        .dt.to_period('W')

    )

    df[
        'tiempo_creacion_fecha_dia'
    ] = (

        df[
            'tiempo_de_creacion'
        ]

        .dt.date

    )
    
    print(df.columns.tolist())
    df['critico'] = (

        (
            df['Urgent'] == 1
        )

        &

        (
            df['Open'] == 1
        )

    ).astype(int)

    return df

def process_csv(file_path):

    df = extract_data(file_path)

    df = clean_level_1(df)

    df = clean_level_2(df)

    df, audit_report = audit_quality(df)

    df = impute_missing_values(df)

    df = strict_casting(df)

    df, quality_report = quality_control(df)

    df, physical_report = fix_physical_errors(df)

    df = identify_project_tickets(df)

    df, _ = detect_univariate_outliers(df)

    df, _ = detect_bivariate_outliers(df)

    df, _ = detect_multivariate_outliers(df)

    df = manage_outliers(df)

    df, inconsistencias = (
        integrate_transform(df)
    )

    df = apply_canonicalization(
        df,
        inconsistencias
    )

    df = feature_engineering(df)

    df.to_csv(
        "processed/tickets_clean.csv",
        index=False
    )

    return {
        "rows": len(df)
    }
