from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas

# Create the database
Base.metadata.create_all(engine)

# Initialize app
app = FastAPI()


# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
def root():
    return "OK"


@app.get("/dispositivos/{id}", response_model=schemas.Dispositivo, status_code=status.HTTP_200_OK)
def read_dispositivo_por_id(id: int, session: Session = Depends(get_session)):
    dispositivo_db = session.query(models.Dispositivo).get(id)
    if not dispositivo_db:
        raise HTTPException(status_code=404, detail=f"El dispositivo con id {id} no existe")

    return dispositivo_db


@app.get("/dispositivos", response_model=List[schemas.Dispositivo], status_code=status.HTTP_200_OK)
def read_dispositivos(session: Session = Depends(get_session)):
    dispositivos_db = session.query(models.Dispositivo).all()
    return dispositivos_db


@app.get("/dispositivos/tipo/{id}", response_model=List[schemas.Dispositivo], status_code=status.HTTP_200_OK)
def read_dispositivos_por_tipo(id_tipo: int, session: Session = Depends(get_session)):
    dispositivos_db = session.query(models.Dispositivo).all()
    dispositivos_seleccionados = [d for d in dispositivos_db if id_tipo == d.id_tipo_dispositivo]
    return dispositivos_seleccionados


@app.post("/dispositivos", response_model=schemas.Dispositivo, status_code=status.HTTP_201_CREATED)
def create_dispositivo(dispositivo: schemas.DispositivoCreate, session: Session = Depends(get_session)):
    dispositivo_db = models.Dispositivo(
        nombre=dispositivo.nombre,
        id_tipo_dispositivo=dispositivo.id_tipo_dispositivo,
        id_status_dispositivo=dispositivo.id_status_dispositivo,
        potencia_actual=dispositivo.potencia_actual,
    )

    session.add(dispositivo_db)
    session.commit()
    session.refresh(dispositivo_db)

    return dispositivo_db


@app.delete("/dispositivos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_dispositivo(id: int, session: Session = Depends(get_session)):
    dispositivo = session.query(models.Dispositivo).get(id)

    if dispositivo:
        session.delete(dispositivo)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"El dispositivo con id {id} no existe")

    return None
