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

# Colores para output
class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"


def print_test(test_name: str, status: str, message: str = ""):
    """Imprime resultado del test formateado"""
    if status == "PASS":
        print(f"{Colors.GREEN}✓ {test_name}{Colors.RESET}")
    elif status == "FAIL":
        print(f"{Colors.RED}✗ {test_name}: {message}{Colors.RESET}")
    else:  # INFO
        print(f"{Colors.BLUE}ℹ {test_name}{Colors.RESET}")


def print_response(response, token_used=None):
    """Imprime los detalles de la respuesta"""
    print(f"\n{Colors.YELLOW}--- Detalles de la respuesta ---{Colors.RESET}")
    print(f"Status Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    if token_used:
        print(f"Token usado: {token_used[:20]}..." if len(token_used) > 20 else f"Token usado: {token_used}")
    try:
        print(f"Body: {json.dumps(response.json(), indent=2, default=str)}")
    except:
        print(f"Body: {response.text}")
    print(f"{Colors.YELLOW}--- Fin detalles ---{Colors.RESET}\n")


def test_without_token():
    """Test 1: Petición sin token (debe fallar con 401)"""
    print(f"\n{Colors.BLUE}Test 1: Petición SIN token{Colors.RESET}")
    try:
        response = requests.get(f"{BASE_URL}{ENDPOINT}", timeout=5)
        if response.status_code == 401:
            print_test("Sin token - Retorna 401", "PASS")
        else:
            print_test("Sin token - Retorna 401", "FAIL", f"Retornó {response.status_code}")
        print_response(response)
        return response.status_code == 401
    except requests.exceptions.ConnectionError:
        print_test("Conexión a servidor", "FAIL", "No se pudo conectar")
        return False


def test_with_invalid_token():
    """Test 2: Petición con token inválido (debe fallar con 401)"""
    print(f"\n{Colors.BLUE}Test 2: Petición con token INVÁLIDO{Colors.RESET}")
    invalid_token = "invalid-token-12345"
    try:
        response = requests.get(
            f"{BASE_URL}{ENDPOINT}",
            headers={"Authorization": f"Bearer {invalid_token}"},
            timeout=5
        )
        if response.status_code == 401:
            print_test("Token inválido - Retorna 401", "PASS")
        else:
            print_test("Token inválido - Retorna 401", "FAIL", f"Retornó {response.status_code}")
        print_response(response, invalid_token)
        return response.status_code == 401
    except requests.exceptions.ConnectionError:
        print_test("Conexión a servidor", "FAIL", "No se pudo conectar")
        return False


def test_with_valid_token(token: str):
    """Test 3: Petición con token válido"""
    print(f"\n{Colors.BLUE}Test 3: Petición con token VÁLIDO{Colors.RESET}")
    print_test("Token a usar", "INFO", token[:20] + "...")
    
    try:
        response = requests.get(
            f"{BASE_URL}{ENDPOINT}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=5
        )
        
        print_response(response, token)
        
        if response.status_code == 200:
            print_test("Token válido - Retorna 200", "PASS")
            data = response.json()
            
            # Verificar estructura de respuesta
            checks = [
                ("status == 'ok'", data.get("status") == "ok"),
                ("endpoint == '/PSP'", data.get("endpoint") == "/PSP"),
                ("recibido existe", "recibido" in data),
                ("procesado_en existe", "procesado_en" in data),
            ]
            
            for check_name, check_result in checks:
                status = "PASS" if check_result else "FAIL"
                print_test(f"Verificación: {check_name}", status)
            
            return all(check[1] for check in checks)
        else:
            print_test("Token válido - Retorna 200", "FAIL", f"Retornó {response.status_code}")
            return False
            
    except requests.exceptions.ConnectionError:
        print_test("Conexión a servidor", "FAIL", "No se pudo conectar")
        return False


def test_with_custom_header():
    """Test 4: Petición con token en header x-token"""
    print(f"\n{Colors.BLUE}Test 4: Petición con token en header x-token{Colors.RESET}")
    test_token = "test-token-value"
    
    try:
        response = requests.get(
            f"{BASE_URL}{ENDPOINT}",
            headers={"x-token": test_token},
            timeout=5
        )
        print_response(response, test_token)
        print_test("Header x-token", "PASS" if response.status_code in [200, 401] else "FAIL")
        return True
    except requests.exceptions.ConnectionError:
        print_test("Conexión a servidor", "FAIL", "No se pudo conectar")
        return False


def run_all_tests(valid_token: str = None):
    """Ejecuta todos los tests"""
    print(f"\n{Colors.GREEN}{'='*50}")
    print(f"INICIO DE PRUEBAS - Endpoint: {ENDPOINT}")
    print(f"Servidor: {BASE_URL}")
    print(f"{'='*50}{Colors.RESET}\n")
    
    results = []
    
    # Test sin token
    results.append(("Sin token", test_without_token()))
    
    # Test con token inválido
    results.append(("Token inválido", test_with_invalid_token()))
    
    # Test con header x-token
    results.append(("Header x-token", test_with_custom_header()))
    
    # Test con token válido (si se proporciona)
    if valid_token:
        results.append(("Token válido", test_with_valid_token(valid_token)))
    else:
        print(f"\n{Colors.YELLOW}⚠ Test con token válido omitido (no se proporcionó token){Colors.RESET}")
    
    # Resumen
    print(f"\n{Colors.GREEN}{'='*50}")
    print("RESUMEN DE RESULTADOS")
    print(f"{'='*50}{Colors.RESET}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if result else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests pasados")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    import sys
    
    # Acepta token como argumento: python test_endpoint.py "tu-token-aqui"
    valid_token = sys.argv[1] if len(sys.argv) > 1 else None
    
    if valid_token:
        print(f"{Colors.GREEN}Token válido proporcionado, se ejecutará test con token{Colors.RESET}")
    else:
        print(f"{Colors.YELLOW}Nota: Para probar con token válido, ejecuta:{Colors.RESET}")
        print(f"{Colors.BLUE}python test_endpoint.py 'tu-token-aqui'{Colors.RESET}")
    
    run_all_tests('9f3a7a2e4d8b1a6f0c5e2d9b7a3c1f0e')
