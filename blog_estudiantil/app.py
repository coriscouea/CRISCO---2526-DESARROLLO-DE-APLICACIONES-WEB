# app.py - Blog Estudiantil (proyecto individual)
# Aplicación Flask con rutas principal, dinámica y "Sobre mí"

from flask import Flask

# Crear la instancia de la aplicación
app = Flask(__name__)

# ------------------------------------------------------------
# Ruta principal: página de inicio
# ------------------------------------------------------------
@app.route("/usuario/<nombre>")
def usuario(nombre):
    """Muestra un mensaje personalizado para un usuario específico."""
    return f"<h1>¡Hola, {nombre}!</h1><p>Bienvenido a mi blog estudiantil. Explora los artículos disponibles.</p>"


@app.route("/")
def home():
    """Muestra el mensaje de bienvenida del blog estudiantil."""
    return "<h1>Blog Estudiantil - Comparte tus ideas</h1><p>Aquí encontrarás artículos escritos por estudiantes.</p>"

# ------------------------------------------------------------
# Ruta dinámica: muestra un artículo según su ID
# ------------------------------------------------------------
@app.route("/articulo/<int:id>")
def articulo(id):
    """
    Recibe un número entero como ID y devuelve un mensaje personalizado.
    Más adelante aquí se mostrará el contenido real del artículo.
    """
    return f"<h1>Artículo {id}</h1><p>Este artículo fue escrito por un estudiante. Pronto tendremos el contenido completo.</p>"

# ------------------------------------------------------------
# Ruta adicional: información sobre el creador del blog
# ------------------------------------------------------------
@app.route("/sobre-mi")
def sobre_mi():
    """Página 'Sobre mí' para identificar al autor del blog."""
    return "<h1>Sobre Mí</h1><p>Soy un estudiante apasionado por compartir conocimientos y experiencias a través de este blog. ¡Bienvenido!</p>"

# ------------------------------------------------------------
# Punto de entrada: ejecutar la aplicación en modo debug
# ------------------------------------------------------------
if __name__ == "__main__":
    app.run(debug=True)