from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime,date

class ModificacionCvu(BaseModel):
    titular: str = Field(..., max_length=40, description="Nombre del titular de la CVU.")
    tipoPersona: Literal["F", "J"] = Field(..., description="Tipo de persona: F (Física) o J (Jurídica).")


class AltaCVU(BaseModel):
    cuit: int
    titular: str = Field(..., max_length=40, description="Nombre del titular de la CVU.")
    tipoPersona: Literal["F", "J"] = Field(..., description="Tipo de persona: F (Física) o J (Jurídica).")


class AltaAlias(BaseModel):
    titular: str = Field(..., max_length=40, description="Nombre del titular de la cuenta")
    alias: str = Field(..., max_length=20, description="Alias a asignar a la cuenta")


class ModificarAlias(BaseModel):
    titular: str = Field(..., max_length=40, description="Nombre del titular de la cuenta")
    nuevoAlias: str = Field(..., max_length=20, description="Nuevo alias para la cuenta")


class TransferenciaRequest(BaseModel):
    idTrxClient: str = Field(
        ..., 
        max_length=19, 
        description="ID que comienza con idPSP o idEmpresa (1-4 dígitos) seguido de 15 dígitos secuenciales."
    )
    cuitDebito: str = Field(..., max_length=11, description="CUIT del Titular de la cuenta de origen")
    cbuDebito: str = Field(..., max_length=22, description="CBU/CVU desde donde se realizará el débito")
    titularDebito: str = Field(..., max_length=40, description="Nombre y Apellido del titular de la cuenta de origen")
    cuitCredito: str = Field(..., max_length=11, description="CUIT del Titular de la cuenta de destino")
    cbuCredito: str = Field(..., max_length=22, description="CBU/CVU de la cuenta destino donde se acreditará")
    concepto: str = Field(..., max_length=3, description="Conceptos válidos según el BCRA")
    importe: float = Field(..., description="Importe de la transferencia (Decimal 13,2)")
    descripcion: str = Field(..., max_length=100, description="Descripción adicional a registrar sobre el movimiento")


class FiltrosConciliacion(BaseModel):
    # Parámetros Requeridos por el Banco
    FechaDesde: datetime = Field(..., description="Fecha desde la que se quieren filtrar (YYYY-MM-DDTHh:mm:ss)")
    FechaHasta: datetime = Field(..., description="Fecha hasta la que se quieren filtrar (YYYY-MM-DDTHh:mm:ss)")
    Pagina: int = Field(..., description="Número de página en la que desea posicionar la consulta")
    IdCuentaRecaudadora: int = Field(..., description="Se puede filtrar sólo para una cuenta recaudadora en particular")
    
    # Parámetros Opcionales
    CVU: str | None = Field(None, description="Se puede filtrar sólo los movimientos realizados para una CVU")
    Tipo: str | None = Field(None, description="Filtrar por movimientos de 'D' Débito o 'C' Crédito")
    Conciliado: bool | None = Field(None, description="Filtro booleano que permite sólo filtrar lo conciliado o no")


class FiltrosConciliacionTransferencias(BaseModel):
    # Parámetros Requeridos
    FechaConciliacion: datetime = Field(..., description="Fecha en la que se quiere realizar la conciliación (YYYY-MM-DDTHh:mm:ss)")
    Pagina: int = Field(..., description="Número de página en la que desea posicionar la consulta")
    IdCuentaRecaudadora: int | None = Field(None, description="Se puede filtrar sólo para conciliar una cuenta recaudadora en particular")


class FiltrosSaldos(BaseModel):
    # Parámetros Requeridos
    fechaDesde: date = Field(..., description="Fecha desde la que se desea consultar el saldo (YYYY-MM-DD)")
    fechaHasta: date = Field(..., description="Fecha hasta la que se desea consultar el saldo (YYYY-MM-DD)")
    CBU: str = Field(..., max_length=22, description="CBU/CVU requerida de la consulta")
    
    # Parámetro Opcional (Paginación)
    Skip: int | None = Field(None, description="Cantidad de registros a saltear (debe ser múltiplo de top)")


class FiltroSaldoActual(BaseModel):
    CBU: str = Field(..., max_length=22, description="CBU/CVU de la cuenta a consultar el saldo actual")


class FiltroSaldoDisponible(BaseModel):
    CBU: str = Field(..., max_length=22, description="CBU/CVU de la cuenta a consultar")

class LogTrafico(BaseModel):
    fecha: datetime = Field(default_factory=datetime.utcnow)
    metodo: str
    url: str
    request_headers: dict
    request_body: str | dict | None = None
    status_code: int
    response_headers: dict
    response_body: str | dict | None = None