# bd.py - Módulo para manejar la base de datos SQLite del inventario de productos.
# Define funciones para crear la conexión a la base de datos y para inicializar la estructura de
# la base de datos, creando la tabla de productos si no existe. Utiliza el módulo sqlite3 de Python
# para interactuar con la base de datos y pathlib para manejar rutas de archivos de manera más segura y compatible entre sistemas operativos.

import sqlite3
from pathlib import Path

# Definir la ruta de la base de datos utilizando pathlib para asegurar compatibilidad entre sistemas operativos
db_path = Path(__file__).parent / "semana_11/almacenamiento" / "inventario.db"

# Función para crear una conexión a la base de datos SQLite
def crear_conexion():
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    return conn

def init_db():
    with crear_conexion() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL
            )
        """)
        conn.commit()