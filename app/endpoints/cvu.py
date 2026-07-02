import os
import requests
from fastapi import APIRouter, HTTPException, Request
from auth import token_required
from app.schemas import AltaCVU, ModificacionCvu
from session import client_banco
router = APIRouter()


@router.put("/cvu/{cvu}")
@token_required()
def modificacion_cvu(cvu: str, payload: ModificacionCvu, request: Request):
    creds = request.state.credentials
    body_data = payload.model_dump()
    body_data["idCuenta"] = creds.get("id_cuenta_recaudadora")
    r = client_banco.put(
        f"{os.getenv('URL')}/coelsapsp/v1/PSP/{creds.get('idPSP')}/CuentaRecaudadora/{creds.get('id_cuenta_recaudadora')}/CVU/{cvu}",
        json=body_data,
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json() if r.text else {"message": "CVU modificado correctamente"}
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.post("/cvu/alta")
@token_required()
def alta_cvu(payload: AltaCVU, request: Request):
    creds = request.state.credentials
    r = client_banco.post(
        f"{os.getenv('URL')}/coelsapsp/v1/PSP/{creds.get('idPSP')}/CuentaRecaudadora/{creds.get('id_cuenta_recaudadora')}/AltaCVU",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
        json=payload.model_dump(),
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=500, detail={"error": r.text})


@router.delete("/cvu/{cvu}")
@token_required()
def baja_cvu(cvu: str, request: Request):
    creds = request.state.credentials
    r = client_banco.delete(
        f"{os.getenv('URL')}/coelsapsp/v1/PSP/{creds.get("idPSP")}/CuentaRecaudadora/{creds.get("id_cuenta_recaudadora")}/CVU/{cvu}",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json() if r.text else {"message": "CVU eliminado correctamente"}

    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.get("/cvu/{cvu}")
@token_required()
def consultar_cvu(cvu: str, request: Request):
    creds = request.state.credentials
    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v1/Consulta/CVU/{cvu}",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.get("/cvu/cuit/{cuit}")
@token_required()
def consultar_cvu_por_cuit(cuit: str, request: Request):
    creds = request.state.credentials
    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v1/PSP/{creds.get("idPSP")}/CuentaRecaudadora/{creds.get("id_cuenta_recaudadora")}/CUIT/{cuit}",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.get("/cbu/{cbu}")
@token_required()
def consultar_cbu(cbu: str, request: Request):
    creds = request.state.credentials
    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v1/Consulta/CBU/{cbu}",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )

    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})
