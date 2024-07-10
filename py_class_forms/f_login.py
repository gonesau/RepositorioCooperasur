from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, InputRequired


class LoginForm(FlaskForm):
    username = StringField('Usuario: ', validators=[InputRequired(
        'Nombre de usuario requerido'), DataRequired('campo requerido')])
    password = PasswordField('Contraseña: ', validators=[InputRequired(
        'Contraseña requerida'), DataRequired('campo requerido')])
