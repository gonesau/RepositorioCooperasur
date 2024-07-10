import psycopg2
from flask import render_template, session, redirect, url_for, flash, jsonify, request, send_file
from flask_bcrypt import Bcrypt
from datetime import timedelta
from flask_ckeditor import CKEditor
from flask_wtf import CSRFProtect
from werkzeug.utils import secure_filename

from psycopg2.errors import UndefinedColumn, InFailedSqlTransaction


# forms
from py_class_forms.f_login import LoginForm
from py_class_forms.f_new_users import NewUser
from py_class_forms.f_edit_users import EditUser
from py_class_forms.f_reset_pswd import ResetPwsd
from py_class_forms.f_change_pswd import ChangePswd
from py_class_forms.f_new_admin import NewAdmin
from py_class_forms.f_edit_admin import EditAdmin
from py_class_forms.f_upload_file import UploadForm

# DB
# from py_class_forms.db_usrs import DB_Users
from py_class_forms.cls_users import dbUsrs

import os

# Functions
from py_class_forms.functions import db_conf_obj, toastObj, getDateTime, hash_password, sendEmail, generar_contrasena, gSettings


class V_Admin:
    
    def __init__(self, app):
        self.app = app
        self.bcrypt = Bcrypt(app)

        self.app.config['SECRET_KEY'] = 'ProyectoSICT.CSIC.2024'
        self.app.permanent_session_lifetime = timedelta(minutes=60)
        self.csrf = CSRFProtect(app)
        self.v = {
            "login": "1_admin/a_login/login-admin.html",
            "reset_pswd": "1_admin/b.1_reset_pswd/reset_pwsd.html",
            "change_pswd": "1_admin/b.2_change_pswd/change_pswd.html",
            "admin_panel": "1_admin/b_admin_panel/admin_panel.html",
            "add_usr": "1_admin/c_add_user/add_users.html",
            "edit_usr": "1_admin/c.1_edit_user/edit_user.html",
            "add_admn": "1_admin/d_add_admin/add_admin.html",
            "edit_admin": "1_admin/d.1_edit_admin/edit_admin.html",
            "upload_file": "1_admin/e_add_file/add_file.html"
        }

    def login_admin(self):
        form = LoginForm()

        if form.validate_on_submit():
            f_usr = form.username.data
            f_pswd = form.password.data
            q = f"SELECT pswd FROM administradores WHERE email = '{f_usr}';"
            db_pswd = dbUsrs.get_data(q)
            if len(db_pswd) > 0:
                db_pswd = db_pswd[0][0]
                password_matched = self.bcrypt.check_password_hash(
                    db_pswd, f_pswd)
                if password_matched:
                    q = f"SELECT nombre, apellidos FROM administradores WHERE email = '{f_usr}';"
                    nombreUsuario = dbUsrs.get_data(q)[0]
                    nombreUsuario = f'{nombreUsuario[0]} {nombreUsuario[1]}'

                    session.permanent = True
                    session['user'] = f_usr
                    session['saludo'] = True
                    session['type_user'] = 'admin'
                    t = 'success'
                    m = f"<p>Bienvenid@:<br>{nombreUsuario}</p>"
                    flash(toastObj(t, m))
                    fecha = getDateTime()
                    fecha = f"{fecha['date']} - {fecha['time']}"

                    q = "UPDATE administradores SET lst_conn = %s where email = %s;"
                    dbUsrs.carga_post(q, (fecha, session['user']))
                    return redirect(url_for("admin_panel"))
                else:
                    title = "error"
                    htmlBody = "<p>Error, favor de verificar:<br><ul><li>Usuario</li><li>Contraseña</li></ul></p>"
                    flash(toastObj(title, htmlBody))
            else:
                title = "error"
                htmlBody = "<p>Error:<br><ul><li>Usuario no registrado</li></ul></p>"
                flash(toastObj(title, htmlBody))
        return render_template(self.v["login"], form=form)

    def reset_pswd_admin(self):
        form = ResetPwsd()
        if form.validate_on_submit():
            email = form.email.data
            q = f"SELECT email FROM administradores WHERE email = '{email}';"
            dataEmail = dbUsrs.get_data(q)
            if len(dataEmail) > 0:
                newPswd = generar_contrasena()
                hshdPswd = hash_password(newPswd)
                q = 'UPDATE administradores SET pswd = %s WHERE email = %s;'
                dbUsrs.carga_post(q, (hshdPswd, email))
                t = 'Reestauración contraseña'
                htmlBody = f"""
                <div>
                <p>La contraseña temporal es: <b>{newPswd}</b><br>
		<a href="https://repo-cooperasur.sict-csic.page/login-repo">Iniciar Sesión</a>
		</p>
                </div>
                """
                sendEmail(email, t, htmlBody)
                t = 'success'
                m = f"<p>Se ha enviado una contraseña temporal al usuarios:<br><b>{email}</b></p>"
                flash(toastObj(t, m))
                return redirect(url_for("login_admin"))
            else:
                t = 'error'
                m = f"<p>Error, no fue encontrado el usuario:<br><b>{email}</b></p>"
                flash(toastObj(t, m))
                return render_template(self.v['reset_pswd'], form=form)
        return render_template(self.v['reset_pswd'], form=form)

    def admin_change_pswd(self):
        form = ChangePswd()
        if form.validate_on_submit():
            p1 = form.pswd1.data
            p2 = form.pswd2.data
            if p1 == p2:
                hsh_pswd = hash_password(p1)
                q = "UPDATE administradores SET pswd = %s WHERE email = %s;"
                dbUsrs.carga_post(q, (hsh_pswd, session['user']))
                titleEmail = "CAMBIO DE CONTRASEÑA DEL ADMINISTRADOR"
                htmlBodyEmail = """
                <div>
                <b>Se ha cambiado con éxito la contraseña del administrador.</b>
                </div>
                """
                sendEmail(session['user'], titleEmail, htmlBodyEmail)
                if 'user' in session:
                    # Clear all session data
                    session.clear()
                    t = 'info'
                    m = "<p>Has cambiado tu contraseña de forma exitosa,<br>favor de iniciar sesión nuevamente.</p>"
                    flash(toastObj(t, m))
                    return redirect(url_for("login_admin"))

            else:
                print("la contraseña no es igual entre p1 y p2")

        return render_template(self.v['change_pswd'], form=form)

    def admin_panel(self): 
        qGetFiles = """
        SELECT
            F.OWNER_EMAIL,
            TP.TIPO_TEMA,
            F.DATE_UPLOAD,
            F.TIME_UPLOAD,
            F.FILE_NAME,
            F.FILE_SIZE,
            F.BRIEF_RESUME
        FROM
            FILES F
            INNER JOIN TP_PUBLICACION TP ON TP.ID_TIPO = F.TP_FILE;
        """
        
        qUsrs = """
        SELECT 
            U.ID_USR, 
            U.USUARIO, 
            U.NOMBRE, 
            U.APELLIDOS, 
            PS.PAIS, 
            U.LST_CONN,
            COALESCE(COUNT(CASE WHEN AP.ID_TP_POST = 1 THEN AP.ID_POST END), 0) AS NUM_POSTS_PRIV,
            COALESCE(COUNT(CASE WHEN AP.ID_TP_POST = 2 THEN AP.ID_POST END), 0) AS NUM_POST_PUB,
            COALESCE(COUNT(CASE WHEN AP.ID_TP_POST IN (1, 2) THEN AP.ID_POST END), 0) AS TOTAL_POST
        FROM 
            USUARIOS U 
        INNER JOIN 
            PAISES PS ON PS.ID_PAIS = U.PAIS
        LEFT JOIN 
            all_posts AP ON AP.ID_USR = U.ID_USR
        GROUP BY 
            U.ID_USR, 
            U.USUARIO, 
            U.NOMBRE, 
            U.APELLIDOS, 
            PS.PAIS, 
            U.LST_CONN;
        """

        # qUsrs = "SELECT U.ID_USR, U.USUARIO, U.NOMBRE, U.APELLIDOS, PS.PAIS, U.LST_CONN FROM USUARIOS U INNER JOIN PAISES PS ON PS.ID_PAIS = U.PAIS;"

        qAdmin = f"""
        SELECT a.id, a.nombre, a.apellidos, a.email, p.pais, a.lst_conn 
        FROM administradores a
        INNER JOIN paises p on p.id_pais = a.id_pais;
        """
        
        qTema = f"SELECT id_tema, tema, img_tema, seccion FROM temas ORDER BY tema;"

        curUser = session['user']
        data_files = dbUsrs.get_data(qGetFiles)
        data_usrs = dbUsrs.get_data(qUsrs)
        data_admins = dbUsrs.get_data(qAdmin)
        dataTemas = dbUsrs.get_data(qTema)
        
        return render_template(self.v["admin_panel"], data_usrs=data_usrs, data_admins=data_admins, curUser=curUser, dataTemas=dataTemas, data_files=data_files)

    def del_cat(self, ic_cat):
        # borrar categoria
        try:
            mensaje = dbUsrs.admin_del_category(ic_cat)
            return jsonify(mensaje)
        except (IndexError, ValueError) as e:
            msj = {
                "type": "error",
                "mensaje": "El registro que intentas eliminar no existe."
            }
            return jsonify(msj)

    def add_user(self):
        form = NewUser()
        if form.validate_on_submit():

            lstUsrs = dbUsrs.get_data("SELECT usuario FROM usuarios;")
            lstUsrs = [ele[0] for ele in lstUsrs]
            if form.email.data in lstUsrs:
                t = "error"
                m = f"<p>Error, usuario registrado previamente:<br><b>{form.email.data}</b></p>"
                flash(toastObj(t, m))
                form.name.data = ""
                form.lastName.data = ""
                form.country.data = ""
                form.email.data = ""
                form.institution.data = ""
                form.jobTitle.data = ""
            else:
                tmpPswd = generar_contrasena()
                ttlEmail = "CREACIÓN DE USUARIO EN REPOSITORIO"

                htmlMnsj = f'''
                <div>
                    <p>Tu cuenta de usuario ha sido creada: </p>
                    <p>
                        <b>Usuario: </b>{form.email.data}<br>
                        <b>Contraseña temporal: </b>{tmpPswd}<br>
			<a href="https://repo-cooperasur.sict-csic.page/login-repo">Iniciar Sesión</a>
                    </p>
                    <p>Te recomendamos cambiar tu contraseña una vez hayas iniciado sesión</p>
                    <p>
                    En caso de tener problemas contactar a el administrador de acuerdo a su páis:
                    <ul>
                        <li>México: email@mexico.com</li>
                        <li>Guatemala: email@guatemala.com</li>
                        <li>Belize: email@belize.com</li>
                        <li>El Salvador: email@salvador.com</li>
                        <li>Holduras: email@honduras.com</li>
                        <li>Nicaragua: email@nicaragua.com</li>
                        <li>Costa Rica: email@costarica.com</li>
                        <li>Panamá: email@panama.com</li>
                        <li>Colombia: email@colombia.com</li>
                        <li>República Dominicana: email@rd.com</li>
                    </ul>
                    </p>
                    
                    <p><b>FAVOR DE NO RESPONDER AL REMITENTE</b></p>
                </div>
                '''
                dataNewUser = (
                    form.email.data, hash_password(tmpPswd), form.name.data,
                    form.lastName.data, form.country.data, form.institution.data,
                    form.jobTitle.data)

                q = "INSERT INTO usuarios (usuario, pswd, nombre, apellidos, pais, institucion, cargo) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                dbUsrs.carga_post(q, dataNewUser)
                sendEmail(form.email.data, ttlEmail, htmlMnsj)
                type = "success"
                htmlBody = f"<p>Se ha registrado con éxito al usuario:<br><b>{form.email.data}</b></p>"
                flash(toastObj(type, htmlBody))

                return redirect(url_for("admin_panel"))
        return render_template(self.v["add_usr"], form=form)

    def edit_user(self, id_user):
        form = EditUser()
        query = f"SELECT usuario, nombre, apellidos, pais, institucion, cargo FROM usuarios WHERE id_usr = '{id_user}';"
        dataUser = dbUsrs.get_data(query)[0]
        email = dataUser[0]
        dataUser = dataUser[1:]

        if form.validate_on_submit():
            dataNewUser = (
                form.name.data, form.lastName.data, form.country.data,
                form.institution.data, form.jobTitle.data, id_user
                )
            q = "update usuarios set nombre = %s, apellidos = %s, pais = %s, institucion = %s, cargo = %s where id_usr = %s;"
            dbUsrs.carga_post(q, dataNewUser)
            pais = dbUsrs.get_data(
                f"SELECT pais FROM paises WHERE id_pais = {dataNewUser[2]};")[0][0]

            ttlEmail = "Modificación Datos del Usuario"
            htmlBody = f"""
            <div>
            <p>Se han modificados los datos de tu usuario quedando de la siguiente forma:</p>
            <p>
            <b>Nombre: </b> {dataNewUser[0]} <br>
            <b>Apellidos: </b> {dataNewUser[1]} <br>
            <b>País: </b> {pais} <br>
            <b>Intitución: </b> {dataNewUser[3]} <br>
            <b>Cargo: </b> {dataNewUser[4]}
            </p>
            <ul>
                <li>México: email@mexico.com</li>
                <li>Guatemala: email@guatemala.com</li>
                <li>Belize: email@belize.com</li>
                <li>El Salvador: email@salvador.com</li>
                <li>Holduras: email@honduras.com</li>
                <li>Nicaragua: email@nicaragua.com</li>
                <li>Costa Rica: email@costarica.com</li>
                <li>Panamá: email@panama.com</li>
                <li>Colombia: email@colombia.com</li>
                <li>República Dominicana: email@rd.com</li>
            </ul>
            </div>
            """
            sendEmail(email, ttlEmail, htmlBody)
            t = 'success'
            m = f"<p>Datos modificados con éxito del usuario:<br><b>{email}</b></p>"
            flash(toastObj(t, m))
            return redirect(url_for('admin_panel'))

        return render_template(self.v["edit_usr"], form=form, dataUser=dataUser, id_user=id_user)

    def del_usrs(self, id_usr):
        try:
            mensaje = dbUsrs.admin_del_usr(id_usr=id_usr)
            return jsonify(mensaje)
        except (IndexError, ValueError) as e:
            msj = {
                "type": "error",
                "mensaje": "El registro que intentas eliminar no existe."
            }
            return jsonify(msj)

    def add_admin(self):
        form = NewAdmin()
        if form.validate_on_submit():
            email = form.email.data
            q = f"SELECT email FROM administradores WHERE email = '{email}';"
            isUserNotRegisted = len(dbUsrs.get_data(q)) == 0

            if isUserNotRegisted:

                newPswd = generar_contrasena()
                data = (
                    form.name.data,
                    form.lastName.data,
                    hash_password(newPswd),
                    email,
                    int(form.country.data)
                )
                q = "INSERT INTO administradores (nombre, apellidos, pswd, email, id_pais) VALUES (%s, %s, %s, %s, %s);"
                dbUsrs.carga_post(q, data)
                t = 'CREACIÓN DE CUENTA DE ADMINISTRADOR'
                m = f"""
                <div>
                <p>Se ha creado una cuenta con privilecios de administrador para:</p>
                <p>
                Nombre de usuario: {email}<br>
                Contraseña temporal: {newPswd}
                </p>
                <div>
                <a href='http://127.0.0.1:8084/login-admin'>Iniciar sesión</a>
                </div>
                </div>
                """
                sendEmail(email, t, m)
                t = 'success'
                m = f"<p>Se ha registrado al nuevo administrador:<br><b>{email}</b></p>"
                flash(toastObj(t, m))
                return redirect(url_for('admin_panel'))

            else:
                t = 'error'
                m = f"<p>Error, administrador previamente registrado:<br><b>{email}</b></p>"
                flash(toastObj(t, m))

        return render_template(self.v["add_admn"], form=form)

    def edit_admin(self, id_admin):
        form = EditAdmin()
        q = f"SELECT adm.email, adm.id, adm.nombre, adm.apellidos, adm.id_pais FROM administradores adm where adm.id = '{id_admin}';"
        dataAdmin = dbUsrs.get_data(q)
        email = dataAdmin[0][0]
        dataAdmin = dataAdmin[0][1:]

        if form.validate_on_submit():
            qUpdate = "UPDATE administradores SET nombre = %s, apellidos = %s, id_pais = %s WHERE email = %s;"
            dataChngAdmin = (
                form.name.data, form.lastName.data, form.country.data, email
            )
            dbUsrs.carga_post(qUpdate, dataChngAdmin)
            type = "success"
            mensaje = f"<p>Se han cambiado los datos del administrador:<br><b>{session['user']}</b></p>"
            flash(toastObj(type, mensaje))
            return redirect(url_for('admin_panel'))

        return render_template(self.v['edit_admin'], form=form, dataAdmin=dataAdmin)

    def del_admin(self, id_admin):
        try:
            mensaje = dbUsrs.admin_del_admin(id_admin)
            return jsonify(mensaje)
        except (IndexError, ValueError) as e:
            msj = {
                "type": "error",
                "mensaje": "El registro que intentas eliminar no existe."
            }
            return jsonify(msj)

    def upload_file(self):
        form = UploadForm()
        if form.validate_on_submit():
            file = form.upload.data
            filename = secure_filename(file.filename)
            file.save(gSettings['admin'] + filename)
            # file.save('/var/www/cooperasur-app/static/uploads/admins/' + filename)
            # Obtener el tamaño del archivo en bytes
            # if file.stream.seekable():
            file.stream.seek(0, 2)  # Mover el puntero al final del archivo
            file_size_bytes = file.stream.tell()  # Obtener la posición del puntero (tamaño del archivo)
            # file.stream.seek(0)  # Restaurar el puntero al principio del archivo
            # else:
                # Si no se puede buscar en el archivo, no se puede determinar su tamaño
                # file_size_bytes = None
            
            # Convertir bytes a kilobytes
            if file_size_bytes is not None:
                
                get_files_in_db = dbUsrs.get_data("SELECT file_name FROM files;")
                get_files_in_db = [ele[0] for ele in get_files_in_db]
                if filename not in get_files_in_db:
                    file_size_kb = file_size_bytes / 1024
                    formatted_size = '{:,.2f}'.format(file_size_kb)
                    # file_extension = os.path.splitext(filename)[1]
                    # print(file_extension)
                    dataTuple = (
                        session['user'], 
                        int(form.type_post.data),
                        getDateTime()['date'],
                        getDateTime()['time'],
                        filename,
                        formatted_size,
                        form.description_file.data
                    )
                    q = 'INSERT INTO files (owner_email, tp_file, date_upload, time_upload, file_name, file_size, brief_resume) VALUES (%s, %s, %s, %s, %s, %s, %s);'
                    dbUsrs.carga_post(q, dataTuple)
                    t= 'success'
                    m = f"<p>se ha cargado correctamente el archivo:<br>{filename}</p>"
                    flash(toastObj(t, m))
                    return redirect(url_for('admin_panel'))
                elif filename in get_files_in_db:
                    t= 'error'
                    m = "En el servidor ya existe un archivo nombrado de esa forma, favor de renombrar el archivo o eliminar el archivo guardado previamente."
                    flash(toastObj(t, m))
            else:
                t= 'error'
                m = "No se pudo determinar el tamaño del archivo."
                flash(toastObj(t, m))
                
        return render_template(self.v['upload_file'], form=form)

    def delete_file(self, file_name):
        # file_path = f'/var/www/cooperasur-app/static/uploads/admins/{file_name}'
        file_path = f'{gSettings["admin"]}{file_name}'
        file_path = os.path.join(file_path)
        if os.path.exists(file_path):
            os.remove(file_path) # <- descomentar
            return dbUsrs.admin_del_file(file_name)
        
        t = "info"
        m = "<p>El archivo no existe</p>"
        flash(toastObj(t, m))
        return redirect(url_for("admin_panel"))
        
    def download_file(self, filename):
        return send_file(f'{gSettings["admin"]}{filename}', as_attachment=True)

    def error_file_too_large(self, error):
        t = 'error'
        m = "<p>El archiuvo es demasiado grande, máximo deben ser 50 mb.</p>"
        flash(toastObj(t, m))
        return redirect(url_for('upload_file'))

    def logout(self):
        # self.session.pop('user', None)
        # # return redirect(url_for('home'))
        if 'user' in session:
            # Clear all session data
            session.clear()
            # Optionally, flash a message to the user
            flash(toastObj("info", "Has cerrado sesión con éxito."))

        # Redirect to the home page after logout
        return redirect(url_for('login_admin'))

