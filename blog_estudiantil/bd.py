# bd.py - Módulo de Base de Datos para el Blog Estudiantil
# Gestiona la conexión y estructura de datos SQLite utilizando SQLAlchemy
# Implementa funciones para inicializar la BD y crear sesiones persistentes

from semana_11.modelos import init_db as crear_tablas, crear_sesion, engine

def crear_conexion():
    """Crea y retorna una conexión a la base de datos SQLite del blog.

    Retorna una sesión de SQLAlchemy para realizar operaciones en la BD.
    Esta función mantiene compatibilidad con código existente que usaba sqlite3.

    Returns:
        Session: Sesión de SQLAlchemy conectada a la base de datos
    """
    return crear_sesion()

def init_db():
    """Inicializa la estructura de la base de datos del blog.

    Utiliza SQLAlchemy para crear las tablas necesarias para el blog estudiantil:
    - autores: información de los autores
    - articulos: artículos publicados
    - comentarios: comentarios en los artículos

    Se ejecuta automáticamente al iniciar la aplicación.
    """
    # Importar los modelos para que SQLAlchemy los reconozca
    from semana_11.modelos import Autor, Articulo, Comentario
    
    # Crear todas las tablas
    crear_tablas()
    
    print("✓ Base de datos inicializada con SQLAlchemy")
    print(f"  - Engine: {engine.url}")
    print(f"  - Tablas creadas: autores, articulos, comentarios")

