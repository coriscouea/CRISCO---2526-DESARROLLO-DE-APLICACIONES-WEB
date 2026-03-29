# Configuración de la base de datos MySQL
# Usamos mysql+mysqlconnector para conectar con MySQL

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# URL de conexión a MySQL
# Formato: mysql+mysqlconnector://usuario:password@host/nombre_base_datos
mysql_url = 'mysql+mysqlconnector://root:123456@localhost/blog_estudiantil'

# Crear engine de SQLAlchemy para MySQL
engine = create_engine(mysql_url, echo=False, pool_pre_ping=True)

""" 
    Motor de SQLAlchemy: echo=False oculta los logs de SQL en consola. 
    pool_pre_ping=True es genial: verifica si la conexión sigue viva antes de 
    usarla (evita el error "MySQL server has gone away").
    
"""

# Crear sesión
Session = sessionmaker(bind=engine)

""" 
    Fábrica de Sesiones: No es la sesión en sí, sino una "plantilla" 
    para crear sesiones cuando las necesitemos.

""" 


def init_db():
    '''Inicializa la base de datos creando todas las tablas.
    
    Utiliza SQLAlchemy para crear las tablas automáticamente
    si no existen en la base de datos MySQL.
    '''
    from semana_11.modelos import Base
    Base.metadata.create_all(engine)

def crear_sesion():
    '''Crea y retorna una nueva sesión de SQLAlchemy.
    
    Returns:
        Session: Nueva sesión conectada a la base de datos
    '''
    return Session()
