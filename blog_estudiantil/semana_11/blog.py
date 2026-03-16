# blog.py - Módulo para la gestión del Blog Estudiantil
# Define la clase Blog que utiliza SQLAlchemy para gestionar artículos, autores y comentarios
# Implementa operaciones CRUD sincronizadas con la base de datos MySQL usando SQLAlchemy ORM

from semana_11.modelos import Autor, Articulo, Comentario, crear_sesion
from semana_11.articulo import Articulo as ArticuloOriginal
from semana_11.autor import Autor as AutorOriginal
from semana_11.comentario import Comentario as ComentarioOriginal

class Blog:
    """Clase que gestiona el blog estudiantil.

    Utiliza SQLAlchemy para todas las operaciones de base de datos,
    manteniendo compatibilidad con las clases originales del proyecto.
    """

    def __init__(self):
        """Inicializa el blog."""
        self.articulos = {}
        self.autores = {}
        self.comentarios = {}

    def cargar_desde_db(self):
        """Carga todos los datos del blog desde la base de datos MySQL usando SQLAlchemy.

        Carga artículos, autores y comentarios en los diccionarios en memoria.
        """
        session = crear_sesion()
        
        try:
            # Cargar autores
            self.autores.clear()
            autores_db = session.query(Autor).all()
            for autor_db in autores_db:
                autor = AutorOriginal(
                    autor_db.id,
                    autor_db.nombre,
                    autor_db.email,
                    autor_db.bio,
                    autor_db.fecha_registro
                )
                self.autores[autor_db.id] = autor

            # Cargar artículos
            self.articulos.clear()
            articulos_db = session.query(Articulo).all()
            for articulo_db in articulos_db:
                articulo = ArticuloOriginal(
                    articulo_db.id,
                    articulo_db.titulo,
                    articulo_db.contenido,
                    articulo_db.autor_id,
                    articulo_db.fecha_publicacion
                )
                self.articulos[articulo_db.id] = articulo

            # Cargar comentarios
            self.comentarios.clear()
            comentarios_db = session.query(Comentario).all()
            for comentario_db in comentarios_db:
                comentario = ComentarioOriginal(
                    comentario_db.id,
                    comentario_db.articulo_id,
                    comentario_db.autor,
                    comentario_db.contenido,
                    comentario_db.fecha_comentario
                )
                self.comentarios[comentario_db.id] = comentario
        finally:
            session.close()

    # CRUD para Autores
    def agregar_autor(self, autor):
        """Agrega un nuevo autor al blog y lo persiste en BD usando SQLAlchemy.

        Args:
            autor (AutorOriginal): Instancia del autor a agregar

        Returns:
            int: ID asignado por la base de datos al nuevo autor
        """
        session = crear_sesion()
        try:
            # Crear nuevo autor en la base de datos
            nuevo_autor = Autor(
                nombre=autor.nombre,
                email=autor.email,
                bio=autor.bio
            )
            session.add(nuevo_autor)
            session.commit()
            
            # Actualizar el ID en el objeto original
            autor.id = nuevo_autor.id
            self.autores[autor.id] = autor
            
            return autor.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def obtener_autor(self, id):
        """Obtiene un autor por su ID.

        Args:
            id (int): ID del autor

        Returns:
            AutorOriginal or None: El autor encontrado o None si no existe
        """
        return self.autores.get(id)

    # CRUD para Artículos
    def publicar_articulo(self, articulo):
        """Publica un nuevo artículo en el blog y lo persiste en BD usando SQLAlchemy.

        Args:
            articulo (ArticuloOriginal): Instancia del artículo a publicar

        Returns:
            int: ID asignado por la base de datos al nuevo artículo
        """
        session = crear_sesion()
        try:
            # Crear nuevo artículo en la base de datos
            nuevo_articulo = Articulo(
                titulo=articulo.titulo,
                contenido=articulo.contenido,
                autor_id=articulo.autor_id
            )
            session.add(nuevo_articulo)
            session.commit()
            
            # Actualizar el ID en el objeto original
            articulo.id = nuevo_articulo.id
            self.articulos[articulo.id] = articulo
            
            return articulo.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def obtener_articulo(self, id):
        """Obtiene un artículo por su ID.

        Args:
            id (int): ID del artículo

        Returns:
            ArticuloOriginal or None: El artículo encontrado o None si no existe
        """
        return self.articulos.get(id)

    def buscar_articulos_por_titulo(self, titulo):
        """Busca artículos por coincidencia de título (búsqueda case-insensitive).

        Args:
            titulo (str): Término de búsqueda

        Returns:
            list: Lista de artículos que coinciden con el criterio
        """
        return [a for a in self.articulos.values() if titulo.lower() in a.titulo.lower()]

    def obtener_articulos_por_autor(self, autor_id):
        """Obtiene todos los artículos de un autor específico.

        Args:
            autor_id (int): ID del autor

        Returns:
            list: Lista de artículos del autor
        """
        return [a for a in self.articulos.values() if a.autor_id == autor_id]

    def mostrar_todos_articulos(self):
        """Retorna todos los artículos publicados en el blog.

        Returns:
            list: Lista de todas las instancias de Articulo ordenadas por fecha (más recientes primero)
        """
        return sorted(self.articulos.values(), key=lambda x: x.fecha_publicacion or "", reverse=True)

    # CRUD para Comentarios
    def agregar_comentario(self, comentario):
        """Agrega un nuevo comentario a un artículo y lo persiste en BD usando SQLAlchemy.

        Args:
            comentario (ComentarioOriginal): Instancia del comentario a agregar

        Returns:
            int: ID asignado por la base de datos al nuevo comentario
        """
        session = crear_sesion()
        try:
            # Crear nuevo comentario en la base de datos
            nuevo_comentario = Comentario(
                articulo_id=comentario.articulo_id,
                autor=comentario.autor,
                contenido=comentario.contenido
            )
            session.add(nuevo_comentario)
            session.commit()
            
            # Actualizar el ID en el objeto original
            comentario.id = nuevo_comentario.id
            self.comentarios[comentario.id] = comentario
            
            return comentario.id
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def obtener_comentarios_articulo(self, articulo_id):
        """Obtiene todos los comentarios de un artículo específico.

        Args:
            articulo_id (int): ID del artículo

        Returns:
            list: Lista de comentarios del artículo ordenados por fecha
        """
        comentarios_articulo = [c for c in self.comentarios.values() if c.articulo_id == articulo_id]
        return sorted(comentarios_articulo, key=lambda x: x.fecha_comentario or "")

    def eliminar_comentario(self, id):
        """Elimina un comentario del blog y de la BD usando SQLAlchemy.

        Args:
            id (int): ID del comentario a eliminar

        Returns:
            bool: True si fue eliminado, False si no existía
        """
        session = crear_sesion()
        try:
            # Eliminar de la base de datos
            comentario = session.query(Comentario).filter(Comentario.id == id).first()
            if comentario:
                session.delete(comentario)
                session.commit()
            
            # Eliminar de memoria
            if id in self.comentarios:
                del self.comentarios[id]
                
            return True
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

