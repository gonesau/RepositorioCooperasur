from flask import Flask, render_template, jsonify, send_file, session
# from flask_cors import CORS

# from apscheduler.schedulers.background import BackgroundScheduler

# clases vistas
from py_class_forms.cls_users import V_Users
from py_class_forms.cls_admin import V_Admin
from py_class_forms.cls_visit import V_Visit

# functions
from py_class_forms.functions import verifica_tipo_usuario, env_folders

env_folders()

app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = '/static/global/imagenes/categorias/'
# app.config['SECRET_KEY'] = 'your-secret-key-here'

app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50 MB máximo por archivo cargado al servidor

# scheduler = BackgroundScheduler(daemon=True)
# scheduler.start()

#                                                          ,,            ,,         
#           mm                       mm                    db            db   mm    
#           MM                       MM                                       MM    
# ,pP"Ybd mmMMmm  ,6"Yb.  `7Mb,od8 mmMMmm     `7M'   `MF'`7MM  ,pP"Ybd `7MM mmMMmm  
# 8I   `"   MM   8)   MM    MM' "'   MM         VA   ,V    MM  8I   `"   MM   MM    
# `YMMMa.   MM    ,pm9MM    MM       MM          VA ,V     MM  `YMMMa.   MM   MM    
# L.   I8   MM   8M   MM    MM       MM           VVV      MM  L.   I8   MM   MM    
# M9mmmP'   `Mbmo`Moo9^Yo..JMML.     `Mbmo         W     .JMML.M9mmmP' .JMML. `Mbmo 

v_visits = V_Visit(app)

@app.route('/')
def main():
    return v_visits.main_pg()

# @scheduler.scheduled_job('interval', seconds=30)
@app.route('/public-data')
def public_data():
    return v_visits.public_data()

@app.route('/public-cat/<id_pub_cat>')
def pub_cat(id_pub_cat):
    return v_visits.pub_cat(id_pub_cat)

@app.route('/public-cat/<id_pub_cat>/post/<id_post>')
def pub_post(id_pub_cat, id_post):
    return v_visits.pub_post(id_pub_cat, id_post)

@app.route('/public-cat/documents')
def pub_documents():
    return v_visits.pub_documents()

@app.route('/public-cat/documents/<file_name>')
def pub_document_download(file_name):
    return v_visits.pub_document_download(file_name)

@app.route('/public-cat/document-post/<id_post>')
def pub_document_post_download(id_post):
    return v_visits.pub_document_post_download(id_post)

# @app.errorhandler(404)
# def page_not_found(error):
#     tipo_usuario = session.get('tipo_usuario')
    
# @app.errorhandler(404)
# @deco_session
# def page_not_found(error):
#     t = 'error'
#     m = "<p>La página a la que deseas entrar no esta disponible</p>"
#     flash(toastObj(t, m))
# """
# from flask import Flask, render_template, request, session, redirect, url_for

# app = Flask(__name__)
# app.secret_key = 'tu_clave_secreta'

# # Ruta para manejar el error 404
# @app.errorhandler(404)
# def page_not_found(error):
#     # Obtener la última página visitada del usuario desde la sesión
#     last_page = session.get('last_page')

#     # Si se conoce la última página visitada, redirigir al usuario a esa página
#     if last_page:
#         return redirect(last_page)

#     # Si no se conoce la última página visitada, redirigir al usuario a una página predeterminada
#     return render_template('404.html'), 404

# # Ruta para mostrar el perfil del usuario
# @app.route('/perfil')
# def perfil():
#     # Guardar la URL actual como la última página visitada en la sesión
#     session['last_page'] = request.path
#     return render_template('perfil.html')


#                           ,,                   ,,            ,,         
#                         `7MM                   db            db   mm    
#                           MM                                      MM    
#  .gP"Ya `7MMpMMMb.   ,M""bMM      `7M'   `MF'`7MM  ,pP"Ybd `7MM mmMMmm  
# ,M'   Yb  MM    MM ,AP    MM        VA   ,V    MM  8I   `"   MM   MM    
# 8M""""""  MM    MM 8MI    MM         VA ,V     MM  `YMMMa.   MM   MM    
# YM.    ,  MM    MM `Mb    MM          VVV      MM  L.   I8   MM   MM    
#  `Mbmmd'.JMML  JMML.`Wbmd"MML.         W     .JMML.M9mmmP' .JMML. `Mbmo 


