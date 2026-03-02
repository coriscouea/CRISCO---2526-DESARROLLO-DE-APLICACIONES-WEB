# app.py - Archivo principal de la aplicación Flask para el blog estudiantil.
# Este archivo define las rutas, la lógica de negocio y la interacción con la 
# base de datos para el módulo de inventario de productos. 
# Utiliza WTForms para manejar formularios y SQLite para


from flask import Flask, render_template, request, redirect, url_for, flash
from semana_11.form import ProductoForm
from semana_11.inventario import Inventario
from semana_11.producto import Producto
from bd import crear_conexion, init_db

# Configuración de la aplicación Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tu_clave_secreta_aqui' # Clave secreta para sesiones y flash messages, debe ser segura en producción


#-----------SEMANA 10 - RUTAS BÁSICAS-----------

@app.route("/")
def inicio():
    return render_template("semana_10/contenido/index.html")

@app.route("/about")
def acerca_de():
    return render_template("semana_10/contenido/about.html")

@app.route("/productos")
def productos():
    return render_template("semana_10/contenido/productos.html")

@app.route("/clientes")
def clientes():
    return render_template("semana_10/contenido/clientes.html")


#-----------SEMANA 11 - INVENTARIO DE PRODUCTOS-----------

# Inicializar BD al arrancar
init_db()

inventario = Inventario()

@app.route("/form", methods=["GET", "POST"])
def form():
    form = ProductoForm()
    if form.validate_on_submit():
        nuevo_producto = Producto(None, form.nombre.data, form.cantidad.data, float(form.precio.data))
        inventario.agregar_producto(nuevo_producto)
        flash(f"Producto agregado exitosamente: {nuevo_producto.nombre}")
        return redirect(url_for('ver_inventario'))
    return render_template("semana_11/inventario/form.html", form=form)

@app.route('/inventario')
def ver_inventario():
    conexion = crear_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM productos")
    productos_db = cursor.fetchall() # Obtener todos los productos de la base de datos
    conexion.close()

    inventario.cargar_desde_db(productos_db)
    productos = inventario.mostrar_todos()
    return render_template('semana_11/inventario/inventario.html', productos=productos)

@app.route('/buscar', methods=['POST'])
def buscar():
    nombre = request.form.get('nombre', '')
    productos = inventario.buscar_por_nombre(nombre)
    if not productos:
        flash(f"No se encontraron productos con '{nombre}'")
    return render_template('semana_11/inventario/inventario.html', productos=productos)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    if request.method == 'POST':
        nombre = request.form['nombre']
        cantidad = request.form['cantidad']
        precio = request.form['precio']

        conexion = crear_conexion()
        cursor = conexion.cursor()
        cursor.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                       (nombre, cantidad, precio))
        conexion.commit()
        conexion.close()

        return redirect(url_for('ver_inventario'))
    return render_template('semana_11/inventario/agregar.html')

@app.route('/eliminar/<int:id>')
def eliminar(id):
    inventario.eliminar_producto(id)
    flash("Producto eliminado")
    return redirect(url_for('ver_inventario'))

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conexion = crear_conexion()
    cursor = conexion.cursor()

    if request.method == "POST":
        nombre = request.form["nombre"]
        cantidad = request.form["cantidad"]
        precio = request.form["precio"]

        cursor.execute("UPDATE productos SET nombre=?, cantidad=?, precio=? WHERE id=?",
                       (nombre, cantidad, precio, id))
        conexion.commit()
        conexion.close()
        return redirect(url_for("ver_inventario"))

    cursor.execute("SELECT * FROM productos WHERE id=?", (id,))
    producto = cursor.fetchone()
    conexion.close()
    return render_template("semana_11/inventario/editar.html", producto=producto)

if __name__ == "__main__":
    app.run(debug=True)