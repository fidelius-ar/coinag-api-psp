import os
import requests
from fastapi import APIRouter, HTTPException, Request
from auth import token_required
from session import client_banco
router = APIRouter()


@router.get("/PSP")
@token_required()
def consultar_cuenta_coelsa_psp(request: Request):
    creds = request.state.credentials

    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v1/PSP/{creds.get('idPSP')}/{creds.get('cuit')}",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=500, detail={"error": r.text})


@router.get("/cuenta-recaudadora")
@token_required()
def consultar_cuenta_recaudadora(request: Request):
    creds = request.state.credentials

    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v1/PSP/{creds.get("idPSP")}/CuentaRecaudadora/{creds.get("id_cuenta_recaudadora")}",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )

    if r.ok:
        return r.json()

    raise HTTPException(status_code=r.status_code, detail={"error": r.text})
