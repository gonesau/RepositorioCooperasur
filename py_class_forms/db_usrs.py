import psycopg2
from psycopg2 import Error
from py_class_forms.functions import sendEmail


class DB_Users():

    def __init__(self, dbObj) -> None:
        self.conn = psycopg2.connect(
            host=dbObj['host'],
            port=dbObj['port'],
            database=dbObj['database'],
            user=dbObj['user'],
            password=dbObj['password']
        )

    def get_data(self, query):
        try:
            cursor = self.conn.cursor()
            cursor.execute(query)
            resultados = cursor.fetchall()
            cursor.close()
            return resultados
        except psycopg2.Error as e:
            if isinstance(e, psycopg2.errors.InvalidTextRepresentation):
                self.conn.rollback()
            else:
                self.conn.rollback()

    def carga_post(self, query, data_tuple):
        cursor = self.conn.cursor()
        try:
            cursor.execute(query, data_tuple)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def del_record(self, id_post):
        cursor = self.conn.cursor()
        try:
            q = f"DELETE FROM all_posts WHERE id_post = '{id_post}';"
            cursor.execute(q)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def admin_del_usr(self, id_usr):
        cursor = self.conn.cursor()
        try:
            # ------------------------------------------------------------
            conteoPosts = f"SELECT count(*) from all_posts where id_usr = '{id_usr}';"
            conteoPosts = self.get_data(conteoPosts)[0][0]
            conteoPosts = conteoPosts if conteoPosts > 0 else 0

            queryGetUsr = self.get_data(
                f"SELECT usuario FROM usuarios WHERE id_usr = '{id_usr}';")[0][0]
            email = queryGetUsr
            q = lambda tb: f"DELETE FROM {tb} WHERE id_usr = '{id_usr}';"
            queryDelUser = q('usuarios')
            queryDelPost = q('all_posts')

            strMensaje = f'''<p><b>Usuario eliminado:</b><br><b>Usuario:</b> {queryGetUsr} <br><b>Publicaciones:</b> {conteoPosts}</p>'''

            cursor.execute(queryDelUser)
            cursor.execute(queryDelPost)
            t = 'EIMINACIÓN DE USUARIO'
            htmlBody = 'Se ha eliminado tu usuario de la base de datos al igual que todas tus publicaciones que hayas hecho.'
            sendEmail(email, t, htmlBody)
            # ------------------------------------------------------------

            self.conn.commit()

            return {"type": "info", "mensaje": strMensaje}

        except Exception as e:
            self.conn.rollback()
            raise e
        finally:
            cursor.close()

    def admin_del_admin(self, id_admin):
        cursor = self.conn.cursor()
        try:
            # ------------------------------------------------------------
            getEmail = f"SELECT email FROM administradores WHERE id = '{id_admin}';"
            getEmail = self.get_data(getEmail)[0][0]

            del_admin = f"DELETE FROM administradores WHERE id = '{id_admin}';"
            cursor.execute(del_admin)

            strMensaje = f'''<p>Administrador eliminado:<br>Email: <b>{getEmail}</b></p>'''
            # ------------------------------------------------------------
            self.conn.commit()

            mnsj = {"type": "info", "mensaje": strMensaje}

        except Exception as e:
            self.conn.rollback()
            mnsj = {"type": "error",
                    "mensaje": "<p>Error:<br><ul><li>Al eliminar usuario.</li></ul></p>"}
        finally:
            cursor.close()
            return mnsj
    
    def admin_del_category(self, id_category):
        cursor = self.conn.cursor()
        try:
            # ------------------------------------------------------------
            category = f"SELECT tema FROM temas WHERE id_tema = '{id_category}';"
            category = self.get_data(category)[0][0]
            
            del_category = f"DELETE FROM temas WHERE id_tema = '{id_category}';"
            cursor.execute(del_category)
            
            del_posts = f"DELETE FROM all_posts WHERE id_category = '{id_category}';"
            cursor.execute(del_posts)

            get_num_post = self.get_data(f"SELECT COUNT(id_category) FROM all_posts WHERE id_category = '{id_category}';")[0][0]

            strMensaje = f'''<p>Se ha eliminado la categoria <b>{category}</b> y sus <b>{get_num_post}</b> publicaciones.</p>'''
            # ------------------------------------------------------------
            self.conn.commit()

            mnsj = {"type": "info", "mensaje": strMensaje}

        except Exception as e:
            self.conn.rollback()
            mnsj = {"type": "error",
                    "mensaje": "Hubo un error al ejecutar la eliminación"}
        finally:
            cursor.close()
            return mnsj
        
    def admin_del_file(self, file_name):
        cursor = self.conn.cursor()
        try:
            no_files = f"SELECT COUNT(*) FROM files WHERE file_name = '{file_name}';"
            no_files = self.get_data(no_files)[0][0]
            
            if no_files > 0:
                del_file = f"DELETE FROM files WHERE file_name = '{file_name}';"
                cursor.execute(del_file)
                self.conn.commit()
                strMensaje = f'''<p>Se ha eliminado el archivo:<br><b>{file_name}</b>.</p>'''
                mnsj = {"type": "success", "mensaje": strMensaje}
            else:
                strMensaje = f'''<p>No se ha encontrado el archivo:<br><b>{file_name}</b>.</p>'''
                mnsj = {"type": "error", "mensaje": strMensaje}
        except Exception as e:
            self.conn.rollback()
            mnsj = {"type": "error",
                    "mensaje": "Hubo un error al ejecutar la eliminación"}
        finally:
            cursor.close()
            return mnsj
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        