"""
Script de prueba para el endpoint /PSP
Prueba el endpoint con diferentes escenarios
"""

import requests
import json
from datetime import datetime

# Configuración
BASE_URL = "http://localhost:5678"
ENDPOINT = "/PSP"




response = requests.get(
    f"{BASE_URL}{ENDPOINT}",
    headers={"Authorization": f"Bearer 9f3a7a2e4d8b1a6f0c5e2d9b7a3c1f0e"},
  
)

print(response.text,response.status_code)
        
      



