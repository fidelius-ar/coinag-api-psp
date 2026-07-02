import os
from datetime import datetime, timedelta
from functools import wraps
import requests
from fastapi import HTTPException, Request
from pymongo import MongoClient

MONGO_URL = os.getenv("MONGO")
MONGODB_DB = os.getenv("MONGODB_DB", "coinag").strip("'\"")

_mongo_client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
_mongo_db = _mongo_client[MONGODB_DB]
_token_collection = _mongo_db["clientes"]


def _get_token_from_header(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:].strip()
    if auth_header:
        return auth_header.strip()
    return request.headers.get("x-token")


def _parse_datetime(value):
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, (int, float)):
        try:
            return datetime.utcfromtimestamp(value)
        except (OverflowError, OSError):
            return None
    if isinstance(value, str):
        try:
            return datetime.fromisoformat(value)
        except ValueError:
            pass
    return None


def _token_is_expired(creds: dict) -> bool:
    token = creds.get("token_coinag")
    if not token:
        return True

    expires_at = _parse_datetime(creds.get("token_coinag_expires_at"))
    if expires_at is not None:
        return expires_at <= datetime.utcnow()

    issued_at = _parse_datetime(creds.get("token_coinag_issued_at"))
    expires_in = creds.get("token_coinag_expires_in")
    if issued_at is not None and expires_in is not None:
        try:
            return issued_at + timedelta(seconds=int(expires_in)) <= datetime.utcnow()
        except (TypeError, ValueError):
            pass

    return False


def _fetch_credentials_for_token(token: str) -> dict | None:
    doc = _token_collection.find_one(
        {"token": token},
        {
            "_id": 0,
            "username": 1,
            "password": 1,
            "client_id": 1,
            "client_secret": 1,
            "idPSP": 1,
            "cuit": 1,
            "token_coinag": 1,
            "token_coinag_expires_at": 1,
            "token_coinag_expires_in": 1,
            "token_coinag_issued_at": 1,
            "id_cuenta_recaudadora":1,
        },
    )
    if not doc:
        return None
    return {
        "username": doc.get("username", ""),
        "password": doc.get("password", ""),
        "client_id": doc.get("client_id", ""),
        "client_secret": doc.get("client_secret", ""),
        "idPSP": doc.get("idPSP", ""),
        "cuit": doc.get("cuit", ""),
        "token_coinag": doc.get("token_coinag"),
        "token_coinag_expires_at": doc.get("token_coinag_expires_at"),
        "token_coinag_expires_in": doc.get("token_coinag_expires_in"),
        "token_coinag_issued_at": doc.get("token_coinag_issued_at"),
        "id_cuenta_recaudadora": doc.get("id_cuenta_recaudadora"),
    }


def _get_token_expiration(token_info: dict) -> datetime | None:
    expires_at = token_info.get("expires_at")
    if expires_at is not None:
        return _parse_datetime(expires_at)
    expires_in = token_info.get("expires_in")
    if expires_in is not None:
        try:
            return datetime.utcnow() + timedelta(seconds=int(expires_in))
        except (TypeError, ValueError):
            return None
    return None


def _refresh_token_coinag(creds: dict, lookup_token: str) -> dict:
    token_info = get_token_coinag(
        creds.get("client_id"),
        creds.get("client_secret"),
        creds.get("username"),
        creds.get("password"),
    )
    access_token = token_info.get("access_token")
    if not access_token:
        raise HTTPException(
            status_code=500,
            detail="No se pudo obtener token_coinag de Coinag",
        )

    updated_fields = {
        "token_coinag": access_token,
        "token_coinag_issued_at": datetime.utcnow(),
    }
    expires_at = _get_token_expiration(token_info)
    if expires_at is not None:
        updated_fields["token_coinag_expires_at"] = expires_at
    if "expires_in" in token_info:
        updated_fields["token_coinag_expires_in"] = token_info.get("expires_in")

    if _token_collection is not None:
        _token_collection.update_one(
            {"token": lookup_token},
            {"$set": updated_fields},
        )

    return {
        **creds,
        "token_coinag": access_token,
        "token_coinag_issued_at": updated_fields["token_coinag_issued_at"],
        "token_coinag_expires_at": updated_fields.get("token_coinag_expires_at"),
        "token_coinag_expires_in": updated_fields.get("token_coinag_expires_in"),
    }


def token_required():
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if request is None:
                for value in args:
                    if isinstance(value, Request):
                        request = value
                        break

            token = _get_token_from_header(request)
            if not token:
                raise HTTPException(status_code=401, detail="Token inválido o ausente")

            creds = _fetch_credentials_for_token(token)
            if not creds:
                raise HTTPException(
                    status_code=401,
                    detail="Token inválido o sin credenciales asociadas",
                )

            if _token_is_expired(creds):
                creds = _refresh_token_coinag(creds, token)

            request.state.credentials = creds
           
            return  func(*args, **kwargs)

        return wrapper

    return decorator


def get_token_coinag(client_id, client_secret, username, password):
    r = requests.post(
        f"{os.getenv('URL')}/token",
        auth=(client_id, client_secret),
        data={"grant_type": "password", "username": username, "password": password},
    )
    if not r.ok:
        print(f"Error al obtener token de Coinag: {r.status_code} {r.text} {os.getenv('URL')}/authorize")
        raise HTTPException(
            status_code=502,
            detail=f"Error al obtener token de Coinag: {r.status_code} {r.text} {os.getenv('URL')}/authorize",
        )

        
    token_info = r.json()
    return token_info
