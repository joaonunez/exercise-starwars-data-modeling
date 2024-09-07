import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, DECIMAL, Text, Enum, JSON
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    rut = Column(String(12), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=True)
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    registration_date = Column(DateTime, default='CURRENT_TIMESTAMP')
    
    role = relationship("Role")

class Camping(Base):
    __tablename__ = 'camping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(100), nullable=False)
    rut_del_negocio = Column(String(12), nullable=False)  # Nuevo campo
    razon_social = Column(String(100), nullable=False)  # Nuevo campo
    comuna_id = Column(Integer, nullable=False)  # Nuevo campo
    region = Column(String(50), nullable=False)  # Nuevo campo
    telefono = Column(String(15), nullable=False)  # Nuevo campo
    direccion = Column(String(255), nullable=False)  # Nuevo campo
    url_web = Column(String(255), nullable=True)  # Nuevo campo
    url_google_maps = Column(String(255), nullable=True)  # Nuevo campo
    description = Column(Text, nullable=True)
    rules = Column(JSON, nullable=True)  # Cambiado a JSON
    main_image = Column(JSON, nullable=True)  # Foto principal
    images = Column(JSON, nullable=True)  # Álbum de imágenes en JSON
    services = Column(JSON, nullable=True)  # Servicios en JSON
    provider = relationship("User")
    zones = relationship("Site", back_populates="camping")

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    site_id = Column(Integer, ForeignKey('site.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    number_of_people = Column(Integer, nullable=False)
    reservation_date = Column(DateTime, default='CURRENT_TIMESTAMP')
    selected_services = Column(JSON, nullable=True)  # Cambiado a JSON
    total_amount = Column(DECIMAL(10, 2), nullable=False, default=0)  # Campo de monto total en inglés

    user = relationship("User")
    site = relationship("Site")

class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    campsite_id = Column(Integer, ForeignKey('camping.id'), nullable=False)
    comment = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)
    date = Column(DateTime, default='CURRENT_TIMESTAMP')

    user = relationship("User")
    camping = relationship("Camping")

class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    campsite_id = Column(Integer, ForeignKey('camping.id'), nullable=False)
    status = Column(Enum('available', 'unavailable', name='site_status'), default='available')
    max_of_people = Column(Integer, nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False, default=10000)  # Nuevo campo
    facilities = Column(JSON, nullable=True)  # Cambiado a JSON
    dimensions = Column(JSON, nullable=True)  # Objeto con "largo" y "ancho"

    camping = relationship("Camping", back_populates="zones")

# Render the SQLAlchemy model diagram
render_er(Base, 'diagram.png')
