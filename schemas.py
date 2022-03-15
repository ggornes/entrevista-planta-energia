from datetime import datetime
from pydantic import BaseModel


class DispositivoCreate(BaseModel):
    nombre: str
    id_tipo_dispositivo: int
    id_status_dispositivo: int
    potencia_actual: float


class Dispositivo(BaseModel):
    id: int
    nombre: str
    id_tipo_dispositivo: int
    id_status_dispositivo: int
    potencia_actual: float
    fecha_alta: datetime
    fecha_actualizacion: datetime

    class Config:
        orm_mode = True


class LecturaCreate(BaseModel):
    id_dispositivo: int
    potencia_actual: float

class Lectura(BaseModel):
    id: int
    id_dispositivo: int
    id_tipo_dispositivo: int
    potencia_actual: float
    timestamp: datetime

    class Config:
        orm_mode = True
