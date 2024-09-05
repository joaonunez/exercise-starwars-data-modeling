import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, DECIMAL
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Clase Rol
class Rol(Base):
    __tablename__ = 'rol'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(50), nullable=False)
    salario_base = Column(DECIMAL(10, 2), nullable=False)

# Clase Beneficios
class Beneficio(Base):
    __tablename__ = 'beneficios'
    id = Column(Integer, primary_key=True, autoincrement=True)
    valor = Column(DECIMAL(10, 2), nullable=False)
    descripcion = Column(String(255), nullable=False)

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

    beneficios_id = Column(Integer, ForeignKey('beneficios.id'), nullable=True)
    beneficios = relationship('Beneficio')

# Clase Mesa
class Mesa(Base):
    __tablename__ = 'mesas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, nullable=False)
    sillas = Column(Integer, nullable=False)

# Clase Producto
class Producto(Base):
    __tablename__ = 'productos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    valor = Column(DECIMAL(10, 2), nullable=False)

    # Foreign Key y relación con Tipo Producto
    tipo_producto_id = Column(Integer, ForeignKey('tipo_producto.id'), nullable=False)
    tipo_producto = relationship('TipoProducto')

# Clase TipoProducto
class TipoProducto(Base):
    __tablename__ = 'tipo_producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

# Clase Menu
class Menu(Base):
    __tablename__ = 'menu'
    id = Column(Integer, primary_key=True, autoincrement=True)

    # Relación con productos
    productos = relationship('Producto', secondary='menu_productos')

# Tabla intermedia para la relación muchos a muchos entre Menu y Productos
from sqlalchemy import Table

menu_productos = Table('menu_productos', Base.metadata,
    Column('menu_id', Integer, ForeignKey('menu.id'), primary_key=True),
    Column('producto_id', Integer, ForeignKey('productos.id'), primary_key=True)
)

# Clase Almacén
class Almacen(Base):
    __tablename__ = 'almacen'
    id = Column(Integer, primary_key=True, autoincrement=True)
    direccion = Column(String(255), nullable=False)

    # Relación con áreas
    area_id = Column(Integer, ForeignKey('area.id'), nullable=False)
    area = relationship('Area')

# Clase Area
class Area(Base):
    __tablename__ = 'area'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cantidad = Column(Integer, nullable=False)

    # Relación con Ileras
    ileras = relationship('Ilera')

# Clase Ilera
class Ilera(Base):
    __tablename__ = 'ileras'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, nullable=False)
    
    # Relación con cajas
    cajas = relationship('Caja')

# Clase Caja
class Caja(Base):
    __tablename__ = 'cajas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, nullable=False)
    cantidad = Column(Integer, nullable=False)

    # Relación con productos
    productos_id = Column(Integer, ForeignKey('productos.id'), nullable=False)
    productos = relationship('Producto')

# Clase Cafetería
class Cafeteria(Base):
    __tablename__ = 'cafeteria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)

    # Relaciones
    empleados = relationship('Empleado')
    mesas = relationship('Mesa')
    menu_id = Column(Integer, ForeignKey('menu.id'))
    menu = relationship('Menu')

# Configurar conexión a la base de datos (añadir motor a la base de datos)
# engine = create_engine('postgresql://usuario:password@localhost:5432/mi_base_de_datos')
# Base.metadata.create_all(engine)

## Draw from SQLAlchemy base
render_er(Base, 'diagram.png')
