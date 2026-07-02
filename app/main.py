from fastapi import FastAPI
from endpoints.cuentas import router as cuentas_router
from endpoints.cvu import router as cvu_router
from endpoints.alias import router as alias_router
from endpoints.transferencias import router as transferencias_router
from endpoints.saldos import router as saldos_router
app = FastAPI(
    title="Coinag PSP API",
    description="API para avisos de crédito, reversa, débitos y adhesiones",
    version="1.0.0",
)

app.include_router(cuentas_router)
app.include_router(cvu_router)
app.include_router(alias_router)
app.include_router(transferencias_router)
app.include_router(saldos_router)