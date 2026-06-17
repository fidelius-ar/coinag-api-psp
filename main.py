from datetime import datetime
from fastapi import FastAPI, Request
from schemas import AvisoResponse
from coinag import token_required, get_current_credentials
import os
import requests

app = FastAPI(
    title="Coinag Avisos API",
    description="API para avisos de crédito, reversa, débitos y adhesiones",
    version="1.0.0",
)


@app.GET("/PSP", response_model=AvisoResponse)
@token_required()
def aviso_credito_cvu(request: Request):
    creds = get_current_credentials()
    if not creds:
        raise RuntimeError("No hay credenciales en el contexto del token")
    idPsp = creds.get("idPsp")
    cuit = creds.get("cuit")
    return requests.get(f"{os.getenv('URL')}/coelsapsp/v1/PSP/{idPsp}/{cuit}").json()


