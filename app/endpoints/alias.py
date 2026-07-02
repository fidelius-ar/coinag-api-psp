import os
import requests
from fastapi import APIRouter, HTTPException, Request
from auth import token_required
from app.schemas import AltaAlias,ModificarAlias
from session import client_banco
router = APIRouter()


@router.get("/alias/{alias}")
@token_required()
def consultar_alias(alias: str, request: Request):
    creds = request.state.credentials
    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v1/Alias/{alias}",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})




@router.post("/alias/{cuit}/{cbu}")
@token_required()
def alta_alias(cuit: str, cbu: str, payload: AltaAlias, request: Request):
    creds = request.state.credentials

    r = client_banco.post(
        f"{os.getenv('URL')}/coelsapsp/v1/Alias/{cuit}/{cbu}",
        json=payload.model_dump(),
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    
    if r.ok:
        return r.json()
        
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})



@router.put("/alias/{cuit}/{cbu}/{alias}")
@token_required()
def modificar_alias(cuit: str, cbu: str, alias: str, payload: ModificarAlias, request: Request):
    creds = request.state.credentials

    r = client_banco.put(
        f"{os.getenv('URL')}/coelsapsp/v1/Alias/{cuit}/{cbu}/{alias}",
        json=payload.model_dump(),
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    
    if r.ok:
        return r.json()
        
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})



@router.delete("/alias/{cuit}/{cbu}/{alias}")
@token_required()
def baja_alias(cuit: str, cbu: str, alias: str, request: Request):
    creds = request.state.credentials
    r = client_banco.delete(
        f"{os.getenv('URL')}/coelsapsp/v1/Alias/{cuit}/{cbu}/{alias}",
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json() if r.text else {"message": "Alias eliminado correctamente"}
        
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})