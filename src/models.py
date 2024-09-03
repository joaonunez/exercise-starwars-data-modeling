import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, DECIMAL, Text, Boolean, Enum
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Rol(Base):
    __tablename__ = 'rol'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(50), nullable=False)

class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    contraseña = Column(String(255), nullable=False)
    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)
    fecha_registro = Column(DateTime, default='CURRENT_TIMESTAMP')
    activo = Column(Boolean, default=True)
    
    rol = relationship("Rol")

class Camping(Base):
    __tablename__ = 'camping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    proveedor_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    nombre = Column(String(100), nullable=False)
    ubicacion = Column(String(255), nullable=False)
    descripcion = Column(Text, nullable=True)
    precio = Column(DECIMAL(10, 2), nullable=False)
    reglas = Column(Text, nullable=True)
    mapa_url = Column(String(255), nullable=True)
    imagenes = Column(String(100), nullable=True)  # Cambiado de JSON a VARCHAR(100)
    
    proveedor = relationship("Usuario")
    servicios = relationship("Servicio", back_populates="camping")
    zonas = relationship("Sitio", back_populates="camping")
    detalles = relationship("DetalleCamping", back_populates="camping")

class Reserva(Base):
    __tablename__ = 'reserva'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    camping_id = Column(Integer, ForeignKey('camping.id'), nullable=False)
    sitio_id = Column(Integer, ForeignKey('sitio.id'), nullable=False)  # Nuevo campo
    fecha_inicio = Column(Date, nullable=False)
    fecha_fin = Column(Date, nullable=False)
    cantidad_personas = Column(Integer, nullable=False)  # Cambiado de 'total' a 'cantidad_personas'
    fecha_reserva = Column(DateTime, default='CURRENT_TIMESTAMP')
    
    usuario = relationship("Usuario")
    camping = relationship("Camping")
    sitio = relationship("Sitio")

class Reseña(Base):
    __tablename__ = 'reseña'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    camping_id = Column(Integer, ForeignKey('camping.id'), nullable=False)
    comentario = Column(Text, nullable=True)
    calificacion = Column(Integer, nullable=False)
    fecha = Column(DateTime, default='CURRENT_TIMESTAMP')
    
    usuario = relationship("Usuario")
    camping = relationship("Camping")

class CategoriaDeServicio(Base):
    __tablename__ = 'categoria_de_servicio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    descripcion = Column(String(100), nullable=False)

class Servicio(Base):
    __tablename__ = 'servicio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    camping_id = Column(Integer, ForeignKey('camping.id'), nullable=False)
    categoria_id = Column(Integer, ForeignKey('categoria_de_servicio.id'), nullable=False)
    
    camping = relationship("Camping", back_populates="servicios")
    categoria = relationship("CategoriaDeServicio")

class Sitio(Base):
    __tablename__ = 'sitio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)  # Nombre o descripción de la zona
    camping_id = Column(Integer, ForeignKey('camping.id'), nullable=False)
    estado = Column(Enum('disponible', 'no_disponible', name='estado_zona'), default='disponible')
    
    camping = relationship("Camping", back_populates="zonas")

class DetalleCamping(Base):
    __tablename__ = 'detalle_camping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    camping_id = Column(Integer, ForeignKey('camping.id'), nullable=False)
    imagen = Column(String(100), nullable=False)  # URL de la imagen
    regla = Column(Text, nullable=True)  # Regla asociada
    
    camping = relationship("Camping", back_populates="detalles")

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
