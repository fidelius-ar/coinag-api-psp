from fastapi import APIRouter, Request, HTTPException, Query
import requests
import os
from auth import token_required
from app.schemas import (
    FiltrosSaldos,
    FiltroSaldoActual,
    FiltroSaldoDisponible
)
from session import client_banco

router = APIRouter()


@router.get("/saldos")
@token_required()
def obtener_consulta_saldos(
    request: Request,
    filtros: FiltrosSaldos = Query(),
):
    creds = request.state.credentials
    query_params = filtros.model_dump(exclude_none=True)

    r = client_banco.get(
        url=f"{os.getenv('URL')}/coelsapsp/v1/Saldos",
        params=query_params,
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )

    if r.ok:
        return r.json()
    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.get("/saldo-actual")
@token_required()
def obtener_saldo_actual(request: Request, filtro: FiltroSaldoActual = Query()):
    creds = request.state.credentials
    query_params = filtro.model_dump()
    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v1/SaldoActual",
        params=query_params,
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )
    if r.ok:
        return r.json()

    raise HTTPException(status_code=r.status_code, detail={"error": r.text})


@router.get("/SaldoDisponible")
@token_required()
def obtener_saldo_disponible(request: Request, filtro: FiltroSaldoDisponible = Query()):
    creds = request.state.credentials
    query_params = filtro.model_dump()

    r = client_banco.get(
        f"{os.getenv('URL')}/coelsapsp/v1/SaldoDisponible",
        params=query_params,
        headers={"Authorization": f"Bearer {creds.get('token_coinag')}"},
    )

    if r.ok:
        return r.json()

    raise HTTPException(status_code=r.status_code, detail={"error": r.text})
