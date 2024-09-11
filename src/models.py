import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time, Table, Text, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er

Base = declarative_base()

# Clase País
class Pais(Base):
    __tablename__ = 'pais'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    regiones = relationship('Region')

# Clase Región
class Region(Base):
    __tablename__ = 'region'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

    pais_id = Column(Integer, ForeignKey('pais.id'), nullable=False)
    pais = relationship('Pais')

    comunas = relationship('Comuna')

# Clase Comuna
class Comuna(Base):
    __tablename__ = 'comuna'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

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

# Tabla intermedia Usuario-Beneficio
usuario_beneficio = Table('usuario_beneficio', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id'), primary_key=True),
    Column('beneficio_id', Integer, ForeignKey('beneficio.id'), primary_key=True)
)

# Nueva tabla Favoritos
class Favoritos(Base):
    __tablename__ = 'favoritos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)

# Nueva tabla HistorialPedidos
class HistorialPedidos(Base):
    __tablename__ = 'historial_pedidos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)
    fecha = Column(Date, nullable=False)

# Clase Usuario
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=False)
    rut = Column(String(12), unique=True, nullable=False)
    fecha_nacimiento = Column(Date, nullable=False)
    
    usuario = Column(String(50), unique=True, nullable=False)  
    correo = Column(String(100), unique=True, nullable=False)  
    contrasena = Column(String(255), nullable=False)  

    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)
    rol = relationship('Rol')

    beneficios = relationship('Beneficio', secondary=usuario_beneficio)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria')

    # Nuevas relaciones para favoritos y historial de pedidos
    favoritos = relationship('Favoritos')
    historial_pedidos = relationship('HistorialPedidos')

# Clase Producto
class Producto(Base):
    __tablename__ = 'producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)
    stock = Column(Integer, nullable=False, default=0)
    
    categoria_producto_id = Column(Integer, ForeignKey('categoria_producto.id'), nullable=False)
    categoria_producto = relationship('CategoriaProducto')

    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria', back_populates='productos')

    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    tipo_item = relationship('TipoItem')

    # Campo de calificación de producto
    calificacion = Column(Float, default=0.0)  # Calificación de 0 a 5

# Clase ComboMenu
class ComboMenu(Base):
    __tablename__ = 'combo_menu'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    precio = Column(Integer, nullable=False)

    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria')

    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    tipo_item = relationship('TipoItem')

    productos = relationship('Producto', secondary='detalle_combo_menu')

# Tabla intermedia ComboMenu-Producto
detalle_combo_menu = Table('detalle_combo_menu', Base.metadata,
    Column('combo_menu_id', Integer, ForeignKey('combo_menu.id'), primary_key=True),
    Column('producto_id', Integer, ForeignKey('producto.id'), primary_key=True)
)

# Clase Cafetería
class Cafeteria(Base):
    __tablename__ = 'cafeteria'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    direccion = Column(String(255), nullable=False)

    comuna_id = Column(Integer, ForeignKey('comuna.id'), nullable=False)
    comuna = relationship('Comuna')

    usuarios = relationship('Usuario')  
    productos = relationship('Producto', back_populates='cafeteria')  
    combos = relationship('ComboMenu')  

# Clase TipoItem
class TipoItem(Base):
    __tablename__ = 'tipo_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)

# Clase Venta
class Venta(Base):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    monto_total = Column(Integer, nullable=False)
    estado = Column(String(50), nullable=False, default="pendiente")
    comentarios = Column(Text, nullable=True)
    
    usuario_id = Column(Integer, ForeignKey('usuario.id'), nullable=False)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)

    usuario = relationship('Usuario')
    cafeteria = relationship('Cafeteria')
    detalles = relationship('DetalleVenta', back_populates='venta')

# Clase DetalleVenta
class DetalleVenta(Base):
    __tablename__ = 'detalle_venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)
    item_id = Column(Integer, nullable=False)
    tipo_item_id = Column(Integer, ForeignKey('tipo_item.id'), nullable=False)
    tipo_item = relationship('TipoItem')

    cantidad = Column(Integer, nullable=False)
    precio_unitario = Column(Integer, nullable=False)
    
    venta = relationship('Venta', back_populates='detalles')

# Configurar conexión a la base de datos
# engine = create_engine('postgresql://usuario:password@localhost:5432/mi_base_de_datos')
# Base.metadata.create_all(engine)

# Dibujar el diagrama
render_er(Base, 'diagrama_cafeteria.png')
