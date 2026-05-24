# Promotick Data API

Backend desarrollado en FastAPI para la gestión y limpieza de datos de tickets exportados.

---

## Flujo de datos

```
POST /upload/file  -->  uploaded_store (raw)
                              |
                              v
POST /clean/run  -->  clean_dataframe()  -->  clean_store (limpio)
                              |
                              v
GET  /clean/download  -->  CSV limpio (tickets_promotick_clean.csv)
```

El `clean_store` queda en memoria como fuente de datos lista para ser consumida por endpoints futuros de análisis y visualizacion.

---

## Estructura del proyecto

```
backend-promotick/
├── main.py                  # Punto de entrada de la aplicacion
├── requirements.txt         # Dependencias
├── .gitignore
├── app/
│   ├── state.py             # Estado compartido en memoria
│   ├── core/
│   │   └── cleaner.py       # Pipeline ETL completo
│   └── routers/
│       ├── upload.py        # Endpoint de carga de archivos
│       └── clean.py         # Endpoint de limpieza y exportacion
└── acd_data_proyecto_limpieza.py  # Notebook original de referencia
```

---

## Requisitos

- Python 3.10 o superior

---

## Instalacion y ejecucion

**1. Crear el entorno virtual e instalar dependencias:**

```bash
python3 -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows

pip install -r requirements.txt
```

**2. Levantar el servidor:**

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

**3. Acceder a la documentacion interactiva (Swagger UI):**

```
http://localhost:8000/docs
```

---

## Endpoints

### Upload

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | `/upload/file` | Sube un archivo `.xls`, `.xlsx` o `.csv` (max 50 MB). El archivo queda en memoria listo para ser procesado. |
| GET | `/upload/files` | Lista los archivos cargados actualmente en memoria. |

**Ejemplo de uso — subir archivo:**

```bash
curl -X POST http://localhost:8000/upload/file \
  -F "file=@9000678639_tickets-April-24-2026-21_21.xls"
```

---

### Clean

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| POST | `/clean/run` | Ejecuta el pipeline completo de limpieza sobre el archivo cargado. Devuelve un resumen estadistico y la URL de descarga. |
| GET | `/clean/download` | Descarga el CSV limpio generado (`tickets_promotick_clean.csv`). |
| GET | `/clean/status` | Muestra que archivos ya fueron procesados y estan disponibles. |

**Ejemplo de uso — ejecutar limpieza:**

```bash
curl -X POST "http://localhost:8000/clean/run"
```

**Ejemplo de uso — descargar CSV limpio:**

```bash
curl -O http://localhost:8000/clean/download
```

---

### Utilidad

| Metodo | Ruta | Descripcion |
|--------|------|-------------|
| GET | `/` | Estado general de la API y lista de endpoints. |
| GET | `/health` | Health check. |

---

## Pipeline de limpieza

El endpoint `POST /clean/run` aplica el siguiente pipeline, basado en el notebook:

1. **Limpieza estructural** — estandariza nombres de columnas, elimina columnas vacias y campos sin valor analitico.
2. **Conversion de fechas** — transforma campos de texto a `datetime` y calcula `lead_time_horas` (tiempo creacion a resolucion).
3. **KPIs derivados** — genera variables como `backlog_critico`, `cumple_sla`, `incumple_sla`, `mes_creacion`, `dia_semana_creacion`.
4. **Eliminacion de variables descontinuadas** — remueve campos que Promotick indico como no relevantes.
5. **Tipado de datos** — asigna tipos correctos (numerico, fecha, timedelta, binario).
6. **Exportacion** — el DataFrame limpio queda disponible para descarga y para consumo interno por otros endpoints.

---

## Formatos soportados

| Formato | Descripcion |
|---------|-------------|
| `.xls` | XML Spreadsheet 2003 (exportaciones Freshdesk / Zendesk) y Excel binario clasico |
| `.xlsx` | Excel moderno |
| `.csv` | CSV con separador autodetectado (coma, punto y coma, tabulacion, pipe) |