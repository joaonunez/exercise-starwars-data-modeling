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

# Clase Producto (Se venden individualmente)
class Producto(Base):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)
    stock = Column(Integer, nullable=False, default=0)  # Campo de stock agregado

    # Foreign Key y relación con categoría de producto
    categoria_producto_id = Column(Integer, ForeignKey('categoria_producto.id'), nullable=False)
    categoria_producto = relationship('CategoriaProducto')

    # Foreign Key para cafetería
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria', back_populates='productos')

# Clase CategoriaProducto
class CategoriaProducto(Base):
    __tablename__ = 'categoria_producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

# Clase ComboMenu (Contiene los combos)
class ComboMenu(Base):
    __tablename__ = 'combo_menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)  # Nuevo campo 'nombre' agregado
    precio = Column(DECIMAL(10, 2), nullable=False)

    # Foreign Key para la cafetería
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria')

    # Relación con productos a través de la tabla intermedia
    productos = relationship('Producto', secondary='combo_menu_detail')

# Tabla intermedia para la relación muchos a muchos entre ComboMenu y Producto
combo_menu_detail = Table('combo_menu_detail', Base.metadata,
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
    empleados = relationship('Empleado')
    productos = relationship('Producto', back_populates='cafeteria')  # Relación con productos
    combos = relationship('ComboMenu')

# Nueva Clase TipoItem
class TipoItem(Base):
    __tablename__ = 'tipo_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)  # Tipo de ítem: 'producto' o 'combo'

# Configurar conexión a la base de datos (añadir motor a la base de datos)
# engine = create_engine('postgresql://usuario:password@localhost:5432/mi_base_de_datos')
# Base.metadata.create_all(engine)

# Dibujar el diagrama
render_er(Base, 'diagram.png')
