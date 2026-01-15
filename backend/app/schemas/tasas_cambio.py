from pydantic import BaseModel
from datetime import date

class TasaCambioOut(BaseModel):
    fecha: date
    tipo_tasa: str
    from_moneda: str
    to_moneda: str
    factor: float
