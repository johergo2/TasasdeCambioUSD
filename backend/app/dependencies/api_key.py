from fastapi import Header, HTTPException, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from datetime import date

from ..database import get_db

# Aquí se tiene toda la lógica de seguridad - valida API_KEY
async def validar_api_key(
    request: Request,
    x_api_key: str = Header(None, alias="X-API-Key"),
    db: AsyncSession = Depends(get_db)
):
    # 1. Validar que venga el header
    if not x_api_key:
        raise HTTPException(
            status_code=401,
            detail="Debe enviar el header X-API-Key"
        )

    # 2. Buscar la API Key en base de datos
    sql = text("""
        SELECT
            api_key,
            estado,
            requests_max,
            requests_usadas,
            periodo_inicio,
            periodo_fin
        FROM tasas_api_keys
        WHERE api_key = :api_key
    """)

    result = await db.execute(sql, {"api_key": x_api_key})
    key = result.mappings().first()

    # 3. API Key no existe
    if not key:
        raise HTTPException(
            status_code=401,
            detail="API Key inválida"
        )

    # 4. API Key inactiva
    if key["estado"] != "ACT":
        raise HTTPException(
            status_code=403,
            detail="API Key inactiva o suspendida"
        )

    # 5. Validar vigencia
    hoy = date.today()

    if hoy < key["periodo_inicio"] or hoy > key["periodo_fin"]:
        raise HTTPException(
            status_code=403,
            detail="API Key fuera del periodo de vigencia"
        )

    # 6. Validar límite de consumo
    if key["requests_usadas"] >= key["requests_max"]:
        raise HTTPException(
            status_code=429,
            detail="Límite de consumo alcanzado"
        )

    # Incrementar consumo
    update_sql = """
        UPDATE tasas_api_keys
        SET requests_usadas = requests_usadas + 1
        WHERE api_key = :api_key
    """

    await db.execute(text(update_sql), {"api_key": x_api_key})
    await db.commit()        
    
    return key
