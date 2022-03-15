from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from sqlalchemy import func

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

@app.put("/dispositivos/{id}", response_model=schemas.Dispositivo, status_code=status.HTTP_200_OK)
def update_dispositivos_por_id(id: int, id_status_dispositivo: int, session: Session = Depends(get_session)):
    dispositivo_db = session.query(models.Dispositivo).get(id)
    status_validos = [1, 2]

    if id_status_dispositivo not in status_validos:
        raise HTTPException(status_code=404, detail=f"El id status del dispositivo {id_status_dispositivo} no existe")
    setattr(dispositivo_db, 'id_status_dispositivo', id_status_dispositivo)
    setattr(dispositivo_db, 'fecha_actualizacion', func.now())

    session.commit()
    session.refresh(dispositivo_db)

    return dispositivo_db




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


@app.post("/lecturas", response_model=schemas.Lectura, status_code=status.HTTP_201_CREATED)
def create_lectura(lectura: schemas.LecturaCreate, session: Session = Depends(get_session)):
    id_dispositivo = lectura.id_dispositivo
    dispositivo_db = session.query(models.Dispositivo).get(id_dispositivo)

    if lectura.potencia_actual < 0:
        raise HTTPException(status_code=404, detail=f"La potencia actual no puede ser menor a cero")

    if not dispositivo_db:
        raise HTTPException(status_code=404, detail=f"El dispositivo con id {id} no existe")

    elif dispositivo_db.id_status_dispositivo == 2:
        raise HTTPException(status_code=400,
                            detail=f"El dispositivo con id {id_dispositivo} se encuentra en mantenimiento")
    else:

        lectura_db = models.Lectura(
            id_dispositivo=id_dispositivo,
            id_tipo_dispositivo=dispositivo_db.id_tipo_dispositivo,
            potencia_actual=lectura.potencia_actual,
        )

        session.add(lectura_db)
        setattr(dispositivo_db, 'potencia_actual', lectura.potencia_actual)
        setattr(dispositivo_db, 'fecha_actualizacion', func.now())
        session.commit()
        session.refresh(lectura_db)

    return lectura_db


@app.get("/lecturas", response_model=List[schemas.Lectura], status_code=status.HTTP_200_OK)
def read_lecturas(session: Session = Depends(get_session)):
    lecturas_db = session.query(models.Lectura).all()
    print(lecturas_db)
    return lecturas_db


@app.get("/lecturas/dispositivo/{id}", response_model=List[schemas.Lectura], status_code=status.HTTP_200_OK)
def read_lecturas_por_dispotivito(id_dispositivo: int, session: Session = Depends(get_session)):
    lecturas_db = session.query(models.Lectura).all()
    lecturas_seleccionadas = [lectura for lectura in lecturas_db if id_dispositivo == lectura.id_dispositivo]
    return lecturas_seleccionadas


@app.get("/lecturas/dispositivo/tipo/{id}", response_model=List[schemas.Lectura], status_code=status.HTTP_200_OK)
def read_lecturas_por_dispotivito(id_tipo_dispositivo: int, session: Session = Depends(get_session)):
    lecturas_db = session.query(models.Lectura).all()
    lecturas_seleccionadas = [lectura for lectura in lecturas_db if id_tipo_dispositivo == lectura.id_tipo_dispositivo]
    return lecturas_seleccionadas


@app.delete("/lecturas/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_lectura(id: int, session: Session = Depends(get_session)):
    lectura = session.query(models.Lectura).get(id)

    if lectura:
        session.delete(lectura)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"La lectura con id {id} no existe")

    return None



@app.get("/energia_total/{id}", status_code=status.HTTP_200_OK)
def get_energia_toal_por_id(id_dispositivo: int, session: Session = Depends(get_session)):
    lecturas_db = session.query(models.Lectura).all()
    lecturas_seleccionadas = [lectura for lectura in lecturas_db if id_dispositivo == lectura.id_dispositivo]
    sum = 0
    for l in lecturas_seleccionadas:
        sum = sum + l.potencia_actual

    result = {
        "energia_total": {
            "id_dispositivo": id_dispositivo,
            "energia": sum
        }
    }
    return result
    return json.dumps(result)
