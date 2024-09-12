import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Table, Text, Float
from datetime import datetime
from sqlalchemy.orm import relationship, declarative_base
from eralchemy2 import render_er

Base = declarative_base()

# Clase País
class Pais(Base):
    __tablename__ = 'pais'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    regiones = relationship('Region', backref='pais')

# Clase Región
class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    pais_id = Column(Integer, ForeignKey('pais.id'), nullable=False)
    comunas = relationship('Comuna', backref='region')

# Clase Comuna
class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)

# Clase Rol
class Rol(Base):
    __tablename__ = 'rol'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    salario_base = Column(Integer, nullable=False)

# Clase Beneficio
class Beneficio(Base):
    __tablename__ = 'beneficio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    precio = Column(Integer, nullable=False)
    descripcion = Column(String(255), nullable=False)

# Tabla intermedia Beneficio-Usuario (Muchos a muchos)
beneficio_usuario = Table(
    'beneficio_usuario', Base.metadata,
    Column('beneficio_id', Integer, ForeignKey('beneficio.id'), primary_key=True),
    Column('usuario_rut', String(12), ForeignKey('usuario.rut'), primary_key=True)
)

# Clase Usuario
class Usuario(Base):
    __tablename__ = 'usuario'
    rut = Column(String(12), primary_key=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)

    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    
    beneficios = relationship('Beneficio', secondary=beneficio_usuario, backref='usuarios')

# Clase Cliente
class Cliente(Base):
    __tablename__ = 'cliente'
    rut = Column(String(12), primary_key=True)
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)
    contrasena = Column(String(255), nullable=False)
    usuario = Column(String(50), unique=True, nullable=False)

# Clase Favoritos
class Favoritos(Base):
    __tablename__ = 'favoritos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)

# Clase CategoriaProducto
class CategoriaProducto(Base):
    __tablename__ = 'categoria_producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

# Clase Producto
class Producto(Base):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    categoria_producto_id = Column(Integer, ForeignKey('categoria_producto.id'), nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)

# Clase ComboMenu
class ComboMenu(Base):
    __tablename__ = 'combo_menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)

    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)

# Tabla intermedia ComboMenu-Producto (Muchos a muchos)
detalle_combo_menu = Table(
    'detalle_combo_menu', Base.metadata,
    Column('combo_menu_id', Integer, ForeignKey('combo_menu.id'), primary_key=True),
    Column('producto_id', Integer, ForeignKey('producto.id'), primary_key=True)
)

# Clase Cafeteria
class Cafeteria(Base):
    __tablename__ = 'cafeteria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)

# Clase TipoItem
class TipoItem(Base):
    __tablename__ = 'tipo_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

# Clase Mesa
class Mesa(Base):
    __tablename__ = 'mesa'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, nullable=False)
    qr_code = Column(String(255), nullable=False)  # Almacenamiento de URL del código QR
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)

# Clase Venta
class Venta(Base):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(DateTime, nullable=False, default=datetime.now)  # Usamos DateTime para incluir fecha y hora
    monto_total = Column(Integer, nullable=False)
    estado = Column(String(50), nullable=False, default="pendiente")
    comentarios = Column(Text, nullable=True)

    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    mesero_rut = Column(String(12), ForeignKey('usuario.rut'), nullable=True)
    mesa_id = Column(Integer, ForeignKey('mesa.id'), nullable=True)

# Clase DetalleVenta
class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Integer, nullable=False)
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    item_id = Column(Integer, nullable=False)

# Clase CalificacionProducto
class CalificacionProducto(Base):
    __tablename__ = 'calificacion_producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)
    calificacion = Column(Float, nullable=False)
    fecha = Column(DateTime, nullable=False, default=datetime.now)

# Dibujar el diagrama
render_er(Base, 'diagrama_cafeteria.png')
