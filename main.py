from datetime import datetime
from fastapi import FastAPI, Request, HTTPException
from auth import token_required
import os
import requests


app = FastAPI(
    title="Coinag Avisos API",
    description="API para avisos de crédito, reversa, débitos y adhesiones",
    version="1.0.0",
)



@app.get("/PSP")
@token_required()
def aviso_credito_cvu(request: Request):
    creds = request.state.credentials
    print(request.state.credentials)

    r = requests.get(
        f"{os.getenv('URL')}/coelsapsp/v1/PSP/{creds.get("idPSP")}/{creds.get("cuit")}",
        headers={"Authorization": f"Bearer {creds.get("token_coinag")}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=500, detail={"error": r.text})
