# articulo.py - Módulo que define la clase Articulo para el Blog Estudiantil
# Esta clase representa un artículo del blog con atributos: ID, título, contenido, autor, fecha
# Implementa métodos getter y setter para acceder y modificar estos atributos (POO)

class Articulo:
    """Clase que representa un artículo en el blog estudiantil.

    Atributos:
        id (int): Identificador único del artículo en la base de datos
        titulo (str): Título del artículo
        contenido (str): Contenido completo del artículo
        autor_id (int): ID del autor que escribió el artículo
        fecha_publicacion (str): Fecha de publicación (formato ISO)
    """

    def __init__(self, id=None, titulo="", contenido="", autor_id=None, fecha_publicacion=None):
        """Inicializa un artículo del blog estudiantil.

        Args:
            id: Identificador único (asignado por BD, None para artículos nuevos)
            titulo: Título del artículo
            contenido: Contenido del artículo
            autor_id: ID del autor
            fecha_publicacion: Fecha de publicación (None para usar fecha actual)
        """
        self.id = id
        self.titulo = titulo
        self.contenido = contenido
        self.autor_id = autor_id
        self.fecha_publicacion = fecha_publicacion

    # Getters
    def get_id(self):
        """Retorna el ID único del artículo."""
        return self.id

    def get_titulo(self):
        """Retorna el título del artículo."""
        return self.titulo

    def get_contenido(self):
        """Retorna el contenido del artículo."""
        return self.contenido

    def get_autor_id(self):
        """Retorna el ID del autor del artículo."""
        return self.autor_id

    def get_fecha_publicacion(self):
        """Retorna la fecha de publicación del artículo."""
        return self.fecha_publicacion

    # Setters
    def set_titulo(self, titulo):
        """Establece el título del artículo."""
        self.titulo = titulo

    def set_contenido(self, contenido):
        """Establece el contenido del artículo."""
        self.contenido = contenido

    def set_autor_id(self, autor_id):
        """Establece el ID del autor del artículo."""
        self.autor_id = autor_id

    def set_fecha_publicacion(self, fecha_publicacion):
        """Establece la fecha de publicación del artículo."""
        self.fecha_publicacion = fecha_publicacion

    def __str__(self):
        """Retorna una representación legible del artículo."""
        return f"Artículo(ID: {self.id}, Título: {self.titulo}, Autor: {self.autor_id})"

    def __repr__(self):
        """Retorna una representación técnica del artículo."""
        return f"Articulo({self.id}, '{self.titulo}', autor_id={self.autor_id})"

