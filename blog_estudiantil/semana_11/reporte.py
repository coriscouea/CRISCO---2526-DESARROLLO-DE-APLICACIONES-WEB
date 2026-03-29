# Importamos la librería FPDF para generar PDFs
from fpdf import FPDF

# Importamos datetime para mostrar fecha y hora en el pie de página
import locale
from datetime import datetime

locale.setlocale(locale.LC_TIME, "es_ES.UTF-8")

# =========================
# CLASE PDF PERSONALIZADA
# =========================
class PDF(FPDF):

    def header(self):
        # Intentamos insertar el logo (si no existe, no rompe el código)
        try:
            self.image("static/assets/img/titulo1.png", 10, 8, 20)
        except:
            pass

        # Configuramos fuente del título principal
        self.set_font("Arial", "B", 24)

        # Título centrado
        self.cell(0, 10, "Blog Estudiantil", 0, 1, "C")

        # Espacio después del título
        self.ln(5)

    def footer(self):
        # Posiciona el pie a 15 mm desde abajo
        self.set_y(-15)

        # Fuente pequeña en cursiva
        self.set_font("Arial", "I", 8)

        # Fecha y hora actual
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")

        # Texto izquierda (fecha)
        self.cell(0, 5, f"Generado el: {fecha}", 0, 1, "L")

        # Número de página a la derecha
        self.cell(0, 5, f"Página {self.page_no()}", 0, 0, "R")


# =========================
# REPORTE DE AUTORES
# =========================
def pdf_autores(autores):

    # Crear objeto PDF
    pdf = PDF()

    # Agregar página
    pdf.add_page()

    # Título
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reporte de Autores", 0, 1, "C")
    pdf.ln(5)

    # Encabezado tabla
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 8, "Nombre", 1, 0, "C")
    pdf.cell(60, 8, "Correo", 1, 0, "C")
    pdf.cell(70, 8, "Fecha Registro", 1, 1, "C")

    # Contenido tabla
    pdf.set_font("Arial", "", 9)

    for autor in autores:

        # Nombre
        pdf.cell(60, 8, autor.nombre, 1)

        # Correo
        pdf.cell(60, 8, autor.email, 1)

        # Fecha formateada
        fecha = autor.fecha_registro.strftime("%A, %d %B %Y") if autor.fecha_registro else "N/A"
        pdf.cell(70, 8, fecha, 1,0,"C")

        # Salto de línea
        pdf.ln()

    # Retornar PDF en bytes
    return pdf.output(dest="S").encode("latin-1")


# =========================
# REPORTE DE ARTÍCULOS
# =========================
def pdf_articulos(articulos):

    pdf = PDF()
    pdf.add_page()

    # Título
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reporte de Artículos", 0, 1, "C")
    pdf.ln(5)

    # Recorrer artículos
    for art in articulos:

        # Título del artículo
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 8, art.titulo)

        # Autor y fecha
        pdf.set_font("Arial", "I", 9)
        autor = art.autor.nombre if art.autor else "N/A"
        fecha = art.fecha_publicacion.strftime("%A, %d %B %Y") if art.fecha_publicacion else "N/A"

        pdf.multi_cell(0, 6, f"Autor: {autor} | Fecha: {fecha}")

        pdf.ln(2)

        # Contenido del artículo
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, art.contenido)

        pdf.ln(4)

        # Línea separadora
        pdf.cell(0, 0, "", 1)
        pdf.ln(5)

    return pdf.output(dest="S").encode("latin-1")


# =========================
# REPORTE COMPLETO
# =========================
def pdf_completo(articulos, autores):

    # Crear PDF
    pdf = PDF()

    # Agregar página
    pdf.add_page()

    # =========================
    # TÍTULO GENERAL
    # =========================
    pdf.set_font("Arial", "B", 14)
    pdf.cell(0, 10, "Reporte Completo del Blog", 0, 1, "C")
    pdf.ln(5)

    # =========================
    # AUTORES (TABLA)
    # =========================
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Autores Registrados", 0, 1)

    # Encabezado
    pdf.set_font("Arial", "B", 10)
    pdf.cell(60, 8, "Nombre", 1, 0, "C")
    pdf.cell(60, 8, "Correo", 1, 0, "C")
    pdf.cell(70, 8, "Fecha Registro", 1, 1, "C")

    # Datos
    pdf.set_font("Arial", "", 9)

    for autor in autores:

        pdf.cell(60, 8, autor.nombre, 1)
        pdf.cell(60, 8, autor.email, 1)

        # Formatear fecha
        fecha = autor.fecha_registro.strftime("%A, %d %B %Y") if autor.fecha_registro else "N/A"
        pdf.cell(70, 8, fecha, 1,0,"C")

        pdf.ln()

    # Espacio antes de artículos
    pdf.ln(5)

    # Nueva página para artículos (más profesional)
    pdf.add_page()

    # =========================
    # ARTÍCULOS (PÁRRAFO)
    # =========================
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Artículos Publicados", 0, 1)

    for art in articulos:

        # Título
        pdf.set_font("Arial", "B", 12)
        pdf.multi_cell(0, 8, art.titulo)

        # Autor y fecha
        pdf.set_font("Arial", "I", 9)
        autor = art.autor.nombre if art.autor else "N/A"
        fecha = art.fecha_publicacion.strftime("%A, %d %B %Y") if art.fecha_publicacion else "N/A"

        pdf.multi_cell(0, 6, f"Autor: {autor} | Fecha: {fecha}")

        pdf.ln(2)

        # Contenido
        pdf.set_font("Arial", "", 10)
        pdf.multi_cell(0, 6, art.contenido)

        pdf.ln(4)

        # Línea separadora
        pdf.cell(0, 0, "", 1)
        pdf.ln(5)

    # Retornar PDF
    return pdf.output(dest="S").encode("latin-1")