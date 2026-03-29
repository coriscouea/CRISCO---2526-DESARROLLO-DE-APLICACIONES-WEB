# bd.py - Módulo de gestión de la base de datos para el Blog Estudiantil

from Conexión.conexion import init_db as crear_tablas, crear_sesion, engine
from werkzeug.security import check_password_hash
from semana_11.modelos import Usuario

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
    from semana_11.modelos import Autor, Articulo, Comentario, Usuario
    
    # Crear todas las tablas
    crear_tablas()

def get_usuario_by_id(user_id):
    """Obtiene usuario por ID para Flask-Login user_loader."""
    session = crear_sesion()
    try:
        usuario = session.query(Usuario).get(user_id) 
        """Consulta por ID: Es la forma más rápida de buscar un registro único."""
        
        return usuario
    finally:
        session.close()

def crear_usuario(usuario, email, password_hash):
    """Crea nuevo usuario con password hasheado."""
    session = crear_sesion()
    try:
        nuevo_usuario = Usuario(usuario=usuario, email=email, password=password_hash)
        session.add(nuevo_usuario)
        session.commit()
        return nuevo_usuario
    except Exception:

        session.rollback()
        """Seguridad de Datos: Si algo falla al crear un usuario, el rollback()
        deshace los cambios a medias, evitando datos corruptos."""

        return None
    finally:
        session.close()

def verificar_credenciales(identifier, password):
    """Verifica usuario por usuario o email, checkea password."""
    session = crear_sesion()
    try:
        usuario = session.query(Usuario).filter(
            (Usuario.usuario == identifier) | (Usuario.email == identifier)
        ).first()
        """Operador OR: Permite al estudiante loguearse con su 
        nombre de usuario o con su correo."""

        if usuario and check_password_hash(usuario.password, password):
            return usuario
        return None
    finally:
        session.close()

