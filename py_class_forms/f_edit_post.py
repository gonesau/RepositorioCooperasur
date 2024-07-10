from flask_wtf import FlaskForm
from wtforms import TextAreaField, StringField, SelectField, BooleanField
from wtforms.validators import InputRequired, DataRequired
from flask_ckeditor import CKEditorField
from py_class_forms.db_usrs import DB_Users
from py_class_forms.functions import db_conf_obj, toastObj
from py_class_forms.functions import fun_StrField_required, fun_Slcfield
from flask_wtf.file import FileField, FileAllowed

class EditPost(FlaskForm):

    dbUsrs = DB_Users(db_conf_obj('sict_sre'))

    # required = validators = [InputRequired()]
    q_lst_tp_pub = 'SELECT id_tipo, tipo_tema FROM tp_publicacion;'
    lst_tp_pub = dbUsrs.get_data(q_lst_tp_pub)
    type_post = SelectField("Tipo Publicación: ", choices=lst_tp_pub)

    q_lst_temas = "SELECT ID_TEMA, TEMA FROM TEMAS WHERE TEMA <> 'Documentos Relevantes';"
    lst_temas = dbUsrs.get_data(q_lst_temas)
    theme_category = SelectField('Categoria: ', choices=lst_temas)

    post_title = fun_StrField_required(
        "Titulo de la Publicación : ", "Titulo de la Publicación")
    
    resume_post = TextAreaField(
        "Resumen breve: ", validators=[InputRequired()])
    
    del_linked_file = BooleanField('Eliminar el archivo vinculado')
    
    uploadFile = FileField('Archivo', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'xlsx', 'xls', 'pptx', 'odp', 'odt', 'docx', 'doc', 'zip','rar', 'pdf',  'txt', 'ods', 'csv'], toastObj('error', '<p>Error, archivo no permitido.</p>'))])
    
    publicacion = CKEditorField(
        'Contenido nueva publicación: ', validators=[InputRequired()])
