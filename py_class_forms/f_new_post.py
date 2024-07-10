from flask_wtf import FlaskForm
from wtforms import TextAreaField
from wtforms.validators import InputRequired, DataRequired
from py_class_forms.db_usrs import DB_Users
from py_class_forms.functions import db_conf_obj, fun_StrField_required, fun_Slcfield, toastObj
from flask_ckeditor import CKEditorField

from flask_wtf.file import FileField, FileAllowed, FileRequired


class NewPost(FlaskForm):

    dbUsrs = DB_Users(db_conf_obj('sict_sre'))

    q_lst_tp_pub = 'SELECT id_tipo, tipo_tema FROM tp_publicacion;'
    lst_tp_pub = dbUsrs.get_data(q_lst_tp_pub)
    lst_tp_pub.insert(0, ("", ""))

    q_lst_temas = "SELECT ID_TEMA, TEMA FROM TEMAS WHERE TEMA <> 'Documentos Relevantes';"
    lst_temas = dbUsrs.get_data(q_lst_temas)
    lst_temas.insert(0, ("", ""))

    type_post = fun_Slcfield("Tipo Publicación: ", lst_tp_pub)
    theme_category = fun_Slcfield("Categoria: ", lst_temas)
    post_title = fun_StrField_required(
        "Titulo de la Publicación : ", "Titulo de la Publicación")
    resume_post = TextAreaField(
        "Resumen breve: ", validators=[InputRequired()])
    
    uploadFile = FileField('Archivo', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'xlsx', 'xls', 'pptx', 'odp', 'odt', 'docx', 'doc', 'zip','rar', 'pdf',  'txt', 'ods', 'csv'], toastObj('error', '<p>Error, archivo no permitido.</p>'))])

    publicacion = CKEditorField('Contenido nueva publicación: ',
                                validators=[DataRequired()])


# backup
# class NewPost(FlaskForm):

#     dbUsrs = DB_Users(db_conf_obj('sict_sre'))

#     q_lst_tp_pub = 'SELECT id_tipo, tipo_tema FROM tp_publicacion;'
#     lst_tp_pub = dbUsrs.get_data(q_lst_tp_pub)
#     lst_tp_pub.insert(0, ("", ""))

#     q_lst_temas = "SELECT ID_TEMA, TEMA FROM TEMAS WHERE TEMA <> 'Documentos Relevantes';"
#     lst_temas = dbUsrs.get_data(q_lst_temas)
#     lst_temas.insert(0, ("", ""))

#     type_post = fun_Slcfield("Tipo Publicación: ", lst_tp_pub)
#     theme_category = fun_Slcfield("Categoria: ", lst_temas)
#     post_title = fun_StrField_required(
#         "Titulo de la Publicación : ", "Titulo de la Publicación")
#     resume_post = TextAreaField(
#         "Resumen breve: ", validators=[InputRequired()])
    

#     publicacion = CKEditorField('Contenido nueva publicación: ',
#                                 validators=[DataRequired()])