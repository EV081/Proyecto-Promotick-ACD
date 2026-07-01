# Backend Promotick

Backend desarrollado con **FastAPI** para la gestión, procesamiento y análisis de tickets operativos.

El proyecto permite cargar archivos CSV de tickets, realizar un proceso de limpieza y transformación de datos, almacenar la información procesada y exponer diferentes endpoints para obtener métricas operativas y gerenciales.

---

# Tecnologías utilizadas

- Python 3.13
- FastAPI
- Uvicorn
- Pandas
- NumPy
- SciPy
- SQLite
- Docker

---

# Estructura del proyecto
```text

Backend_Promotick/
│
├── models/
│   └── user.py
│
├── routes/
│   ├── auth.py
│   ├── upload.py
│   └── metrics.py
│
├── services/
│   ├── storage_service.py
│   ├── cleaning_service.py
│   └── metrics_service.py
│
├── uploads/
│   └── Archivos CSV originales cargados
│
├── processed/
│   └── Archivos CSV procesados y limpios
│
├── app.db
│   └── Base de datos SQLite
│
├── Dockerfile
│
├── docker-compose.yml
│
├── requirements.txt
│
└── main.py
```
---

# Ejecución con Docker

## Requisitos

Tener instalado:

- Docker Desktop

---

## Construcción del contenedor

Desde la raíz del proyecto:

```bash
docker compose build
```

Levantar el backend

```bash
docker compose up
```

También puede ejecutarse en segundo plano:

```bash
docker compose up -d
```

Para detener el servicio:

```bash
docker compose down
```

El backend estará disponible en:
```bash
http://localhost:8000
```

La documentación automática de FastAPI:
```bash
http://localhost:8000/docs
```

## Carga de información
Antes de utilizar los endpoints de métricas es necesario cargar un archivo CSV mediante el endpoint de subida.

El archivo cargado se almacena inicialmente en:
```bash
uploads/
```

Después pasa por el servicio de limpieza:
```bash
services/cleaning_service.py
```
donde se realizan transformaciones, limpieza de datos y preparación del dataset.

El resultado final se guarda en:
```bash
processed/
```
Este archivo procesado es el que utilizan los endpoints de métricas.

## Base de datos

El proyecto utiliza SQLite:
```bash
app.db
```
Actualmente almacena información de usuarios para autenticación.

Docker mantiene la persistencia mediante un volumen:
```bash
volumes:
  - ./app.db:/app/app.db
```
Esto permite que los datos sobrevivan aunque el contenedor se reinicie.
