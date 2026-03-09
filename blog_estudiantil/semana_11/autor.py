# autor.py - Módulo que define la clase Autor para el Blog Estudiantil
# Esta clase representa un autor del blog con atributos: ID, nombre, email, bio
# Implementa métodos getter y setter para acceder y modificar estos atributos (POO)

class Autor:
    """Clase que representa un autor en el blog estudiantil.

    Atributos:
        id (int): Identificador único del autor en la base de datos
        nombre (str): Nombre completo del autor
        email (str): Correo electrónico único del autor
        bio (str): Biografía breve del autor
        fecha_registro (str): Fecha de registro (formato ISO)
    """

    def __init__(self, id=None, nombre="", email="", bio="", fecha_registro=None):
        """Inicializa un autor del blog estudiantil.

        Args:
            id: Identificador único (asignado por BD, None para autores nuevos)
            nombre: Nombre completo del autor
            email: Correo electrónico único
            bio: Biografía breve
            fecha_registro: Fecha de registro (None para usar fecha actual)
        """
        self.id = id
        self.nombre = nombre
        self.email = email
        self.bio = bio
        self.fecha_registro = fecha_registro

    # Getters
    def get_id(self):
        """Retorna el ID único del autor."""
        return self.id

    def get_nombre(self):
        """Retorna el nombre del autor."""
        return self.nombre

    def get_email(self):
        """Retorna el email del autor."""
        return self.email

    def get_bio(self):
        """Retorna la biografía del autor."""
        return self.bio

    def get_fecha_registro(self):
        """Retorna la fecha de registro del autor."""
        return self.fecha_registro

    # Setters
    def set_nombre(self, nombre):
        """Establece el nombre del autor."""
        self.nombre = nombre

    def set_email(self, email):
        """Establece el email del autor."""
        self.email = email

    def set_bio(self, bio):
        """Establece la biografía del autor."""
        self.bio = bio

    def set_fecha_registro(self, fecha_registro):
        """Establece la fecha de registro del autor."""
        self.fecha_registro = fecha_registro

    def __str__(self):
        """Retorna una representación legible del autor."""
        return f"Autor(ID: {self.id}, Nombre: {self.nombre}, Email: {self.email})"

    def __repr__(self):
        """Retorna una representación técnica del autor."""
        return f"Autor({self.id}, '{self.nombre}', '{self.email}')"