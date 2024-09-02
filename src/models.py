import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, DECIMAL, Text, JSON, Boolean, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Rol(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(50), nullable=False)

class Usuario(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey('roles.id'), nullable=False)
    fecha_registro = Column(DateTime, default='CURRENT_TIMESTAMP')
    activo = Column(Boolean, default=True)
    
    rol = relationship("Rol")

class Camping(Base):
    __tablename__ = 'campings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    proveedor_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(DECIMAL(10, 2), nullable=False)
    luz_electrica = Column(Boolean, default=False)
    reglas = Column(Text, nullable=True)
    politicas_cancelacion = Column(Text, nullable=True)
    imagenes = Column(JSON, nullable=True)  # Almacena URLs de imágenes en formato JSON
    mapa_url = Column(String(255), nullable=True)
    
    proveedor = relationship("Usuario")
    servicios = relationship("Servicio", back_populates="camping")

class Reserva(Base):
    __tablename__ = 'reservas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    camping_id = Column(Integer, ForeignKey('campings.id'), nullable=False)
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    total = Column(DECIMAL(10, 2), nullable=False)
    estado = Column(Enum('realizada', 'perdida', 'en_proceso', name='estado_reserva'), default='en_proceso')
    fecha_reserva = Column(DateTime, default='CURRENT_TIMESTAMP')
    
    usuario = relationship("Usuario")
    camping = relationship("Camping")

class Reseña(Base):
    __tablename__ = 'reseñas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    camping_id = Column(Integer, ForeignKey('campings.id'), nullable=False)
    comentario = Column(Text, nullable=True)
    calificacion = Column(Integer, nullable=False)
    fecha = Column(DateTime, default='CURRENT_TIMESTAMP')
    
    usuario = relationship("Usuario")
    camping = relationship("Camping")

class Transaccion(Base):
    __tablename__ = 'transacciones'
    id = Column(Integer, primary_key=True, autoincrement=True)
    proveedor_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    reserva_id = Column(Integer, ForeignKey('reservas.id'), nullable=False)
    monto = Column(DECIMAL(10, 2), nullable=False)
    metodo_pago = Column(String(50), nullable=False)
    fecha = Column(DateTime, default='CURRENT_TIMESTAMP')
    
    proveedor = relationship("Usuario")
    reserva = relationship("Reserva")

class MetodoPago(Base):
    __tablename__ = 'metodos_pago'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'), nullable=False)
    tipo_pago = Column(String(50), nullable=False)
    detalles_pago = Column(JSON, nullable=True)
    activo = Column(Boolean, default=True)
    
    usuario = relationship("Usuario")

class Estadistica(Base):
    __tablename__ = 'estadisticas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total_reservas = Column(Integer, nullable=True)
    reservas_realizadas = Column(Integer, nullable=True)
    reservas_perdidas = Column(Integer, nullable=True)
    reservas_en_proceso = Column(Integer, nullable=True)
    ventas_totales = Column(DECIMAL(10, 2), nullable=True)
    fecha = Column(DateTime, default='CURRENT_TIMESTAMP')

    def to_dict(self):
        return {}

class Servicio(Base):
    __tablename__ = 'servicios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)  # Nombre del servicio (e.g., internet, minimarket, restaurante)
    camping_id = Column(Integer, ForeignKey('campings.id'), nullable=False)
    
    camping = relationship("Camping", back_populates="servicios")

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
