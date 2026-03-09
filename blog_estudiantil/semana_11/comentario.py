# comentario.py - Módulo que define la clase Comentario para el Blog Estudiantil
# Esta clase representa un comentario en un artículo del blog
# Implementa métodos getter y setter para acceder y modificar estos atributos (POO)

class Comentario:
    """Clase que representa un comentario en el blog estudiantil.

    Atributos:
        id (int): Identificador único del comentario en la base de datos
        articulo_id (int): ID del artículo al que pertenece el comentario
        autor (str): Nombre del autor del comentario
        contenido (str): Contenido del comentario
        fecha_comentario (str): Fecha del comentario (formato ISO)
    """

    def __init__(self, id=None, articulo_id=None, autor="", contenido="", fecha_comentario=None):
        """Inicializa un comentario del blog estudiantil.

        Args:
            id: Identificador único (asignado por BD, None para comentarios nuevos)
            articulo_id: ID del artículo al que pertenece
            autor: Nombre del autor del comentario
            contenido: Contenido del comentario
            fecha_comentario: Fecha del comentario (None para usar fecha actual)
        """
        self.id = id
        self.articulo_id = articulo_id
        self.autor = autor
        self.contenido = contenido
        self.fecha_comentario = fecha_comentario

    # Getters
    def get_id(self):
        """Retorna el ID único del comentario."""
        return self.id

    def get_articulo_id(self):
        """Retorna el ID del artículo al que pertenece el comentario."""
        return self.articulo_id

    def get_autor(self):
        """Retorna el nombre del autor del comentario."""
        return self.autor

    def get_contenido(self):
        """Retorna el contenido del comentario."""
        return self.contenido

    def get_fecha_comentario(self):
        """Retorna la fecha del comentario."""
        return self.fecha_comentario

    # Setters
    def set_articulo_id(self, articulo_id):
        """Establece el ID del artículo."""
        self.articulo_id = articulo_id

    def set_autor(self, autor):
        """Establece el nombre del autor del comentario."""
        self.autor = autor

    def set_contenido(self, contenido):
        """Establece el contenido del comentario."""
        self.contenido = contenido

    def set_fecha_comentario(self, fecha_comentario):
        """Establece la fecha del comentario."""
        self.fecha_comentario = fecha_comentario

    def __str__(self):
        """Retorna una representación legible del comentario."""
        return f"Comentario(ID: {self.id}, Artículo: {self.articulo_id}, Autor: {self.autor})"

    def __repr__(self):
        """Retorna una representación técnica del comentario."""
        return f"Comentario({self.id}, articulo_id={self.articulo_id}, '{self.autor}')"