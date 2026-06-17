import os
import inspect
from contextvars import ContextVar
from functools import wraps
from inspect import iscoroutinefunction

from fastapi import HTTPException, Request
from pymongo import MongoClient
from starlette.concurrency import run_in_threadpool

MONGO_URL = os.getenv("MONGO")
MONGODB_DB = os.getenv("MONGODB_DB", "coinag").strip("'\"")

_mongo_client = None
_mongo_db = None
_token_collection = None

if MONGO_URL:
    _mongo_client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
    _mongo_db = _mongo_client[MONGODB_DB]
    _token_collection = _mongo_db["tokens"]



def _get_token_from_header(request: Request) -> str | None:
    auth_header = request.headers.get("Authorization", "")
    if auth_header.startswith("Bearer "):
        return auth_header[7:].strip()
    if auth_header:
        return auth_header.strip()
    return request.headers.get("x-token")


def _fetch_credentials_for_token(token: str) -> dict | None:
    if  _token_collection is None:
        raise HTTPException(status_code=500, detail="MongoDB no está configurado para validación de token")
    doc = _token_collection.find_one(
        {"token": token},
        {"_id": 0, "username": 1, "password": 1, "client_id": 1, "client_secret": 1, "idPsp": 1, "cuit": 1},
    )
    if not doc:
        return None
    return {
        "username": doc.get("username", ""),
        "password": doc.get("password", ""),
        "client_id": doc.get("client_id", ""),
        "client_secret": doc.get("client_secret", ""),
        "idPsp": doc.get("idPsp", ""),
        "cuit": doc.get("cuit", ""),
    }



def token_required():
    def decorator(func):
        sig = inspect.signature(func)
        pass_credentials = "credentials" in sig.parameters

        @wraps(func)
        async def wrapper(*args, **kwargs):
            request = kwargs.get("request")
            if request is None:
                for a in args:
                    if isinstance(a, Request):
                        request = a
                        break

            if request is None:
                raise HTTPException(status_code=500, detail="Request object no disponible para validación de token")

            token = _get_token_from_header(request)
            if not token:
                raise HTTPException(status_code=401, detail="Token inválido o ausente")

            creds = _fetch_credentials_for_token(token)
            if not creds:
                raise HTTPException(status_code=401, detail="Token inválido o sin credenciales asociadas")
            try:
                request.state.credentials = creds
            except Exception:
                pass

            call_kwargs = dict(kwargs)
            if pass_credentials:
                call_kwargs["credentials"] = creds

            if iscoroutinefunction(func):
                return await func(*args, **call_kwargs)
            return await run_in_threadpool(func, *args, **call_kwargs)

        return wrapper

    return decorator
