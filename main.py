from datetime import datetime
from fastapi import FastAPI, Request
from schemas import AvisoResponse
from auth import token_required
import os
import requests

app = FastAPI(
    title="Coinag Avisos API",
    description="API para avisos de crédito, reversa, débitos y adhesiones",
    version="1.0.0",
)

# requests.get(f"{os.getenv('URL')}/coelsapsp/v1/PSP/{idPsp}/{cuit}").json()
@app.get("/PSP", response_model=AvisoResponse)
@token_required()
def aviso_credito_cvu(request: Request):

    return {
        "status": "ok",
        "endpoint": "/PSP",
        "recibido": {
            "referencia": "",
            "monto": None,
            "moneda": "ARS",
            "cliente_id": None,
            "fecha": datetime.utcnow(),
            "detalles": {},
        },
        "procesado_en": datetime.utcnow(),
    }


