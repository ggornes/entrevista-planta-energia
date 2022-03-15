from pydantic import BaseModel

class DispositivoCreate(BaseModel):
    nombre: str

class Dispositivo(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True