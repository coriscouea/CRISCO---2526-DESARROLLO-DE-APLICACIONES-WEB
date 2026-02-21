# Blog Estudiantil (proyecto individual)
# Aplicación Flask para un blog estudiantil con rutas estáticas y plantilla base.

from flask import Flask, render_template, request, redirect, url_for
# Importamos Flask para crear la aplicación, render_template para renderizar las plantillas HTML,
# request para manejar datos de formularios (si es necesario), redirect y url_for para redireccionar a otras rutas.

# Crear la instancia de la aplicación
app = Flask(__name__)

# ------------------------------------------------------------
# Ruta principal: muestra la página de inicio
# ------------------------------------------------------------

@app.route("/")
def inicio():
    # renderiza la plantilla index.html (que está en la carpeta "contenido").

    return render_template("contenido/index.html")

# ------------------------------------------------------------
# Ruta estática: muestra la página "Acerca de mí"
# ------------------------------------------------------------

@app.route("/about")
def acerca_de():
    # renderiza la plantilla about.html (en "contenido").
    
    return render_template("contenido/about.html")

# ------------------------------------------------------------
# Ruta estatica: muestra la página del productos
# ------------------------------------------------------------

@app.route("/productos")
def productos():
    # Renderiza la plantilla productos.html (en "contenido").

    return render_template("contenido/productos.html")

# ------------------------------------------------------------
# Ruta estática: muestra la página de clientes
# ------------------------------------------------------------

@app.route("/clientes")
def clientes():
    # Renderiza la plantilla clientes.html (en "contenido").

    return render_template("contenido/clientes.html")


# ------------------------------------------------------------
# Punto de entrada: ejecutar la aplicación en modo debug
# ------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)