# """
# Georgia11
#                                                            ,,                      ,,
#           mm                       mm                    `7MM                      db
#           MM                       MM                      MM
# ,pP"Ybd mmMMmm  ,6"Yb.  `7Mb,od8 mmMMmm      ,6"Yb.   ,M""bMM  `7MMpMMMb.pMMMb.  `7MM  `7MMpMMMb.
# 8I   `"   MM   8)   MM    MM' "'   MM       8)   MM ,AP    MM    MM    MM    MM    MM    MM    MM
# `YMMMa.   MM    ,pm9MM    MM       MM        ,pm9MM 8MI    MM    MM    MM    MM    MM    MM    MM
# L.   I8   MM   8M   MM    MM       MM       8M   MM `Mb    MM    MM    MM    MM    MM    MM    MM
# M9mmmP'   `Mbmo`Moo9^Yo..JMML.     `Mbmo    `Moo9^Yo.`Wbmd"MML..JMML  JMML  JMML..JMML..JMML  JMML.
v_admin = V_Admin(app)

@app.route('/login-admin', methods=['POST', 'GET'])
def login_admin():
    return v_admin.login_admin()

@app.route('/reset-pswd', methods=['GET', 'POST'])
def reset_pswd_admin():
    return v_admin.reset_pswd_admin()

@app.route('/admin')
@verifica_tipo_usuario('admin')
def admin_panel():
    return v_admin.admin_panel()

@app.route("/admin/change-pswd", methods=['POST', 'GET'])
@verifica_tipo_usuario('admin')
def admin_change_pswd():
    return v_admin.admin_change_pswd()

@app.route('/admin/del-usr/<id_usr>', methods=['GET', 'POST'])
@verifica_tipo_usuario('admin')
def del_usr(id_usr):
    return v_admin.del_usrs(id_usr)


@app.route('/admin/del-adm/<id_admin>', methods=['GET', 'POST'])
@verifica_tipo_usuario('admin')
def del_admin(id_admin):
    return v_admin.del_admin(id_admin)

@app.route('/admin/del-cat/<id_cat>', methods=['GET', 'POST'])
@verifica_tipo_usuario('admin')
def del_cat(id_cat):
    return v_admin.del_cat(id_cat)


@app.route("/admin/add-user", methods=['GET', 'POST'])
@verifica_tipo_usuario('admin')
def add_user():
    return v_admin.add_user()


@app.route('/admin/edit-user/<id_user>', methods=['GET', 'POST'])
@verifica_tipo_usuario('admin')
def edit_user(id_user):
    return v_admin.edit_user(id_user)


@app.route('/admin/edit-admin/<id_admin>', methods=['GET', 'POST'])
@verifica_tipo_usuario('admin')
def edit_admin(id_admin):
    return v_admin.edit_admin(id_admin)


@app.route('/admin/add-admin', methods=['GET', 'POST'])
@verifica_tipo_usuario('admin')
def add_admin():
    return v_admin.add_admin()

@app.route('/admin/upload-file', methods=['GET', 'POST'])
@verifica_tipo_usuario('admin')
def upload_file():
    return v_admin.upload_file()

@app.route('/admin/download-file/<file_name>')
@verifica_tipo_usuario('admin')
def download_file(file_name):
    return v_admin.download_file(file_name)

@app.route('/admin/delete-file/<file_name>',  methods=['GET','POST'])
@verifica_tipo_usuario('admin')
def adm_del_file(file_name):
    return v_admin.delete_file(file_name)

@app.errorhandler(413)
@verifica_tipo_usuario('admin')
def error_file_too_large(error):
    return v_admin.error_file_too_large(error)

@app.route('/admin-logout')
def admin_logout():
    return v_admin.logout()




# Georgia11
#                           ,,                     ,,                      ,,
#                         `7MM                   `7MM                      db
#                           MM                     MM
#  .gP"Ya `7MMpMMMb.   ,M""bMM       ,6"Yb.   ,M""bMM  `7MMpMMMb.pMMMb.  `7MM  `7MMpMMMb.
# ,M'   Yb  MM    MM ,AP    MM      8)   MM ,AP    MM    MM    MM    MM    MM    MM    MM
# 8M""""""  MM    MM 8MI    MM       ,pm9MM 8MI    MM    MM    MM    MM    MM    MM    MM
# YM.    ,  MM    MM `Mb    MM      8M   MM `Mb    MM    MM    MM    MM    MM    MM    MM
#  `Mbmmd'.JMML  JMML.`Wbmd"MML.    `Moo9^Yo.`Wbmd"MML..JMML  JMML  JMML..JMML..JMML  JMML.


