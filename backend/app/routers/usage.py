from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import date

from ..database import get_db
from ..dependencies.api_key import validar_api_key

router = APIRouter(prefix="/usage", tags=["Usage"])


@router.get("/")
async def obtener_usage(
    api_key_data = Depends(validar_api_key)
):
    hoy = date.today()

    inicio = api_key_data["periodo_inicio"]
    fin = api_key_data["periodo_fin"]

    # Normalizar fechas
    if hasattr(inicio, "date"):
        inicio = inicio.date()
    if hasattr(fin, "date"):
        fin = fin.date()

    dias_restantes = max((fin - hoy).days, 0)
 
    return {
        "plan": api_key_data["plan"],
        "estado": api_key_data["estado"],
        "periodo_inicio": inicio,
        "periodo_fin": fin,
        "requests_max": api_key_data["requests_max"],
        "requests_usadas": api_key_data["requests_usadas"],
        "requests_restantes": max(api_key_data["requests_max"] - api_key_data["requests_usadas"], 0),
        "dias_restantes": dias_restantes
    }
