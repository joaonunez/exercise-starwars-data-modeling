import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time, Table, Text
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Clase Pais
class Pais(Base):
    __tablename__ = 'pais'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    # Relación con regiones
    regiones = relationship('Region')

# Clase Region
class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    # Foreign Key para país
    pais_id = Column(Integer, ForeignKey('pais.id'), nullable=False)
    pais = relationship('Pais')

    # Relación con comunas
    comunas = relationship('Comuna')

# Clase Comuna
class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    # Foreign Key para región
    region_id = Column(Integer, ForeignKey('region.id'), nullable=False)
    region = relationship('Region')

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

# Tabla intermedia User-Beneficio
user_beneficio = Table('user_beneficio', Base.metadata,
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('beneficio_id', Integer, ForeignKey('beneficio.id'), primary_key=True)
)

# Clase User (anteriormente Empleado)
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=False)
    rut = Column(String(12), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    
    # Nuevos campos para el login
    usuario = Column(String(50), unique=True, nullable=False)  # Usuario único para el login
    correo = Column(String(100), unique=True, nullable=False)  # Correo único para el login
    contraseña = Column(String(255), nullable=False)  # Contraseña encriptada para el login

    # Foreign Key y Relaciones
    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)
    rol = relationship('Rol')

    # Relación con beneficios a través de la tabla intermedia
    beneficios = relationship('Beneficio', secondary=user_beneficio)

    # Foreign Key para la cafetería
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria')

# Clase Producto (Se venden individualmente)
class Producto(Base):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False, default=0)

    # Foreign Key y relación con categoría de producto
    categoria_producto_id = Column(Integer, ForeignKey('categoria_producto.id'), nullable=False)
    categoria_producto = relationship('CategoriaProducto')

    # Foreign Key para cafetería
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria', back_populates='productos')

    # Foreign Key para tipo de ítem
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    tipo_item = relationship('TipoItem')

# Clase CategoriaProducto
class CategoriaProducto(Base):
    __tablename__ = 'categoria_producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

# Clase ComboMenu (Contiene los combos)
class ComboMenu(Base):
    __tablename__ = 'combo_menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)

    # Foreign Key para la cafetería
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria')

    # Foreign Key para tipo de ítem
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    tipo_item = relationship('TipoItem')

    # Relación con productos a través de la tabla intermedia
    productos = relationship('Producto', secondary='detalle_combo_menu')

# Tabla intermedia para la relación muchos a muchos entre ComboMenu y Producto
detalle_combo_menu = Table('detalle_combo_menu', Base.metadata,
    Column('combo_menu_id', Integer, ForeignKey('combo_menu.id'), primary_key=True),
    Column('producto_id', Integer, ForeignKey('producto.id'), primary_key=True)
)

# Clase Cafeteria
class Cafeteria(Base):
    __tablename__ = 'cafeteria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)

    # Foreign Key para comuna
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    comuna = relationship('Comuna')

    # Relaciones
    users = relationship('User')
    productos = relationship('Producto', back_populates='cafeteria')
    combos = relationship('ComboMenu')

# Clase TipoItem
class TipoItem(Base):
    __tablename__ = 'tipo_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)  # Tipo de ítem: 'producto' o 'combo'

# Clase Venta
class Venta(Base):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    monto_total = Column(Integer, nullable=False)
    estado = Column(String(50), nullable=False, default="pendiente")  # Estado de la venta
    comentarios = Column(Text, nullable=True)  # Campo para comentarios opcionales
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)  # Cambiado a user_id
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)

    # Relaciones
    user = relationship('User')  # Relación con User
    cafeteria = relationship('Cafeteria')
    detalles = relationship('DetalleVenta', back_populates='venta')

# Clase DetalleVenta
class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    # Foreign Key para la venta
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)

    # Foreign Key para el ítem (puede ser Producto o ComboMenu)
    item_id = Column(Integer, nullable=False)  # ID del producto o combo
    
    # Foreign Key para el tipo de ítem
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)  # Relación con TipoItem
    tipo_item = relationship('TipoItem')  # Relación con la tabla TipoItem
    
    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Integer, nullable=False)
    
    # Relación con la tabla Venta
    venta = relationship('Venta', back_populates='detalles')

# Configurar conexión a la base de datos (añadir motor a la base de datos)
# engine = create_engine('postgresql://usuario:password@localhost:5432/mi_base_de_datos')
# Base.metadata.create_all(engine)

# Dibujar el diagrama
render_er(Base, 'diagram.png')
