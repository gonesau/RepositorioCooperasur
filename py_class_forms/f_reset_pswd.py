from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

strRequired = lambda lbl: StringField(label=lbl, validators=[InputRequired()])


class ResetPwsd(FlaskForm):
    email = strRequired("Email:")
