from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

strRequired = lambda lbl: StringField(label=lbl, validators=[InputRequired()])


class ChangePswd(FlaskForm):
    pswd1 = strRequired("Nueva contraseña:")
    pswd2 = strRequired("Confirmación contraseña:")
