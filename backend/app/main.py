from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.routers import tasas
from backend.app.routers import tasas_cambio

app = FastAPI(
    title="API Tasas de Cambio USA",
    description="API para consultar tasas de cambio basadas en USD",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # luego restringes
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasas.router, prefix="/api")
app.include_router(tasas_cambio.router, prefix="/api")

@app.get("/")
def health():
    return {"status": "ok"}