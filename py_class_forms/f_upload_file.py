from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import SubmitField, TextAreaField
from wtforms.validators import InputRequired
from py_class_forms.db_usrs import DB_Users
from py_class_forms.functions import db_conf_obj, toastObj, fun_Slcfield
from wtforms.validators import ValidationError
from werkzeug.utils import secure_filename


# from werkzeug.utils import secure_filename


class UploadForm(FlaskForm):
    
    dbUsrs = DB_Users(db_conf_obj('sict_sre'))
    q_lst_tp_pub = 'SELECT id_tipo, tipo_tema FROM tp_publicacion;'
    lst_tp_pub = dbUsrs.get_data(q_lst_tp_pub)
    lst_tp_pub.insert(0, ("", ""))
    type_post = fun_Slcfield("Tipo: ", lst_tp_pub)

    upload = FileField('Archivo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg', 'xlsx', 'xls', 'pptx', 'odp', 'odt', 'docx', 'doc', 'zip','rar', 'pdf',  'txt', 'ods', 'csv'], toastObj('error', '<p>Error, archivo no permitido.</p>'))])

    description_file = TextAreaField(
        "Descripción: ", validators=[InputRequired()])
    # btn enviar datos
    submit = SubmitField('Enviar')


# class UploadForm(FlaskForm):
    
#     dbUsrs = DB_Users(db_conf_obj('sict_sre'))
#     q_lst_tp_pub = 'SELECT id_tipo, tipo_tema FROM tp_publicacion;'
#     lst_tp_pub = dbUsrs.get_data(q_lst_tp_pub)
#     lst_tp_pub.insert(0, ("", ""))
#     type_post = fun_Slcfield("Tipo de Documento: ", lst_tp_pub)

#     upload = FileField('Archivo', validators=[
#         FileRequired(),
#         FileAllowed(['jpg', 'png', 'jpeg', 'xlsx', 'xls', 'pptx', 'odp', 'odt', 'docx', 'doc', 'zip','rar', 'pdf',  'txt', 'ods', 'csv'],
#                     'El tipo de archivo que quieres subir no es permitido')])

#     description_file = TextAreaField(
#         "Descripción del documento: ", validators=[InputRequired()])
#     # btn enviar datos
#     submit = SubmitField('Enviar')

#     def validate_upload(self, upload):
#         if not upload.data:
#             raise ValidationError('Archivo no proporcionado.')
#         elif hasattr(upload.data.stream, 'seekable') and not upload.data.stream.seekable():
#             raise ValidationError('El archivo no es buscable.')

