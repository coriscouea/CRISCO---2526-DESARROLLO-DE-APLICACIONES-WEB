# modelos.py - Modelos SQLAlchemy para el Blog Estudiantil
# Define las clases de modelo usando SQLAlchemy ORM para persistencia de datos
# Proporciona una capa de abstracción sobre la base de datos SQLite

from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from datetime import datetime

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


# Configuración de la base de datos
import os
from pathlib import Path

# Ruta de la base de datos
db_path = Path(__file__).parent / "almacenamiento" / "blog.db"
db_url = f'sqlite:///{db_path}'

# Crear engine de SQLAlchemy
engine = create_engine(db_url, echo=False)

# Crear sesión
Session = sessionmaker(bind=engine)


def init_db():
    """Inicializa la base de datos creando todas las tablas.
    
    Utiliza SQLAlchemy para crear las tablas automáticamente
    si no existen en la base de datos SQLite.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    Base.metadata.create_all(engine)


def crear_sesion():
    """Crea y retorna una nueva sesión de SQLAlchemy.
    
    Returns:
        Session: Nueva sesión conectada a la base de datos
    """
    return Session()

