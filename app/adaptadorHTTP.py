import json
from httpcore2 import request
from pymongo import MongoClient
from requests.adapters import HTTPAdapter
from datetime import datetime
import os
from schemas import LogTrafico

MONGO_URL = os.getenv("MONGO")
MONGODB_DB = os.getenv("MONGODB_DB", "coinag").strip("'\"")

_mongo_client = MongoClient(MONGO_URL, serverSelectionTimeoutMS=5000)
_mongo_db = _mongo_client[MONGODB_DB]
_logs_collection = _mongo_db["logs"]

class MongoLoggerAdapter(HTTPAdapter):
    def send(self, request, *args, **kwargs):
        # 1. Ejecuta la petición original al banco de forma normal
        response = self.super_send(request, *args, **kwargs)
        
        try:
            # 2. Intentar parsear los cuerpos a JSON si es posible, sino guardarlos como texto
            req_body = request.body.decode('utf-8') if isinstance(request.body, bytes) else request.body
            try:
                req_body = json.loads(req_body) if req_body else None
            except ValueError:
                pass

            res_body = response.text
            try:
                res_body = response.json() if res_body else None
            except ValueError:
                pass

            log_objeto = LogTrafico(
                metodo=request.method,
                url=request.url,
                request_headers=dict(request.headers),
                request_body=req_body,
                status_code=response.status_code,
                response_headers=dict(response.headers),
                response_body=res_body
            )
            _logs_collection.insert_one(log_objeto.model_dump())
            
        except Exception as e:
            print(f"Error al guardar log en Mongo: {e}")
            
        return response

    def super_send(self, request, *args, **kwargs):
        return super().send(request, *args, **kwargs)