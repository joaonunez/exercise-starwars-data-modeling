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

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
        }

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    rut = Column(String(12), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    phone = Column(String(15), nullable=True)  # New field
    role_id = Column(Integer, ForeignKey('role.id'), nullable=False)
    registration_date = Column(DateTime, default='CURRENT_TIMESTAMP')
    
    role = relationship("Role")

    def serialize(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "rut": self.rut,
            "email": self.email,
            "phone": self.phone,
            "role": self.role.serialize(),
            "registration_date": self.registration_date
        }

class Campsite(Base):
    __tablename__ = 'campsite'
    id = Column(Integer, primary_key=True, autoincrement=True)
    provider_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    name = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    rules = Column(Text, nullable=True)
    map_url = Column(String(255), nullable=True)
    image = Column(String(100), nullable=True)
    
    provider = relationship("User")
    services = relationship("Service", back_populates="campsite")
    zones = relationship("Site", back_populates="campsite")
    details = relationship("CampsiteDetail", back_populates="campsite")
    prices = relationship("Price", back_populates="campsite")

    def serialize(self):
        return {
            "id": self.id,
            "provider": self.provider.serialize(),
            "name": self.name,
            "location": self.location,
            "description": self.description,
            "rules": self.rules,
            "map_url": self.map_url,
            "image": self.image,
            "services": [service.serialize() for service in self.services],
            "zones": [zone.serialize() for zone in self.zones],
            "details": [detail.serialize() for detail in self.details],
            "prices": [price.serialize() for price in self.prices],
        }

class Price(Base):
    __tablename__ = 'price'
    id = Column(Integer, primary_key=True, autoincrement=True)
    campsite_id = Column(Integer, ForeignKey('campsite.id'), nullable=False)
    amount_per_day = Column(DECIMAL(10, 2), nullable=False, default=10000)

    campsite = relationship("Campsite", back_populates="prices")

    def serialize(self):
        return {
            "id": self.id,
            "campsite_id": self.campsite_id,
            "amount_per_day": float(self.amount_per_day),
        }

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

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "campsite": self.campsite.serialize(),
            "site": self.site.serialize(),
            "start_date": self.start_date,
            "end_date": self.end_date,
            "number_of_people": self.number_of_people,
            "reservation_date": self.reservation_date,
        }

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

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.serialize(),
            "campsite": self.campsite.serialize(),
            "comment": self.comment,
            "rating": self.rating,
            "date": self.date,
        }

class ServiceDetail(Base):
    __tablename__ = 'service_detail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    price = Column(DECIMAL(10, 2), nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": float(self.price),
        }

class Service(Base):
    __tablename__ = 'service'
    id = Column(Integer, primary_key=True, autoincrement=True)
    campsite_id = Column(Integer, ForeignKey('campsite.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service_detail.id'), nullable=False)
    
    campsite = relationship("Campsite", back_populates="services")
    service_detail = relationship("ServiceDetail")

    def serialize(self):
        return {
            "id": self.id,
            "campsite": self.campsite.serialize(),
            "service_detail": self.service_detail.serialize(),
        }

class Site(Base):
    __tablename__ = 'site'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    campsite_id = Column(Integer, ForeignKey('campsite.id'), nullable=False)
    status = Column(Enum('available', 'unavailable', name='site_status'), default='available')
    max_of_people = Column(Integer, nullable=False)

    campsite = relationship("Campsite", back_populates="zones")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "campsite_id": self.campsite_id,
            "status": self.status,
            "max_of_people": self.max_of_people,
        }

class CampsiteImage(Base):
    __tablename__ = 'campsite_image'
    id = Column(Integer, primary_key=True, autoincrement=True)
    campsite_id = Column(Integer, ForeignKey('campsite.id'), nullable=False)
    image = Column(String(100), nullable=False)
    
    campsite = relationship("Campsite")

    def serialize(self):
        return {
            "id": self.id,
            "campsite_id": self.campsite_id,
            "image": self.image,
        }

class CampsiteRule(Base):
    __tablename__ = 'campsite_rule'
    id = Column(Integer, primary_key=True, autoincrement=True)
    campsite_id = Column(Integer, ForeignKey('campsite.id'), nullable=False)
    rule = Column(Text, nullable=True)
    
    campsite = relationship("Campsite")

    def serialize(self):
        return {
            "id": self.id,
            "campsite_id": self.campsite_id,
            "rule": self.rule,
        }

class ReservationDetail(Base):
    __tablename__ = 'reservation_detail'
    id = Column(Integer, primary_key=True, autoincrement=True)
    reservation_id = Column(Integer, ForeignKey('reservation.id'), nullable=False)
    service_id = Column(Integer, ForeignKey('service_detail.id'), nullable=False)
    
    reservation = relationship("Reservation")
    service_detail = relationship("ServiceDetail")

    def serialize(self):
        return {
            "id": self.id,
            "reservation": self.reservation.serialize(),
            "service_detail": self.service_detail.serialize(),
        }

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
