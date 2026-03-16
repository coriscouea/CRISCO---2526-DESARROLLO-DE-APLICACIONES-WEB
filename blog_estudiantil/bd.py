# bd.py - Módulo de gestión de la base de datos para el Blog Estudiantil

from Conexión.conexion import init_db as crear_tablas, crear_sesion, engine

def crear_conexion():
    """Crea y retorna una conexión a la base de datos MySQL del blog.

    Retorna una sesión de SQLAlchemy para realizar operaciones en la BD.
    Esta función mantiene compatibilidad con código existente.

    Returns:
        Session: Sesión de SQLAlchemy conectada a la base de datos
    """
    return crear_sesion()

def init_db():
    """Inicializa la estructura de la base de datos del blog.

    Utiliza SQLAlchemy para crear las tablas necesarias para el blog estudiantil:
    - autores: información de los autores
    - artículos: artículos publicados
    - comentarios: comentarios en los artículos

    Se ejecuta automáticamente al iniciar la aplicación.
    """
    # Importar los modelos para que SQLAlchemy los reconozca
    from semana_11.modelos import Autor, Articulo, Comentario
    
    # Crear todas las tablas
    crear_tablas()


