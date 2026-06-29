from datetime import datetime
from typing import Any, Dict, Optional
from pydantic import BaseModel


class AvisoRequest(BaseModel):
    referencia: str
    monto: Optional[float] = None
    moneda: Optional[str] = "ARS"
    cliente_id: Optional[str] = None
    fecha: Optional[datetime] = None
    detalles: Optional[Dict[str, Any]] = None


