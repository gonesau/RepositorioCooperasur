from datetime import datetime
import os
import json
from functools import wraps
from flask import session, redirect, url_for
from wtforms import StringField, SelectField
from wtforms.validators import DataRequired, InputRequired
from flask_bcrypt import Bcrypt

import os
import secrets
import string
import shortuuid

# send emails
from email.message import EmailMessage
import smtplib

bcrypt = Bcrypt()


def generar_contrasena():
    caracteres = string.ascii_letters + string.digits
    contrasena = ''.join(secrets.choice(caracteres) for _ in range(25))
    return contrasena


def hash_password(password):
    try:
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        return hashed_password
    except Exception as e:
        # Manejar la excepción según tu lógica de la aplicación
        print(f"Error hashing password: {str(e)}")
        return None

def sendEmail(destinatario, strEmailSubject, strHTMLBodyEmail):
    try:
        remitente = "systems.dix.dev@gmail.com"
        # crear un variable de entorno
        pswd = 'hufj gohu noso yjor'
        email = EmailMessage()
        email['From'] = remitente
        email['To'] = destinatario
        email['Subject'] = strEmailSubject

        # Establecer el cuerpo en formato HTML
        email.add_alternative(strHTMLBodyEmail, subtype='html')

        smtp = smtplib.SMTP_SSL('smtp.gmail.com')
        smtp.login(remitente, pswd)
        smtp.sendmail(remitente, destinatario, email.as_string())
        smtp.quit()
    except TimeoutError:
        # manejar este mensaje de error
        return "no se ha podido mandar el email"


def fun_StrField_required(label_name: str, txt_label: str):
    return StringField(label=label_name, validators=[InputRequired(txt_label), DataRequired('campo requerido')])


def fun_Slcfield(lblText, lstTupleOptions, defaultValue=' '):
    return SelectField(label=lblText, choices=lstTupleOptions, default=defaultValue, validators=[InputRequired()])


def db_conf_obj(dbEnvVarName: str) -> object:
    '''
    dbEnvVarName = nombre de la variable de entorno
    '''
    db = os.getenv(dbEnvVarName)
    db = json.loads(db)
    return db

def verifica_tipo_usuario(tipo_usuario):
    def decorador(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if "type_user" in session and session['type_user'] == tipo_usuario:
                return func(*args, **kwargs)
            else:
                session.clear()
                return redirect(url_for('home'))
        return wrapper
    return decorador

def getDateTime():
    cur_date = datetime.now()
    data = {
        'date': f'{cur_date.strftime("%d/%m/%Y")}',
        'time': f'{cur_date.strftime("%H:%M:%S")}'
    }
    return data


def toastObj(type, message):
    '''
    str type: error, success, info, warning
    str message: cualquier texto 
    '''
    return {"type": type, "message": message}


def getRandomId():
    # POR DEFAULT SHORUUID SACA 22 CARACTERES
    # LOS PODEMOS ACORTAR DE LA SIGUIENTE MANERA: short_id_custom = shortuuid.uuid()[:10]
    # Configurar el generador con una semilla específica (opcional)
    # shortuuid.set_alphabet("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-!#$!%&/()=?¡¿")
    shortuuid.set_alphabet("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789")
    # Generar un UUID corto con la semilla personalizada
    short_id_custom = shortuuid.uuid()
    return short_id_custom


def env_folders():
    if not os.path.exists('/var/www/cooperasur-app/static/uploads'):
        os.makedirs('/var/www/cooperasur-app/static/uploads/admins')
        os.makedirs('/var/www/cooperasur-app/static/uploads/users')

gSettings = {
    # linux: "/var/www/cooperasur-app/static/uploads/admins/"
    # windows: 'static/uploads/admins/'
    "admin": '/var/www/cooperasur-app/static/uploads/admins/'
}


def convert_size(fileObj):
    
    fileObj.stream.seek(0, 2)  # Mover el puntero al final del archivo
    file_size_bytes = fileObj.stream.tell()  # Obtener la posición del puntero (tamaño del archivo)
    fileKbSize = file_size_bytes / 1024
    
    if fileKbSize < 1024:
        size = '{:,.2f} kb'.format(fileKbSize)
        return size
    else:
        fileKbSize = fileKbSize / 1024
        size = '{:,.2f} mb'.format(fileKbSize)
        return size
    


