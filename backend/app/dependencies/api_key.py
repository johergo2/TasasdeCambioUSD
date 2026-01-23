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
    
    client_ip = request.client.host if request.client else "0.0.0.0"
    endpoint = str(request.url.path)

    # 1. Validar que venga el header
    if not x_api_key:
        await registrar_log(
            db=db,
            api_key="SIN_API_KEY",
            endpoint=endpoint,
            ip=client_ip,
            status_code=401            
        )
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
        await registrar_log(
            db=db,
            api_key=x_api_key,
            endpoint=endpoint,
            ip=client_ip,
            status_code=401            
        )        
        raise HTTPException(
            status_code=401,
            detail="API Key inválida"
        )

    # 4. API Key inactiva
    if key["estado"] != "ACT":
        await registrar_log(
            db=db,
            api_key=x_api_key,
            endpoint=endpoint,
            ip=client_ip,
            status_code=403
        )        
        raise HTTPException(
            status_code=403,
            detail="API Key inactiva o suspendida"
        )

    # 5. Validar vigencia
    hoy = date.today()

    inicio = key["periodo_inicio"]
    fin = key["periodo_fin"]

    # Convertir si vienen como datetime
    if hasattr(inicio, "date"):
       inicio = inicio.date()

    if hasattr(fin, "date"):
       fin = fin.date()

    if hoy < inicio or hoy > fin:
        await registrar_log(
            db=db,
            api_key=x_api_key,
            endpoint=endpoint,
            ip=client_ip,
            status_code=403
        )        
        raise HTTPException(
            status_code=403,
            detail="API Key fuera del periodo de vigencia"
        )

    # Incrementar consumo
    update_sql = """
        UPDATE tasas_api_keys
        SET requests_usadas = requests_usadas + 1
        WHERE api_key = :api_key
        AND requests_usadas < requests_max
    """
    try:
        result_update = await db.execute(text(update_sql), {"api_key": x_api_key})
        await db.commit()    

        if result_update.rowcount == 0:
            await registrar_log(
                db=db,
                api_key=x_api_key,
                endpoint=endpoint,
                ip=client_ip,
                status_code=429
            )    
            await db.rollback()
            raise HTTPException(
                status_code=429,
                detail="Límite de consumo alcanzado"
            )      

        await db.commit()                  

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Error actualizando consumo de la API Key en la tabla"
        )
    
    if result_update.rowcount == 0:
        await registrar_log(
            db=db,
            api_key=x_api_key,
            endpoint=endpoint,
            ip=client_ip,
            status_code=429
        )
        await db.rollback()
        raise HTTPException(
            status_code=429,
            detail="Límite de consumo alcanzado"
        )

    await registrar_log(
        db=db,
        api_key=x_api_key,
        endpoint=endpoint,
        ip=client_ip,
        status_code=200
    )


    return key

async def registrar_log(
    db: AsyncSession,
    api_key: str,
    endpoint: str,
    ip: str,
    status_code: int
):
    try:
        sql = text("""
            INSERT INTO tasas_api_logs
                (api_key, endpoint, ip, status_code)
            VALUES
                (:api_key, :endpoint, :ip, :status_code)
        """)

        await db.execute(sql, {
            "api_key": api_key,
            "endpoint": endpoint,
            "ip": ip,
            "status_code": status_code
        })

        await db.commit()

    except Exception:
        await db.rollback()
        # ⚠️ Nunca rompemos la API por un error de logging
        pass
