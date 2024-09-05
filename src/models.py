import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DECIMAL, Table
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
    salario_base = Column(DECIMAL(10, 2), nullable=False)

# Clase Beneficio
class Beneficio(Base):
    __tablename__ = 'beneficio'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(DECIMAL(10, 2), nullable=False)
    descripcion = Column(String(255), nullable=False)

# Tabla intermedia Empleado-Beneficio
empleado_beneficio = Table('empleado_beneficio', Base.metadata,
    Column('empleado_id', Integer, ForeignKey('empleado.id'), primary_key=True),
    Column('beneficio_id', Integer, ForeignKey('beneficio.id'), primary_key=True)
)

# Clase Empleado
class Empleado(Base):
    __tablename__ = 'empleado'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido_p = Column(String(100), nullable=False)
    apellido_m = Column(String(100), nullable=False)
    rut = Column(String(12), unique=True, nullable=False)
    fecha_de_nacimiento = Column(Date, nullable=False)

    # Foreign Key y Relaciones
    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)
    rol = relationship('Rol')

    # Relación con beneficios a través de la tabla intermedia
    beneficios = relationship('Beneficio', secondary=empleado_beneficio)

    # Foreign Key para la cafetería
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria')

# Clase Producto
class Producto(Base):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)
    stock_cafeteria = Column(Integer, nullable=False, default=0)  # Control de stock en la cafetería
    stock_almacen = Column(Integer, nullable=False, default=0)    # Control de stock en el almacén

    # Foreign Key y relación con categoría de producto
    categoria_producto_id = Column(Integer, ForeignKey('categoria_producto.id'), nullable=False)
    categoria_producto = relationship('CategoriaProducto')

# Clase CategoriaProducto (anteriormente TipoProducto)
class CategoriaProducto(Base):
    __tablename__ = 'categoria_producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

# Clase Menu
class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    precio = Column(DECIMAL(10, 2), nullable=False)

    # Foreign Key para cafetería
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria', back_populates='menus')

    # Relación con productos
    productos = relationship('Producto', secondary='menu_detail')

# Tabla intermedia para la relación muchos a muchos entre Menu y Producto
menu_detail = Table('menu_detail', Base.metadata,
    Column('menu_id', Integer, ForeignKey('menu.id'), primary_key=True),
    Column('producto_id', Integer, ForeignKey('producto.id'), primary_key=True)
)

# Clase Almacen
class Almacen(Base):
    __tablename__ = 'almacen'
    id = Column(Integer, primary_key=True, autoincrement=True)
    direccion = Column(String(255), nullable=False)

    # Foreign Key para la cafetería
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria')

    # Relación con áreas
    areas = relationship('Area')

# Clase Area (Ahora pertenece a un Almacen)
class Area(Base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, nullable=False)

    # Foreign Key y relación con almacén
    almacen_id = Column(Integer, ForeignKey('almacen.id'), nullable=False)
    almacen = relationship('Almacen')

    # Relación con cajas
    cajas = relationship('Caja')

# Clase Caja (Pertenece a un Area)
class Caja(Base):
    __tablename__ = 'caja'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, nullable=False)
    cantidad = Column(Integer, nullable=False)

    # Foreign Key y relación con área
    area_id = Column(Integer, ForeignKey('area.id'), nullable=False)
    area = relationship('Area')

    # Foreign Key y relación con producto
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)
    producto = relationship('Producto')

# Clase Cafetería
class Cafeteria(Base):
    __tablename__ = 'cafeteria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)

    # Foreign Key para comuna
    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    comuna = relationship('Comuna')

    # Relaciones
    empleados = relationship('Empleado')
    almacen = relationship('Almacen', uselist=False)

    # Relación con menús
    menus = relationship('Menu', back_populates='cafeteria')

# Configurar conexión a la base de datos (añadir motor a la base de datos)
# engine = create_engine('postgresql://usuario:password@localhost:5432/mi_base_de_datos')
# Base.metadata.create_all(engine)

## Dibujar el diagrama
render_er(Base, 'diagram.png')