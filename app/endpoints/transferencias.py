import os
import requests
from fastapi import APIRouter, HTTPException, Request, Query
from auth import token_required
from app.schemas import TransferenciaRequest, FiltrosConciliacion,FiltrosConciliacionTransferencias
from session import client_banco
router = APIRouter()


@router.post("/transferencia/ARS")
@token_required()
def transferencia(payload: TransferenciaRequest, request: Request):
    creds = request.state.credentials
    r = client_banco.post(
        f"{os.getenv('URL')}/coelsapsp/v2/Transferencia",
        json=payload.model_dump(),
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.post("/transferencia/USD")
@token_required()
def transferenciaUSD(payload: TransferenciaRequest, request: Request):
    creds = request.state.credentials
    r = client_banco.post(
        f"{os.getenv('URL')}/coelsapsp/v2/TransferenciaUSD",
        json=payload.model_dump(),
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.post("/transferencia/interna/ARS")
@token_required()
def transferenciaInterna(payload: TransferenciaRequest, request: Request):
    creds = request.state.credentials
    r = client_banco.post(
        f"{os.getenv('URL')}/coelsapsp/v2/TransferenciaCoinag",
        json=payload.model_dump(),
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.post("/transferencia/interna/USD")
@token_required()
def transferenciaInternaUSD(payload: TransferenciaRequest, request: Request):
    creds = request.state.credentials
    r = client_banco.post(
        f"{os.getenv('URL')}/coelsapsp/v2/TransferenciaCoinagUSD",
        json=payload.model_dump(),
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.get("/transferencia/{idTrxOri}")
@token_required()
def consultar_transferencia(idTrxOri: str, request: Request):
    creds = request.state.credentials

    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v1/Transferencia/{idTrxOri}",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.get("/transferencia/v2/{idTrxOri}")
@token_required()
def consultar_transferenciaV2(idTrxOri: str, request: Request):
    creds = request.state.credentials

    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v2/Transferencia/{idTrxOri}",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.get("/transferencia-id/{idTrxCliente}")
@token_required()
def consultar_transferenciaIDinterno(idTrxCliente: str, request: Request):
    creds = request.state.credentials

    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v1/TransferenciaByIdTrxCliente/{idTrxCliente}",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.get("/conciliacion/transferenciaBanco")
@token_required()
def listar_transferencias_banco(
    request: Request,
    filtros: FiltrosConciliacion = Query(),
):
    creds = request.state.credentials
    query_params = filtros.model_dump(exclude_none=True)

    r = client_banco.get(
        url=f"{os.getenv('URL')}/coelsapsp/v1/Conciliacion/ListaTransferenciaBanco/{creds.get("idPSP")}",
        params=query_params,
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )

    if r.ok:
        return r.json()

    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.get("/Conciliacion/ConciliacionTransferenciasDeBanco")
@token_required()
def obtener_conciliacion_transferencias(
    request: Request,
    filtros: FiltrosConciliacionTransferencias = Query() # FastAPI parsea automáticamente los Query Params
):
    creds = request.state.credentials
    id_psp = creds.get("idPSP")
    query_params = filtros.model_dump(exclude_none=True)
    
    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v1/Conciliacion/ConciliacionTransferenciasDeBanco/{id_psp}",
        params=query_params,
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    
    if r.ok:
        return r.json()
        
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})