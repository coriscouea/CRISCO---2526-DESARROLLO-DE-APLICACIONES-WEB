# modelos.py - Definición de modelos SQLAlchemy para el Blog Estudiantil
# Define las clases Autor, Articulo y Comentario como modelos de SQLAlchemy para la base
# de datos MySQL del blog estudiantil. Cada clase representa una tabla en la base de datos
# con sus respectivas columnas, relaciones y métodos de representación. También incluye

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime
from Conexión.conexion import init_db, crear_sesion

# Crear base declarativa para los modelos
Base = declarative_base()

class Autor(Base):
    """Modelo SQLAlchemy para la tabla de autores del blog estudiantil.
    
    Atributos:
        id (int): Clave primaria, identificador único del autor
        nombre (str): Nombre completo del autor
        email (str): Correo electrónico único del autor
        bio (str): Biografía breve del autor
        fecha_registro (datetime): Fecha de registro automática
        articulos (list): Relación uno a muchos con artículos
    """
    __tablename__ = 'autores'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    bio = Column(Text, nullable=True)
    fecha_registro = Column(DateTime, default=datetime.now)
    
    # Relación uno a muchos con artículos
    articulos = relationship('Articulo', back_populates='autor', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Autor {self.nombre}>'
    
    def __str__(self):
        return f"Autor(ID: {self.id}, Nombre: {self.nombre}, Email: {self.email})"


class Articulo(Base):
    """Modelo SQLAlchemy para la tabla de artículos del blog estudiantil.
    
    Atributos:
        id (int): Clave primaria, identificador único del artículo
        titulo (str): Título del artículo
        contenido (str): Contenido completo del artículo
        autor_id (int): Clave foránea al autor
        fecha_publicacion (datetime): Fecha de publicación automática
        autor (Autor): Relación muchos a uno con autor
        comentarios (list): Relación uno a muchos con comentarios
    """
    __tablename__ = 'articulos'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String(200), nullable=False)
    contenido = Column(Text, nullable=False)
    autor_id = Column(Integer, ForeignKey('autores.id'), nullable=False)
    fecha_publicacion = Column(DateTime, default=datetime.now)
    
    # Relación muchos a uno con autor
    autor = relationship('Autor', back_populates='articulos')
    
    # Relación uno a muchos con comentarios
    comentarios = relationship('Comentario', back_populates='articulo', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Articulo {self.titulo}>'
    
    def __str__(self):
        return f"Artículo(ID: {self.id}, Título: {self.titulo}, Autor ID: {self.autor_id})"


class Comentario(Base):
    """Modelo SQLAlchemy para la tabla de comentarios del blog estudiantil.
    
    Atributos:
        id (int): Clave primaria, identificador único del comentario
        articulo_id (int): Clave foránea al artículo
        autor (str): Nombre del autor del comentario
        contenido (str): Contenido del comentario
        fecha_comentario (datetime): Fecha del comentario automática
        articulo (Articulo): Relación muchos a uno con artículo
    """
    __tablename__ = 'comentarios'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    articulo_id = Column(Integer, ForeignKey('articulos.id'), nullable=False)
    autor = Column(String(100), nullable=False)
    contenido = Column(Text, nullable=False)
    fecha_comentario = Column(DateTime, default=datetime.now)
    
    # Relación muchos a uno con artículo
    articulo = relationship('Articulo', back_populates='comentarios')
    
    def __repr__(self):
        return f'<Comentario {self.id} - {self.autor}>'
    
    def __str__(self):
        return f"Comentario(ID: {self.id}, Artículo: {self.articulo_id}, Autor: {self.autor})"




