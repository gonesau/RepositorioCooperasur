from flask import render_template, jsonify, send_file, redirect, url_for, flash
import os
# DB
from py_class_forms.db_usrs import DB_Users

# Functions
from py_class_forms.functions import db_conf_obj, toastObj, gSettings


dbUsrs = DB_Users(db_conf_obj('sict_sre'))
get_topic = lambda id_tema: dbUsrs.get_data(f"SELECT tema FROM temas WHERE id_tema = '{id_tema}';")[0][0]

class V_Visit:
    def __init__(self, app):
      self.app = app
      
      self.v = {
        'home': 'index.html',
        'all_post': '3_visits/a_all_posts/all_posts.html',
        'post': '3_visits/b_post/post.html',
        'documents': '3_visits/c_documents/documents.html'
      }

    def main_pg(self):
      q = "SELECT ID_TEMA, TEMA, IMG_TEMA FROM TEMAS WHERE TEMA <> 'Documentos Relevantes';"
      dataTemas = dbUsrs.get_data(q) #"SELECT * FROM temas;"
      return render_template(self.v['home'], dataTemas=dataTemas)
    
    def public_data(self):
      q = """
      SELECT id_post, id_category, title_post FROM all_posts WHERE id_tp_post = 1
      ORDER BY id_post DESC
      LIMIT 8;
      """
      data = dbUsrs.get_data(q)
      return jsonify(data)
    
    def pub_cat(self, id_pub_cat):
      t = 'error'
      m = "<p>La página a la que intentas acceder no está disponible o no existe</p>"
      if len(id_pub_cat) == 22:
        try:
          q = f"SELECT id_post, id_tp_post, id_category, title_post, resume_post FROM all_posts WHERE id_category = '{id_pub_cat}' AND id_tp_post = 1;"
          data_posts = dbUsrs.get_data(q)
          tema = get_topic(id_pub_cat)
          return render_template(self.v['all_post'], data_posts=data_posts, tema=tema)
        except IndexError:
          flash(toastObj(t, m))
          return redirect(url_for("main"))
      flash(toastObj(t, m))
      return redirect(url_for("main"))
      
    def pub_post(self, id_pub_cat, id_post):
      t = 'error'
      m = "<p>La públicación a la que deseas acceder no existe.</p>"
      if len(id_pub_cat) == 22 and len(id_post) == 36:
        try:
          qIsFile = f"SELECT file_name FROM all_posts WHERE id_tp_post = 1 AND id_post = '{id_post}';"
          isFile = dbUsrs.get_data(qIsFile)[0][0]
          isFile = True if isFile is not None else False
          
          q = f"""
            SELECT ap.fecha, ap.hora, u.nombre, u.apellidos, ap.title_post, ap.html_post_body
            FROM all_posts ap
            INNER JOIN usuarios u ON u.id_usr = ap.id_usr
            WHERE ap.id_tp_post = 1 AND ap.id_category = '{id_pub_cat}' AND ap.id_post = '{id_post}';
          """
          
          dataPost = dbUsrs.get_data(q)[0]
                  
          tema = get_topic(id_pub_cat)
          return render_template(self.v['post'], dataPost=dataPost, id_pub_cat=id_pub_cat, tema=tema, id_post=id_post, isFile=isFile)
        except (IndexError, TypeError):
          m = "<p>La publicación a la que deseas acceder no esta disponible por alguna de las siguientes razones:<ul><li>Publicación eliminada por el autor.</li><li>Publicación no existente.</li></ul></p>"
          flash(toastObj(t, m))
          return redirect(url_for("main"))
      flash(toastObj(t, m))
      return redirect(url_for("main"))
    
    def pub_documents(self):
      q = """
      SELECT TP.TIPO_TEMA, F.DATE_UPLOAD, F.TIME_UPLOAD, F.FILE_SIZE, F.BRIEF_RESUME, F.FILE_NAME FROM FILES F
      INNER JOIN TP_PUBLICACION TP ON TP.ID_TIPO = F.TP_FILE AND F.TP_FILE = 1;
      """
      data_files = dbUsrs.get_data(q)
      return render_template(self.v['documents'], data_files=data_files)
    
    def pub_document_download(self, file_name):
      t = 'error'
      if len(file_name) > 0:
        q = f"SELECT file_name FROM files WHERE file_name = '{file_name}' AND tp_file = 1;"
        r = dbUsrs.get_data(q)
        if len(r) == 1:
          return send_file(f'{gSettings["admin"]}{file_name}', as_attachment=True)
        m = "<p>El archivo al que intentas acceder no esta disponible para este tipo de perfil.</p>"
        flash(toastObj(t, m))
        return redirect(url_for('pub_documents'))
      m = "<p>Solicitid de archivo no válida.</p>"
      flash(toastObj(t, m))
      return redirect(url_for('pub_documents'))
    
    def pub_document_post_download(self, id_post):
      try:
        q = f"SELECT file_path, file_name FROM all_posts WHERE id_tp_post = 1 AND id_post = '{id_post}';"
        dataFile = dbUsrs.get_data(q)[0]
        f_path = dataFile[0] 
        f_name = dataFile[1]
        fullPath = os.path.join(f_path, f_name)
        return send_file(fullPath, as_attachment=True)
      except IndexError:
        t = 'error'
        m = '<p>El documento ya no esta disponible para su descarga.</p>'
        flash(toastObj(t, m))
        return redirect(url_for('main'))
