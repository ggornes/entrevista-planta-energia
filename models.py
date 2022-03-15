
import datetime
from sqlalchemy import Column, Integer, String, BIGINT, ForeignKey, func, FLOAT, DateTime
from database import Base

# Define To Do class inheriting from Base
class Dispositivo(Base):
    __tablename__ = 'dispositivos'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(256))
    id_tipo_dispositivo = Column(BIGINT, ForeignKey("tipo_dispositivo.id"))
    id_status_dispositivo = Column(BIGINT, ForeignKey("status_dispositivo.id"))
    potencia_actual = Column(FLOAT(precision=10, decimal_return_scale=None))
    fecha_alta = Column(DateTime(timezone=True), default=func.now())
    fecha_actualizacion = Column(DateTime(timezone=True), default=func.now())


    def __repr__(self):
        return 'Dispositivo:' + \
               f'id: {self.id}\n' + \
               f'nombre: {self.nombre}\n' + \
               f'id_tipo_dispositivo: {self.id_tipo_dispositivo}\n' + \
               f'id_status_dispositivo: {self.id_status_dispositivo}\n' + \
               f'potencia_actual: {self.potencia_actual}\n' + \
               f'fecha_alta: {self.fecha_alta}\n' + \
               f'fecha_actualizacion: {self.fecha_actualizacion}\n'


class TipoDispositivo(Base):
    __tablename__ = "tipo_dispositivo"
    id = Column(BIGINT, primary_key=True, index=True)
    nombre_tipo_dispositivo = Column(String(255), unique=True)


class StatusDispositivo(Base):
    __tablename__ = "status_dispositivo"
    id = Column(BIGINT, primary_key=True, index=True)
    descripcion = Column(String(255), unique=True)


class Lectura(Base):
    __tablename__ = 'lecturas'
    id = Column(Integer, primary_key=True)
    id_dispositivo = Column(BIGINT, ForeignKey("dispositivos.id"))
    id_tipo_dispositivo = Column(BIGINT, ForeignKey("tipo_dispositivo.id"))
    potencia_actual = Column(FLOAT(precision=10, decimal_return_scale=None))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return 'Lectura:' + \
               f'id: {self.id}\n' + \
               f'id_dispositivo: {self.id_dispositivo}\n' + \
               f'id_tipo_dispositivo: {self.id_tipo_dispositivo}\n' + \
               f'potencia_actual: {self.potencia_actual}\n' + \
               f'timestamp: {self.timestamp}\n'