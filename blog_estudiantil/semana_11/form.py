# form.py - Módulo de formularios para el Blog Estudiantil
# Tarea: Semana 11 - Validación de formularios de artículos, autores y comentarios con WTForms
# Implementa validación de campos para el blog estudiantil

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, EmailField, SelectField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError, Optional, NumberRange

# Importar modelos para validación de unicidad
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from semana_11.modelos import Autor, Usuario
from bd import crear_conexion as crear_sesion

def obtener_opciones_autores():
    """Obtiene la lista de autores para el formulario."""
    session = crear_sesion()
    try:
        autores = session.query(Autor).all()
        # Retorna lista de tuplas (id, nombre)
        return [(0, '-- Seleccionar autor --')] + [(a.id, a.nombre) for a in autores]
    finally:
        session.close()

class ArticuloForm(FlaskForm):
    """Formulario para crear/editar artículos en el blog estudiantil.

    Utiliza WTForms para validación automática de datos:
    - Título: 5-100 caracteres requerido
    - Contenido: texto largo requerido (mínimo 50 caracteres)
    - Autor: Selección de autor de la lista
    """

    titulo = StringField(
        'Título del Artículo',
        validators=[
            DataRequired(message='El título es requerido'),
            Length(min=5, max=100, message='El título debe tener entre 5 y 100 caracteres')
        ]
    )
    contenido = TextAreaField(
        'Contenido del Artículo',
        validators=[
            DataRequired(message='El contenido es requerido'),
            Length(min=50, message='El contenido debe tener al menos 50 caracteres')
        ]
    )
    autor_id = SelectField(
        'Autor',
        choices=obtener_opciones_autores,
        validators=[
            DataRequired(message='Debe seleccionar un autor')
        ]
    )
    submit = SubmitField('Publicar Artículo')

class AutorForm(FlaskForm):
    """Formulario para crear/editar autores en el blog estudiantil.

    Utiliza WTForms para validación automática de datos:
    - Nombre: 2-50 caracteres requerido
    - Email: formato válido de email requerido
    - Bio: texto opcional (máximo 500 caracteres)
    """

    nombre = StringField(
        'Nombre del Autor',
        validators=[
            DataRequired(message='El nombre es requerido'),
            Length(min=2, max=50, message='El nombre debe tener entre 2 y 50 caracteres')
        ]
    )
    email = EmailField(
        'Correo Electrónico',
        validators=[
            DataRequired(message='El email es requerido'),
            Email(message='Debe proporcionar un email válido')
        ]
    )
    bio = TextAreaField(
        'Biografía',
        validators=[
            Optional(),
            Length(max=1000, message='La biografía no puede exceder 500 caracteres')
        ]
    )
    submit = SubmitField('Registrar Autor')
    
    def validate_email(self, field):
        """Valida que el email no esté ya registrado en la base de datos."""
        session = crear_sesion()
        try:
            autor_existente = session.query(Autor).filter_by(email=field.data).first()
            if autor_existente:
                raise ValidationError('Este correo electrónico ya está registrado en el sistema.')
        finally:
            session.close()

class ComentarioForm(FlaskForm):
    """Formulario para agregar comentarios a artículos del blog.

    Utiliza WTForms para validación automática de datos:
    - Autor: nombre del comentarista (2-50 caracteres)
    - Contenido: texto del comentario (5-500 caracteres)
    - Articulo ID: ID del artículo (requerido)
    """

    autor = StringField(
        'Tu Nombre',
        validators=[
            DataRequired(message='Tu nombre es requerido'),
            Length(min=2, max=50, message='El nombre debe tener entre 2 y 50 caracteres')
        ]
    )
    contenido = TextAreaField(
        'Comentario',
        validators=[
            DataRequired(message='El comentario es requerido'),
            Length(min=5, max=500, message='El comentario debe tener entre 5 y 500 caracteres')
        ]
    )
    articulo_id = IntegerField(
        'ID del Artículo',
        validators=[
            DataRequired(message='El ID del artículo es requerido'),
            NumberRange(min=1, message='El ID del artículo debe ser un número positivo')
        ]
    )
    submit = SubmitField('Publicar Comentario')

class LoginForm(FlaskForm):
    """Formulario para iniciar sesión."""
    identifier = StringField('Usuario o Email', validators=[DataRequired(message="Campo requerido")])
    password = PasswordField('Contraseña', validators=[DataRequired(message="Campo requerido")])
    submit = SubmitField('Iniciar Sesión')

    def validate_identifier(self,field):
        from bd import verificar_credenciales

        # Verifica usuario SIN contraseña aún
        user = verificar_credenciales(field.data, self.password.data)
        if not user:
            raise ValidationError("Usuario o contraseña incorrectos")

class RegisterForm(FlaskForm):
    """Formulario para registrar usuario."""
    usuario = StringField('Usuario', validators=[DataRequired(), Length(min=3, max=50)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    repeat_password = PasswordField('Repetir Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Registrar')

    def validate_usuario(self, field):
        session = crear_sesion()
        try:
            if session.query(Usuario).filter_by(usuario=field.data).first():
                raise ValidationError('Usuario ya existe')
        finally:
            session.close()

    def validate_email(self, field):
        session = crear_sesion()
        try:
            if session.query(Usuario).filter_by(email=field.data).first():
                raise ValidationError('Email ya registrado')
        finally:
            session.close()

    def validate_repeat_password(self, field):
        if field.data != self.password.data:
            raise ValidationError('Las contraseñas no coinciden')
