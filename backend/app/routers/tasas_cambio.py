from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..database import get_db
from datetime import date
from backend.app.dependencies.api_key import validar_api_key


router = APIRouter(prefix="/tasas", tags=["Tasas de Cambio"])

#================================================
# Listar todos los registros 
#================================================
@router.get("/")
async def obtener_tasas(
    fecha: str | None = Query(None),
    from_moneda: str | None = Query(None),
    to_moneda: str | None = Query(None),
    api_key_data = Depends(validar_api_key),
    db: AsyncSession = Depends(get_db)
):
    sql = """
        SELECT fecha, tipo_tasa, from_moneda, to_moneda, factor
        FROM tasas_de_cambio
        WHERE 1=1
        AND id = 443
    """

    params = {}

    if fecha:
        sql += " AND fecha >= :fecha"
        params["fecha"] = date.fromisoformat(fecha)

    if from_moneda:
        sql += " AND from_moneda = :from_moneda"
        params["from_moneda"] = from_moneda

    if to_moneda:
        sql += " AND to_moneda = :to_moneda"
        params["to_moneda"] = to_moneda

    result = await db.execute(text(sql), params)
    return result.mappings().all()
