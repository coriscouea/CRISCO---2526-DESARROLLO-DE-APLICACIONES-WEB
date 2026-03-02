# inventario.py - Módulo para manejar el inventario de productos.
# Define la clase Inventario, que gestiona una colección de productos.

from semana_11.producto import Producto
from bd import crear_conexion

class Inventario:
    def __init__(self): # El inventario se inicializa con un diccionario vacío para almacenar los productos, donde la clave es el ID del producto y el valor es la instancia del producto.
        self.productos = {}

    def cargar_desde_db(self, lista_productos):
        self.productos.clear()
        for p in lista_productos:
            producto = Producto(p[0], p[1], p[2], p[3]) # Crear instancia de Producto con los datos de la base de datos
            self.productos[p[0]] = producto

    def agregar_producto(self, producto):
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)", 
                       (producto.nombre, producto.cantidad, float(producto.precio))) # Insertar nuevo producto en la base de datos
        conexion.commit()
        producto.id = cursor.lastrowid
        self.productos[producto.id] = producto
        conexion.close()

    def eliminar_producto(self, id):
        if id in self.productos:
            del self.productos[id]
        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("DELETE FROM productos WHERE id=?", (id,))
        conexion.commit()
        conexion.close()

    def buscar_por_nombre(self, nombre):
        return [p for p in self.productos.values() if nombre.lower() in p.nombre.lower()]

    def mostrar_todos(self): # Retorna una lista de todos los productos en el inventario
        return list(self.productos.values())