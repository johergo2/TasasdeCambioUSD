#!/usr/bin/env bash

# Activar entorno virtual (Render ya crea uno automáticamente)
# uvicorn ejecuta la app desde la carpeta app
uvicorn app.main:app --host 0.0.0.0 --port $PORT
