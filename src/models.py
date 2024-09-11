import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Date, Time, Table, Text, Float, Boolean
from sqlalchemy.orm import relationship, declarative_base
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
    Column('usuario_id', Integer, ForeignKey('usuario.rut'), primary_key=True),
    Column('beneficio_id', Integer, ForeignKey('beneficio.id'), primary_key=True)
)

# Clase Usuario (funcionarios del café)
class Usuario(Base):
    __tablename__ = 'usuario'
    rut = Column(String(12), primary_key=True)  # Ahora el rut es el ID primario
    nombre = Column(String(100), nullable=False)
    apellido_paterno = Column(String(100), nullable=False)
    apellido_materno = Column(String(100), nullable=False)
    
    usuario = Column(String(50), unique=True, nullable=False)  
    correo = Column(String(100), unique=True, nullable=False)  
    contrasena = Column(String(255), nullable=False)  

    rol_id = Column(Integer, ForeignKey('rol.id'), nullable=False)
    rol = relationship('Rol')

    beneficios = relationship('Beneficio', secondary=usuario_beneficio)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria')

# Nueva tabla Cliente
class Cliente(Base):
    __tablename__ = 'cliente'
    rut = Column(String(12), primary_key=True)  # El rut es el ID primario
    nombre = Column(String(100), nullable=False)
    correo = Column(String(100), unique=True, nullable=False)  
    contrasena = Column(String(255), nullable=False)  
    usuario = Column(String(50), unique=True, nullable=False)

    # Relación con favoritos e historial de pedidos
    favoritos = relationship('Favoritos')
    historial_pedidos = relationship('HistorialPedidos')

# Nueva tabla Favoritos
class Favoritos(Base):
    __tablename__ = 'favoritos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)

# Nueva tabla HistorialPedidos
class HistorialPedidos(Base):
    __tablename__ = 'historial_pedidos'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    venta_id = Column(Integer, ForeignKey('venta.id'), nullable=False)
    fecha = Column(Date, nullable=False)

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

# Nueva tabla Mesa
class Mesa(Base):
    __tablename__ = 'mesa'
    id = Column(Integer, primary_key=True, autoincrement=True)
    numero = Column(Integer, nullable=False)
    qr_code = Column(String(255), nullable=False)  # Código QR (puede ser un URL o datos del QR)
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    cafeteria = relationship('Cafeteria')

# Modificación de la clase Venta para incluir relación con Mesero y Mesa
class Venta(Base):
    __tablename__ = 'venta'
    id = Column(Integer, primary_key=True, autoincrement=True)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    monto_total = Column(Integer, nullable=False)
    estado = Column(String(50), nullable=False, default="pendiente")
    comentarios = Column(Text, nullable=True)
    
    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)  # Relacionado con Cliente
    cafeteria_id = Column(Integer, ForeignKey('cafeteria.id'), nullable=False)
    mesero_rut = Column(String(12), ForeignKey('usuario.rut'), nullable=True)  # Relación con el Mesero (opcional)
    mesa_id = Column(Integer, ForeignKey('mesa.id'), nullable=True)  # Relación con la Mesa (opcional)

    cliente = relationship('Cliente')
    cafeteria = relationship('Cafeteria')
    mesero = relationship('Usuario')  # Relacionado con el mesero
    mesa = relationship('Mesa')  # Relacionado con la mesa

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

class CalificacionProducto(Base):
    __tablename__ = 'calificacion_producto'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_rut = Column(String(12), ForeignKey('cliente.rut'), nullable=False)
    producto_id = Column(Integer, ForeignKey('producto.id'), nullable=False)
    calificacion = Column(Float, nullable=False)  # Rango de 0 a 5, por ejemplo
    fecha = Column(Date, nullable=False)  # Fecha en que se realizó la calificación

    cliente = relationship('Cliente')
    producto = relationship('Producto')    



# Dibujar el diagrama
render_er(Base, 'diagrama_cafeteria.png')
