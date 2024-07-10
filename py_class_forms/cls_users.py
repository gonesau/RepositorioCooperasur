from flask import render_template, session, redirect, url_for, flash, jsonify, send_file
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_ckeditor import CKEditor
from flask_wtf import CSRFProtect
import os
from werkzeug.utils import secure_filename

import psycopg2
from psycopg2 import Error

# forms
from py_class_forms.f_login import LoginForm
from py_class_forms.f_new_post import NewPost
from py_class_forms.f_edit_post import EditPost
from py_class_forms.f_change_pswd import ChangePswd
from py_class_forms.f_reset_pswd import ResetPwsd

# DB
from py_class_forms.db_usrs import DB_Users

# Functions
from py_class_forms.functions import db_conf_obj, toastObj, getDateTime, hash_password, sendEmail, generar_contrasena, gSettings, convert_size

dbUsrs = DB_Users(db_conf_obj('sict_sre'))



class V_Users:
    def __init__(self, app):
        self.app = app
        self.ckeditor = CKEditor(app)
        self.bcrypt = Bcrypt(app)

        self.app.config['SECRET_KEY'] = 'ProyectoSICT.CSIC.2024'
        self.app.permanent_session_lifetime = timedelta(minutes=60)
        # self.app.config['CKEDITOR_HEIGHT'] = 250
        self.csrf = CSRFProtect(app)
        self.v = {
            "home": "2_users/a_login.html",
            "wellcome": '2_users/a_wellcome/wellcome.html',
            "change_pswd": "2_users/a.2_change_pswd/change_pswd.html",
            "reset_pswd": "2_users/a.1_reset_pswd/reestablecer_pswd.html",
            "seccion": '2_users/b_seccion/seccion.html',
            'add_post': '2_users/c_add_post/add_post.html',
            'post': '2_users/d_post/post.html',
            'my_posts': '2_users/e_my_posts/my_posts.html',
            'edit_post': '2_users/f_edit_post/edit_post.html',
            'documents': '2_users/a.3_documents/documents.html'
        }
    
    def home(self):
        form = LoginForm()
        if form.validate_on_submit():
            f_usr = form.username.data
            f_pswd = form.password.data
            try:
                info_db = dbUsrs.get_data(
                    f"SELECT id_usr, usuario, pswd FROM usuarios WHERE usuario = '{f_usr}'")[0]
                id_usr, db_usr, db_pswd = info_db[0], info_db[1], info_db[2]

                password_matched = self.bcrypt.check_password_hash(
                    db_pswd, f_pswd)
                if password_matched:
                    session.permanent = True
                    session['user'] = f_usr
                    session['id_user'] = id_usr
                    session['saludo'] = True
                    session['type_user'] = 'user'

                    lstConn = getDateTime()
                    lstConn = f"{lstConn['date']} - {lstConn['time']}"
                    query = "UPDATE usuarios SET lst_conn = %s where usuario = %s;"
                    dbUsrs.carga_post(query, (lstConn, f_usr))
                    return redirect(url_for('w_repo'))
                else:
                    t = 'error'
                    m = "<p>Verificar el usuario y/o contraseña.</p>"
                    flash(toastObj(t, m))
            except IndexError:
                t = 'error'
                m = "<p>Verificar el usuario y/o contraseña.</p>"
                flash(toastObj(t, m))
        return render_template(self.v["home"], form=form)

    def priv_info(self):
        q = '''
        SELECT id_post, id_category, title_post FROM all_posts WHERE id_tp_post = 2
        ORDER BY id_post DESC
        LIMIT 8;
        '''
        data = dbUsrs.get_data(q)
        
        return jsonify(data)

    def w_repo(self):
        q = "SELECT ID_TEMA, TEMA, IMG_TEMA FROM TEMAS WHERE TEMA <> 'Documentos Relevantes';"
        dataTemas = dbUsrs.get_data(q)
        if session['saludo']:
            session['saludo'] = False
            usr_fullname = dbUsrs.get_data(
                f"SELECT nombre, apellidos FROM usuarios WHERE usuario = '{session['user']}';")[0]
            t = "success"
            m = f"<p>Bienvenid@:<br> <b>{usr_fullname[0]} {usr_fullname[1]}</b></p>"
            flash(toastObj(t, m))
            return render_template(self.v['wellcome'], dataTemas=dataTemas)
        return render_template(self.v['wellcome'], dataTemas=dataTemas)

    def reset_pswd(self):
        form = ResetPwsd()
        if form.validate_on_submit():
            email = form.email.data
            q = f"SELECT usuario FROM usuarios WHERE usuario = '{email}';"
            lstEmail = dbUsrs.get_data(q)
            if len(lstEmail) > 0:
                # enviar email
                new_pswd = generar_contrasena()
                hsh_pswd = hash_password(new_pswd)
                q = "UPDATE usuarios SET pswd = %s WHERE usuario = %s"
                dbUsrs.carga_post(q, (hsh_pswd, form.email.data))
                ttlEmail = "CONTRASEÑA REESTABLECIDA"
                htmlBody = f"se ha reestablecido la contrase a: {new_pswd}"
                form.email.data = ''
                sendEmail(email, ttlEmail, htmlBody)
                # enviar notificación en pantalla
                t = 'success'
                m = f"<p>Se envío una nueva contraseña provisional a:<br><b>{email}</b></p>"
                flash(toastObj(t, m))
                return redirect(url_for('home'))
            else:
                t = 'error'
                m = f"<p>Usuario no encontrado:<br> <b>{email}</b></p>"
                flash(toastObj(t, m))
                return render_template(self.v["reset_pswd"], form=form)
        return render_template(self.v["reset_pswd"], form=form)

    def change_pswd(self):
        form = ChangePswd()
        if form.validate_on_submit():
            p1 = form.pswd1.data
            p2 = form.pswd2.data
            if p1 == p2:
                hshPswd = hash_password(p1)
                q = "UPDATE usuarios SET pswd = %s WHERE usuario = %s;"
                email = session['user']
                t = (hshPswd, email)
                dbUsrs.carga_post(q, t)
                sendEmail(email, 'CAMBIO DE CONTRASEÑA',
                          "<p>Se ha cambiado la contraseña de forma exitosa</p>")
                if 'user' in session:
                    session.clear()
                    t = "success"
                    m = "<p>Se ha cambiado la contraseña correctamente, iniciar sesión nuevamente</p>"
                    flash(toastObj(t, m))
                    return redirect(url_for('home'))
            else:
                print("la contraseña no es igual")
        return render_template(self.v["change_pswd"], form=form)

    def categoria(self, categoria):
        t = 'error'
        if len(categoria) == 22:
            try:
                q_seccion = f"SELECT tema FROM temas WHERE id_tema = '{categoria}';"
                seccion = dbUsrs.get_data(q_seccion)[0][0]
                q_data_posts = f"SELECT ID_POST, TITLE_POST, RESUME_POST FROM ALL_POSTS WHERE ID_CATEGORY = '{categoria}';"
                data_posts = dbUsrs.get_data(q_data_posts)
                print(data_posts)
                return render_template(self.v['seccion'], seccion=seccion, data_posts=data_posts, categoria=categoria)
            except IndexError:
                m = "<p>La página a la que deseas acceder no está disponible o ya no existe.</p>"
                flash(toastObj(t, m))
                return redirect(url_for('w_repo'))
        m = "<p>La página a la que deseas acceder no existe.</p>"
        flash(toastObj(t, m))
        return redirect(url_for('w_repo'))

    def post(self, categoria, id_post):
        t = 'error'
        if len(categoria) == 22 and len(id_post) == 36:
            try:
                
                q_tema = f"SELECT tema FROM temas WHERE id_tema = '{categoria}';"
                tema = dbUsrs.get_data(q_tema)[0][0]
                
                q_publicacion = f"""
                SELECT ap.fecha, ap.hora, ap.id_usr, u.nombre, u.apellidos, ap.title_post, ap.html_post_body
                FROM all_posts ap 
                INNER JOIN usuarios u ON ap.id_usr = u.id_usr WHERE ap.id_post = '{id_post}';
                """
                
                publicacion = dbUsrs.get_data(q_publicacion)[0]
                
                isfile = dbUsrs.get_data(f"SELECT file_name FROM all_posts WHERE id_post = '{id_post}';")[0][0]
                isfile = True if isfile != None else False
                
                return render_template(self.v['post'], categoria=categoria, tema=tema, publicacion=publicacion, isfile=isfile, id_post=id_post)
            # IndexError
            except (IndexError, TypeError):
                m = '<p>La publicación a la que deseas acceder no esta disponible por alguna de las siguientes razones:<ul><li>Publicación eliminada por el autor.</li><li>Publicación no existente.</li></ul></p>'
                flash(toastObj(t, m))
                return redirect(url_for('w_repo'))

        m = "<p>La públicación a la que deseas acceder no existe.</p>"
        flash(toastObj(t, m))
        return redirect(url_for('w_repo'))

    def endpoint_usr_files_uploaded(self):
        q = f"SELECT file_name FROM all_posts WHERE id_usr = '{session['id_user']}'  AND file_name IS NOT NULL;"
        usr_files = dbUsrs.get_data(q)
        usr_files = [ele[0] for ele in usr_files]
        return jsonify(usr_files)

    def add_post(self):
        form = NewPost()

        if form.validate_on_submit():
            fecha = getDateTime()['date']
            hora = getDateTime()['time']
            
            file = form.uploadFile.data
            
            q = f"SELECT id_usr FROM usuarios WHERE usuario = '{session['user']}';"
            data_id = dbUsrs.get_data(q)[0][0]
            ruta = f'/var/www/cooperasur-app/static/uploads/users/{data_id}'

            # crear la carpeta exista o no
            if not os.path.exists(ruta):
                os.makedirs(ruta)
            
            if file:
                filename = secure_filename(file.filename)
                
                path_save = os.path.join(ruta, filename)
                
                # Guardar el archivo
                file.save(path_save)
                
                # Verificar si el archivo se ha guardado correctamente
                if os.path.exists(path_save):
                    # Obtener el tamaño del archivo
                    # file_size = os.path.getsize(path_save)
                    file_size = convert_size(file)
                    
                else:
                    print("Error al guardar el archivo.")
                    
                    # Si hay un error al guardar, establecer fileSize en None
                    file_size = None
            else:
                filename = None
                file_size = None
                
            newPost = (
                fecha,
                hora,
                session["id_user"],
                form.type_post.data,
                form.theme_category.data,
                form.post_title.data,
                form.resume_post.data,
                form.publicacion.data,
                ruta,
                filename,
                file_size
            )
            
            query = """
            INSERT INTO all_posts ( fecha, hora, id_usr, id_tp_post, id_category, title_post, resume_post, html_post_body, file_path, file_name, file_size ) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s );
            """
            
            dbUsrs.carga_post(query, newPost)
            
            # Limpiar el formulario después de enviar
            form.type_post.data = ""
            form.theme_category.data = ""
            form.post_title.data = ""
            form.resume_post.data = ""
            form.publicacion.data = ""
            
            # Mensaje de éxito
            t = "success"
            m = "<p>Publicación guardada.</p>"
            flash(toastObj(t, m))
            
            # Redireccionar a la página de repositorio después de guardar la publicación
            return redirect(url_for('w_repo'))
        
        # Renderizar la plantilla del formulario
        return render_template(self.v['add_post'], form=form)

    def usr_download_file(self, id_post):
        q = f"SELECT file_path, file_name FROM ALL_POSTS WHERE id_post = '{id_post}';"
        file = dbUsrs.get_data(q)[0]
        temp_path = os.path.join(file[0], file[1])
        # if os.path.exists(temp_path):
        #     print("el archivo si exite")
        # else:
        #     print("el archivo no existe")
        file_path = f"{file[0]}/{file[1]}"
        return send_file(file_path, as_attachment=True)

    def my_posts(self):
        q = f"""
        SELECT ts.id_tema, ap.id_post, ap.fecha, ap.hora, tp.tipo_tema, ts.tema, ap.title_post, ap.file_name, ap.file_size FROM all_posts ap
        INNER JOIN tp_publicacion tp ON ap.id_tp_post = tp.id_tipo
        INNER JOIN temas ts ON ts.id_tema = ap.id_category
        WHERE id_usr = '{session['id_user']}';
        """
        lst_post = dbUsrs.get_data(q)
        return render_template(self.v['my_posts'], lst_post=lst_post)

    def endpoint_edit_post(self, id_post):
        q = f"""
        SELECT ap.id_usr, ap.id_post, ap.id_tp_post, ap.id_category, ap.title_post, ap.resume_post, ap.html_post_body, ap.file_name, ap.file_size 
        FROM all_posts ap
        INNER JOIN usuarios u ON u.id_usr = ap.id_usr AND u.usuario = '{session["user"]}' 
        WHERE ap.id_post = '{id_post}';
        """
        data = dbUsrs.get_data(q)[0]

        id_tp_post = data[2]
        id_category = data[3]
        str_post_title = data[4]
        str_resumen_post = data[5]
        str_html_body_post = data[6]
        file_name = data[7]
        file_size = data[8]
        
        data_post = {
            'id_tp_post': id_tp_post,
            'id_category':id_category,
            'str_post_title':str_post_title,
            'str_resumen_post':str_resumen_post,
            'str_html_body_post':str_html_body_post,
            'str_file_name' : file_name,
            'str_file_size' : file_size
        }
        return jsonify(data_post)

    def edit_post(self, id_post):
        isFile = f"SELECT file_name, file_size FROM all_posts WHERE id_post = '{id_post}';"
        dataFile = dbUsrs.get_data(isFile)[0]
        new_file_name = dataFile[0]
        file_size = dataFile[1]
        isFile = True if dataFile[0] is not None else False
        
        form = EditPost()      
        if form.validate_on_submit():
            
            q_data_file = f"SELECT file_path, file_name FROM all_posts WHERE id_post = '{id_post}';"
            data_file = dbUsrs.get_data(q_data_file)[0]
            p_file, f_name = data_file[0], data_file[1]
            
            file = form.uploadFile.data
            
            # si el campo de archivo hay un documento por ser cargado
            if file:
                # datos del nuevo archivo
                new_file_name = secure_filename(file.filename)
                new_file_path = os.path.join(p_file, new_file_name)
                # eliminar el archivo en caso de existir
                if f_name is not None:
                    lst_file_path = os.path.join(p_file, f_name)
                    os.remove(lst_file_path)
                # guardar el nuevo archivo
                file.save(new_file_path)
                file_size = convert_size(file)
            
            if form.del_linked_file.data:
                old_file = os.path.join(p_file, f_name)
                os.remove(old_file)
                new_file_name = None
                file_size = None
                
            # -------------------------------
            # Definir los valores de la tupla
            # actualización de la base de datos
            data = (
                getDateTime()['date'],
                getDateTime()['time'],
                int(form.type_post.data),
                form.theme_category.data,
                form.post_title.data,
                form.resume_post.data,
                form.publicacion.data,
                new_file_name, 
                file_size,
                id_post
            )
            # Ejecutar la consulta UPDATE con los valores de la tupla
            consulta = """
            UPDATE all_posts
            SET 
                fecha = %s,
                hora = %s,
                id_tp_post = %s,
                id_category = %s,
                title_post = %s,
                resume_post = %s,
                html_post_body = %s,
                file_name = %s, 
                file_size = %s
            WHERE 
                id_post = %s;
            """

            dbUsrs.carga_post(consulta, data)

            # -------------------------------
            t = 'success'
            m = f'<p>Se ha modificado la publicación</p>'
            flash(toastObj(t, m))
            return redirect(url_for('my_posts'))
        return render_template(self.v['edit_post'], id_post=id_post, form=form, isFile=isFile)

    def del_post(self, id_post):
        
        try:
            q = f"""
            SELECT u.usuario FROM all_posts ap
            INNER JOIN usuarios u ON u.id_usr = ap.id_usr
            WHERE id_post = '{id_post}';
            """
            
            usr = dbUsrs.get_data(q)[0][0]
            
            # borrar el archivo en el servidor
            q_file_path = f"SELECT file_path, file_name FROM all_posts WHERE id_post = '{id_post}';"
            file_path = dbUsrs.get_data(q_file_path)[0]
            
            if usr == session['user']:
                dbUsrs.del_record(id_post)
                
                if file_path[0] is not None:
                    file_del = os.path.join(file_path[0],file_path[1])
                    os.remove(file_del)
                
                msj = {
                    "type": "success",
                    "mensaje": f"<p>Se ha eliminado la publicación.</p>"
                }
            else:
                msj = {
                    "type": "error",
                    "mensaje": "<p>El registro que intentas eliminar no corresponde al usuario actual.</p>"
                }
        except (IndexError, ValueError) as e:
            msj = {
                "type": "error",
                "mensaje": "<p>Publicación no encontrada en la base de datos</p>"
            }
        finally:
            return jsonify(msj)

    def documents(self):
        q = """
        SELECT TP.TIPO_TEMA, F.DATE_UPLOAD, F.TIME_UPLOAD, F.FILE_SIZE, F.BRIEF_RESUME, F.FILE_NAME
        FROM FILES F
        INNER JOIN TP_PUBLICACION TP ON TP.ID_TIPO = F.TP_FILE;
        """
        data_files = dbUsrs.get_data(q)
        return render_template(self.v['documents'], data_files=data_files)

    def download_file(self, filename):
        return send_file(f'{gSettings["admin"]}{filename}', as_attachment=True)

    def logout(self, t='info', m='Has cerrado la sesión con éxito.'):
        # session.pop('user', None)
        # # return redirect(url_for('home'))
        if 'user' in session:
            # Clear all session data
            session.clear()
            # Optionally, flash a message to the user
            flash(toastObj(t, m))

        # Redirect to the home page after logout
        return redirect(url_for('home'))


