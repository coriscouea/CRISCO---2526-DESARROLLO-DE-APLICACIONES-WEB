# app.py - Archivo principal de la aplicación Flask para el Blog Estudiantil
# Configura rutas, maneja la lógica de negocio y conecta con la base de datos MySQL utilizando SQLAlchemy.
# Implementa funcionalidades para publicar artículos, registrar autores, agregar comentarios y editar contenido.
# Utiliza WTForms para formularios con validación y Jinja2 para renderizar plantillas HTML dinámicas.

from flask import Flask, render_template, request, redirect, url_for, flash
from sqlalchemy import text
from semana_11.form import ArticuloForm, AutorForm, ComentarioForm, LoginForm, RegisterForm
from semana_11.blog import Blog 
from semana_11.articulo import Articulo
from semana_11.autor import Autor
from semana_11.comentario import Comentario
from bd import crear_conexion, init_db, get_usuario_by_id, verificar_credenciales, crear_usuario
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

# Configuración de la aplicación Flask para Blog Estudiantil
app = Flask(__name__)
app.config['SECRET_KEY'] = 'blog_estudiantil_clave_segura_2026'  # Cambiar en producción

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return get_usuario_by_id(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('ver_blog'))
    form = RegisterForm()
    if form.validate_on_submit():
        password_hash = generate_password_hash(form.password.data)
        if crear_usuario(form.usuario.data, form.email.data, password_hash):
            flash('Registro exitoso. Por favor inicia sesión.', 'success')
            return redirect(url_for('login'))
        flash('Error al registrar usuario.', 'error')
    return render_template('auth/register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('ver_blog'))
    form = LoginForm()
    if form.validate_on_submit():
        user = verificar_credenciales(form.identifier.data, form.password.data)
        login_user(user)
        return redirect(url_for('ver_blog'))
    return render_template('auth/login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada.', 'info')
    return redirect(url_for('inicio'))

#-----------SEMANA 10 - RUTAS BÁSICAS DEL BLOG-----------

@app.route("/")
def inicio():
    """Página principal / Inicio del blog estudiantil."""
    return render_template("semana_10/contenido/index.html")

@app.route("/about")
def acerca_de():
    """Página con información sobre el blog estudiantil."""
    return render_template("semana_10/contenido/about.html")

@app.route("/autores")
def autores():
    """Página que muestra la lista de autores registrados en el blog estudiantil."""
    from semana_11.modelos import Autor
    session = crear_conexion()
    try:
        lista = session.query(Autor).all()
    finally:
        session.close()
    return render_template("semana_10/contenido/autores.html", autores=lista)

#-----------SEMANA 11 - GESTIÓN DEL BLOG ESTUDIANTIL-----------

# Inicializar base de datos al arrancar la aplicación
init_db()

# Instancia global del blog
blog = Blog()

@app.route("/nuevo_articulo", methods=["GET", "POST"])
@login_required 
def nuevo_articulo():
    """Formulario WTForms para publicar artículos en el blog con validación.

    GET: Muestra el formulario vacío
    POST: Procesa la validación y publica el artículo en la BD
    """
    form = ArticuloForm()
    if form.validate_on_submit():
        # Obtener el autor_id y convertirlo a entero
        autor_id = int(form.autor_id.data)
        
        # Validar que se haya seleccionado un autor válido
        if autor_id == 0:
            flash("Debe seleccionar un autor válido", "error")
            return render_template("semana_11/inventario/form.html", form=form)
        
        # Crear instancia de artículo con datos del formulario
        nuevo_articulo = Articulo(None, form.titulo.data, form.contenido.data, autor_id)
        # Publicar en BD y actualizar blog
        blog.publicar_articulo(nuevo_articulo)
        flash(f"Artículo publicado exitosamente: {nuevo_articulo.titulo}", "success")
        return redirect(url_for('ver_blog'))
    return render_template("semana_11/inventario/form.html", form=form)

@app.route('/blog')
def ver_blog():
    """Muestra todos los artículos publicados en el blog estudiantil.

    Carga todos los artículos de la BD MySQL y los muestra en la página principal del blog."""
    # Cargar datos desde BD
    blog.cargar_desde_db()
    articulos = blog.mostrar_todos_articulos()
    return render_template('semana_11/inventario/inventario.html', articulos=articulos)

@app.route('/articulo/<int:id>')
def ver_articulo(id):
    """Muestra un artículo específico con sus comentarios.

    Args:
        id: ID del artículo a mostrar
    """
    # Cargar datos desde BD
    blog.cargar_desde_db() # Asegura que los datos estén actualizados antes de obtener el artículo
    articulo = blog.obtener_articulo(id)
    if not articulo:
        flash("Artículo no encontrado", "error")
        return redirect(url_for('ver_blog'))

    comentarios = blog.obtener_comentarios_articulo(id)
    autor = blog.obtener_autor(articulo.autor_id) if articulo.autor_id else None

    return render_template('semana_11/inventario/ver_articulo.html',
                          articulo=articulo, comentarios=comentarios, autor=autor)


@app.route('/buscar_articulo', methods=['POST'])
def buscar_articulo():
    """Busca artículos en el blog por título (búsqueda case-insensitive).

    POST: Recibe término de búsqueda y retorna artículos coincidentes"""
    titulo = request.form.get('titulo', '')
    articulos = blog.buscar_articulos_por_titulo(titulo)
    if not articulos:
        flash(f"No se encontraron artículos con '{titulo}'", "warning")
    return render_template('semana_11/inventario/inventario.html', articulos=articulos)

@app.route('/nuevo_autor', methods=["GET", "POST"])
@login_required
def nuevo_autor():
    """Formulario WTForms para registrar nuevos autores en el blog con validación.

    GET: Muestra el formulario vacío
    POST: Procesa la validación y registra el autor en la BD
    """
    form = AutorForm()
    if form.validate_on_submit():
        # Crear instancia de autor con datos del formulario
        nuevo_autor = Autor(None, form.nombre.data, form.email.data, form.bio.data)
        # Registrar en BD y actualizar blog
        blog.agregar_autor(nuevo_autor)
        flash(f"Autor registrado exitosamente: {nuevo_autor.nombre}", "success")
        return redirect(url_for('autores'))
    return render_template("semana_11/inventario/agregar.html", form=form)

@app.route('/agregar_comentario', methods=['POST'])
def agregar_comentario():
    """Agrega un comentario a un artículo del blog.

    POST: Recibe datos del comentario y lo agrega a la BD"""
    autor = request.form['autor']
    contenido = request.form['contenido']
    articulo_id = request.form['articulo_id']

    # Crear y agregar comentario
    nuevo_comentario = Comentario(None, int(articulo_id), autor, contenido)
    blog.agregar_comentario(nuevo_comentario)
    flash("Comentario agregado exitosamente", "success")
    return redirect(url_for('ver_articulo', id=articulo_id))

@app.route('/eliminar_comentario/<int:id>')
@login_required
def eliminar_comentario(id):
    """Elimina un comentario del blog y su BD.

    Args:
        id: ID del comentario a eliminar"""
    # Obtener artículo_id antes de eliminar para redireccionar
    blog.cargar_desde_db()
    comentario = blog.comentarios.get(id)
    articulo_id = comentario.articulo_id if comentario else None

    blog.eliminar_comentario(id)
    flash("Comentario eliminado", "success")
    return redirect(url_for('ver_articulo', id=articulo_id) if articulo_id else url_for('ver_blog'))


@app.route("/editar_articulo/<int:id>", methods=["GET", "POST"])
@login_required
def editar_articulo(id):
    """Edita los datos de un artículo en el blog.

    GET: Muestra formulario con datos actuales del artículo
    POST: Actualiza el artículo en BD usando SQLAlchemy"""
    from semana_11.modelos import Articulo
    
    blog.cargar_desde_db()
    articulo = blog.obtener_articulo(id)

    if not articulo:
        flash("Artículo no encontrado", "error")
        return redirect(url_for("ver_blog"))

    if request.method == "POST":
        titulo = request.form["titulo"]
        contenido = request.form["contenido"]

        # Actualizar artículo usando SQLAlchemy
        session = crear_conexion()
        try:
            articulo_db = session.query(Articulo).filter(Articulo.id == id).first()
            if articulo_db:
                articulo_db.titulo = titulo
                articulo_db.contenido = contenido
                session.commit()
            
            # Actualizar en memoria
            articulo.titulo = titulo
            articulo.contenido = contenido
            
            flash("Artículo actualizado correctamente", "success")
        except Exception as e:
            session.rollback()
            flash(f"Error al actualizar: {str(e)}", "error")
        finally:
            session.close()
            
        return redirect(url_for("ver_articulo", id=id))

    # GET: Mostrar formulario con datos actuales
    return render_template("semana_11/inventario/editar.html", articulo=articulo)


@app.route("/editar_autor/<int:id>", methods=["GET", "POST"])
@login_required
def editar_autor(id):
    """Edita los datos de un autor en el blog.

    GET: Muestra formulario con datos actuales del autor
    POST: Actualiza el autor en BD usando SQLAlchemy"""
    from semana_11.modelos import Autor
    
    blog.cargar_desde_db()
    autor = blog.obtener_autor(id)

    if not autor:
        flash("Autor no encontrado", "error")
        return redirect(url_for("autores"))

    if request.method == "POST":
        nombre = request.form["nombre"]
        email = request.form["email"]
        bio = request.form["bio"] or None

        # Actualizar autor usando SQLAlchemy
        session = crear_conexion()
        try:
            autor_db = session.query(Autor).filter(Autor.id == id).first()
            if autor_db:
                autor_db.nombre = nombre
                autor_db.email = email
                autor_db.bio = bio
                session.commit()
            
            # Actualizar en memoria
            autor.nombre = nombre
            autor.email = email
            autor.bio = bio
            
            flash("Autor actualizado correctamente", "success")
            blog.cargar_desde_db()
        except Exception as e:
            session.rollback()
            flash(f"Error al actualizar: {str(e)}", "error")
        finally:
            session.close()
            
        return redirect(url_for("autores"))

    # GET: Mostrar formulario con datos actuales
    return render_template("semana_10/contenido/editar_autor.html", autor=autor)

@app.route('/eliminar_autor/<int:id>')
@login_required
def eliminar_autor(id):
    """Elimina un autor (cascade artículos)."""
    
    from semana_11.modelos import Autor
    session = crear_conexion()

    try:   
        autor = session.query(Autor).filter(Autor.id == id).first()  
        if autor:         
            session.delete(autor)        
            session.commit()         
            flash('Autor eliminado', 'success')
        else:   
            flash('Autor no encontrado')
    except Exception as e:
        session.rollback()    
        flash(f'Error: {str(e)}') 
    finally:    
        session.close()
    return redirect(url_for('autores'))

@app.route('/eliminar_articulo/<int:id>', methods=['POST'])
@login_required
def eliminar_articulo(id):
    """Elimina un artículo del blog y su BD.

    Args:
        id: ID del artículo a eliminar"""
    
    from semana_11.modelos import Articulo
    session = crear_conexion()
    try:   
        articulo = session.query(Articulo).filter(Articulo.id == id).first()  
        if articulo:         
            session.delete(articulo)        
            session.commit()         
            flash('Artículo eliminado', 'success')
        else:   
            flash('Artículo no encontrado')
    except Exception as e:
        session.rollback()    
        flash(f'Error: {str(e)}') 
    finally:    
        session.close()
    return redirect(url_for('ver_blog'))

if __name__ == "__main__":
    app.run(debug=True)