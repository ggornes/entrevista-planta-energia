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
    return "hello world"

@app.get("/dispositivos", response_model=schemas.Dispositivo, status_code=status.HTTP_200_OK)
def read_dispositivos(session: Session = Depends(get_session)):
    dispositivos_db = session.query(models.Dispositivo).all()
    return dispositivos_db


@app.post("/dispositivos", response_model=schemas.Dispositivo, status_code=status.HTTP_201_CREATED)
def create_dispositivo(dispositivo: schemas.DispositivoCreate, session: Session = Depends(get_session)):

    dispositivo_db = models.Dispositivo(nombre = dispositivo.nombre)

    session.add(dispositivo_db)
    session.commit()
    session.refresh(dispositivo_db)

    print(dispositivo_db)

    return dispositivo_db
