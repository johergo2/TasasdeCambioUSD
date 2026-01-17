from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from ..database import get_db

router = APIRouter(prefix="/tasas", tags=["Tasas de Cambio"])

#================================================
# Listar todos los registros 
#================================================
@router.get("/")
async def obtener_tasas(
    fecha: str | None = Query(None),
    from_moneda: str | None = Query(None),
    to_moneda: str | None = Query(None),
    db: AsyncSession = Depends(get_db)
):
    sql = """
        SELECT fecha, tipo_tasa, from_moneda, to_moneda, factor
        FROM tasas_de_cambio
        WHERE 1=1
    """

    params = {}

    if fecha:
        sql += " AND fecha = :fecha::date"
        params["fecha"] = fecha

    if from_moneda:
        sql += " AND from_moneda = :from_moneda"
        params["from_moneda"] = from_moneda

    if to_moneda:
        sql += " AND to_moneda = :to_moneda"
        params["to_moneda"] = to_moneda

    result = await db.execute(text(sql), params)
    return result.mappings().all()
