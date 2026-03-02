# producto.py - Módulo que define la clase Producto, que representa un producto en el inventario.
# La clase Producto debe contener atributos como ID (único), nombre, cantidad y precio,

class Producto:
    def __init__(self, id=None ,nombre ="", cantidad=1, precio=0.0): # El constructor de la clase Producto permite crear una instancia con un ID opcional (que se asignará automáticamente al agregarlo a la base de datos), un nombre, una cantidad y un precio. Si no se proporcionan valores, se asignan valores predeterminados.
        self.id = id
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    # Getters
    def get_id(self):
        return self.id

    def get_nombre(self):
        return self.nombre

    def get_cantidad(self):
        return self.cantidad

    def get_precio(self):
        return self.precio

    # Setters
    def set_nombre(self, nombre):
        self.nombre = nombre

    def set_cantidad(self, cantidad):
        self.cantidad = cantidad

    def set_precio(self, precio):
        self.precio = precio

