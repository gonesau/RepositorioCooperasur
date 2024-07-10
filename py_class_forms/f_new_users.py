from flask_wtf import FlaskForm
from flask_wtf.form import _Auto
from wtforms import StringField, SelectField
from wtforms.validators import InputRequired, DataRequired
from py_class_forms.db_usrs import DB_Users
from py_class_forms.functions import db_conf_obj
from py_class_forms.functions import fun_StrField_required, fun_Slcfield


strRequired = lambda lbl: StringField(label=lbl, validators=[InputRequired()])


class NewUser(FlaskForm):
    dbUsrs = DB_Users(db_conf_obj('sict_sre'))
    lstCountrys = dbUsrs.get_data("SELECT * FROM paises;")
    lstCountrys.insert(0, ("", ""))
    name = strRequired("Nombre:")
    lastName = strRequired("Apellidos:")
    country = fun_Slcfield("País:", lstCountrys)
    email = strRequired("Email:")
    # tmpPswd = strRequired("Contraseña")
    institution = strRequired("Instución:")
    jobTitle = strRequired("Cargo:")

    # required = validators = [InputRequired()]
    # lst_tp_pub = dbUsrs.get_data(
    #     'SELECT id_tipo, tipo_tema FROM tp_publicacion;')
    # type_post = SelectField("Tipo Publicación: ", choices=lst_tp_pub)
    # lst_temas = dbUsrs.get_data("SELECT id_tema, tema FROM temas;")
    # theme_category = SelectField('Categoria: ', choices=lst_temas)
    # post_title = fun_StrField_required(
    #     "Titulo de la Publicación : ", "Titulo de la Publicación")
    # resume_post = TextAreaField(
    #     "Resumen breve: ", validators=[InputRequired()])
    # publicacion = CKEditorField(
    #     'Contenido nueva publicación: ', validators=[InputRequired()])
