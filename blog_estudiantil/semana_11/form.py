# Blog Estudiantil (proyecto individual)
# Tarea: Semana 11: Validación de formularios de productos
# Clase Producto: Debe contener atributos como ID (único), nombre, cantidad y precio, etc  Implementa métodos para obtener y establecer estos atributos.

from flask_wtf import FlaskForm
from wtforms import StringField, DecimalField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Length, NumberRange

class ProductoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=0)])
    precio = DecimalField('Precio', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Agregar Producto')

