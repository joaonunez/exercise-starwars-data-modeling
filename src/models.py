import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(80), nullable=False)
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    subscription_date = Column(DateTime, default=datetime.now, nullable=False)

    favorites = relationship('Favorite', back_populates='user')

class Planet(Base):
    __tablename__ = 'planet'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    climate = Column(String(50))
    terrain = Column(String(50))

class Character(Base):
    __tablename__ = 'character'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    height = Column(String(10))
    weight = Column(String(10))
    gender = Column(String(10))

class Favorite(Base):
    __tablename__ = 'favorite'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    planet_id = Column(Integer, ForeignKey('planet.id'), nullable=True)
    character_id = Column(Integer, ForeignKey('character.id'), nullable=True)

    user = relationship('User', back_populates='favorites')
    planet = relationship('Planet')
    character = relationship('Character')

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