# Georgia11
#           mm                       mm
#           MM                       MM
# ,pP"Ybd mmMMmm  ,6"Yb.  `7Mb,od8 mmMMmm     `7M'   `MF'    `7MM  `7MM  ,pP"Ybd  .gP"Ya `7Mb,od8 ,pP"Ybd
# 8I   `"   MM   8)   MM    MM' "'   MM         VA   ,V        MM    MM  8I   `" ,M'   Yb  MM' "' 8I   `"
# `YMMMa.   MM    ,pm9MM    MM       MM          VA ,V         MM    MM  `YMMMa. 8M""""""  MM     `YMMMa.
# L.   I8   MM   8M   MM    MM       MM           VVV ,,       MM    MM  L.   I8 YM.    ,  MM     L.   I8
# M9mmmP'   `Mbmo`Moo9^Yo..JMML.     `Mbmo         W  db       `Mbod"YML.M9mmmP'  `Mbmmd'.JMML.   M9mmmP'
v_users = V_Users(app)

@app.route('/login-repo', methods=['POST', 'GET'])
def home():
    return v_users.home()

@app.route('/repo')
@verifica_tipo_usuario('user')
def w_repo():
    return v_users.w_repo()

@app.route('/repo/documents')
@verifica_tipo_usuario('user')
def documents_usr():
    return v_users.documents()

@app.route('/repo/priv-info')
@verifica_tipo_usuario('user')
def priv_info():
    return v_users.priv_info()


@app.route('/repo/change-pswd', methods=['GET', 'POST'])
@verifica_tipo_usuario('user')
def change_pswd():
    return v_users.change_pswd()

@app.route('/login-repo/reset-pswd', methods=['GET', 'POST'])
def reset_pswd():
    return v_users.reset_pswd()

@app.route('/repo/cat/<categoria>')
@verifica_tipo_usuario('user')
def categoria(categoria):
    return v_users.categoria(categoria)

@app.route('/repo/cat/<categoria>/post/<id_post>')
@verifica_tipo_usuario('user')
def post(categoria, id_post):
    return v_users.post(categoria, id_post)

@app.route('/repo/np/nueva-publicacion/lst-files')
@verifica_tipo_usuario('user')
def endpoint_usr_files_uploaded():
    return v_users.endpoint_usr_files_uploaded()

@app.route('/repo/np/nueva-publicacion', methods=['GET', 'POST'])
@verifica_tipo_usuario('user')
def add_post():
    return v_users.add_post()

@app.route('/repo/mis-posts/download/<id_post>')
@verifica_tipo_usuario('user')
def usr_download_file(id_post):
    return v_users.usr_download_file(id_post)

@app.route('/repo/mis-posts')
@verifica_tipo_usuario('user')
def my_posts():
    return v_users.my_posts()

@app.route('/repo/mis-posts/edit-post/<id_post>/post-info')
@verifica_tipo_usuario('user')
def endpoint_edit_post(id_post):
    return v_users.endpoint_edit_post(id_post)

@app.route('/repo/mis-posts/edit-post/<id_post>', methods=['GET', 'POST'])
@verifica_tipo_usuario('user')
def edit_post(id_post):
    return v_users.edit_post(id_post)

@app.route('/repo/mis-posts/del-post/<id_post>', methods=['GET', 'POST'])
@verifica_tipo_usuario('user')
def del_post(id_post):
    return v_users.del_post(id_post)

@app.route('/repo/download-file/<file_name>')
@verifica_tipo_usuario('user')
def download_file_usr(file_name):
    return v_users.download_file(file_name)

@app.route('/repo/logout')
def logout():
    return v_users.logout()


# Georgia11
#                           ,,
#                         `7MM
#                           MM
#  .gP"Ya `7MMpMMMb.   ,M""bMM      `7M'   `MF'    `7MM  `7MM  ,pP"Ybd  .gP"Ya `7Mb,od8 ,pP"Ybd
# ,M'   Yb  MM    MM ,AP    MM        VA   ,V        MM    MM  8I   `" ,M'   Yb  MM' "' 8I   `"
# 8M""""""  MM    MM 8MI    MM         VA ,V         MM    MM  `YMMMa. 8M""""""  MM     `YMMMa.
# YM.    ,  MM    MM `Mb    MM          VVV ,,       MM    MM  L.   I8 YM.    ,  MM     L.   I8
#  `Mbmmd'.JMML  JMML.`Wbmd"MML.         W  db       `Mbod"YML.M9mmmP'  `Mbmmd'.JMML.   M9mmmP'


if __name__ == '__main__':
    app.run(debug=True, port=8089, host='0.0.0.0')
