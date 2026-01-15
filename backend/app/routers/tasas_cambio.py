from fastapi import APIRouter, Depends, Query
import httpx


router = APIRouter(tags=["Tasas de Cambio"])

@router.get("/tasas/usd")
async def obtener_tasas_usd():
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "https://api.frankfurter.app/latest?base=USD"
        )
    return response.json()
