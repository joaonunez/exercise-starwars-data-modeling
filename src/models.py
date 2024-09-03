import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DateTime, DECIMAL, Text, Enum
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
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    registration_date = Column(DateTime, default='CURRENT_TIMESTAMP')
    
    role = relationship("Role")

class Campsite(Base):
    __tablename__ = 'campsite'
    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(DECIMAL(10, 2), nullable=False)
    rules = Column(Text, nullable=True)
    map_url = Column(String(255), nullable=True)
    image = Column(String(100), nullable=True)  # Cambiado de 'images' a 'image'
    
    provider = relationship("User")
    services = relationship("Service", back_populates="campsite")
    zones = relationship("Site", back_populates="campsite")
    details = relationship("CampsiteDetail", back_populates="campsite")

class Reservation(Base):
    __tablename__ = 'reservation'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    campsite_id = Column(Integer, ForeignKey('campsite.id'), nullable=False)
    site_id = Column(Integer, ForeignKey('site.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    number_of_people = Column(Integer, nullable=False)
    reservation_date = Column(DateTime, default='CURRENT_TIMESTAMP')
    
    user = relationship("User")
    campsite = relationship("Campsite")
    site = relationship("Site")

class Review(Base):
    __tablename__ = 'review'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    campsite_id = Column(Integer, ForeignKey('campsite.id'), nullable=False)
    comment = Column(Text, nullable=True)
    rating = Column(Integer, nullable=False)
    date = Column(DateTime, default='CURRENT_TIMESTAMP')
    
    user = relationship("User")
    campsite = relationship("Campsite")

class ServiceCategory(Base):
    __tablename__ = 'service_category'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

class Service(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, autoincrement=True)
    campsite_id = Column(Integer, ForeignKey('campsite.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('service_category.id'), nullable=False)
    
    campsite = relationship("Campsite", back_populates="services")
    category = relationship("ServiceCategory")

class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    campsite_id = Column(Integer, ForeignKey('campsite.id'), nullable=False)
    status = Column(Enum('available', 'unavailable', name='site_status'), default='available')
    
    campsite = relationship("Campsite", back_populates="zones")

class CampsiteDetail(Base):
    __tablename__ = 'campsite_detail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    campsite_id = Column(Integer, ForeignKey('campsite.id'), nullable=False)
    image = Column(String(100), nullable=False)
    rule = Column(Text, nullable=True)
    
    campsite = relationship("Campsite", back_populates="details")

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
