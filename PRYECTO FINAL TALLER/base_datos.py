import mysql.connector

class BaseDatos:
    def __init__(self, host="localhost", user="root", password="", database="crud_taller"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def conectar(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as e:
            print(f"❌ Error al conectar a la base de datos: {e}")
            return None

    def eliminar_tweet(self, id_tweet):
        """Elimina el tweet y todos los comentarios asociados a ese tweet."""
        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            # Eliminar los comentarios relacionados con el tweet
            cursor.execute("DELETE FROM comentarios WHERE id_publicacion = %s", (id_tweet,))
            
            # Eliminar el tweet
            cursor.execute("DELETE FROM publicaciones WHERE id_publicacion = %s", (id_tweet,))
            
            conexion.commit()
            print(f"✅ Tweet con ID {id_tweet} eliminado exitosamente.")
        except Exception as e:
            print(f"❌ Error al eliminar el tweet: {e}")
        finally:
            cursor.close()
            conexion.close()

    def eliminar_comentario(self, id_comentario):
        """Elimina el comentario especificado."""
        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            # Eliminar el comentario
            cursor.execute("DELETE FROM comentarios WHERE id_comentario = %s", (id_comentario,))
            
            conexion.commit()
            print(f"✅ Comentario con ID {id_comentario} eliminado exitosamente.")
        except Exception as e:
            print(f"❌ Error al eliminar el comentario: {e}")
        finally:
            cursor.close()
            conexion.close()

    def eliminar_cuenta(self, id_usuario):
        """Elimina la cuenta de usuario especificada junto con todos sus tweets y comentarios."""
        conexion = self.conectar()
        cursor = conexion.cursor()

        try:
            # Eliminar los comentarios de la cuenta
            cursor.execute("DELETE FROM comentarios WHERE id_usuario = %s", (id_usuario,))
            
            # Eliminar los tweets de la cuenta
            cursor.execute("DELETE FROM publicaciones WHERE id_usuario = %s", (id_usuario,))
            
            # Eliminar la cuenta de usuario
            cursor.execute("DELETE FROM usuarios WHERE id_usuario = %s", (id_usuario,))

            conexion.commit()
            print(f"✅ Cuenta de usuario con ID {id_usuario} eliminada exitosamente.")
        except Exception as e:
            print(f"❌ Error al eliminar la cuenta: {e}")
        finally:
            cursor.close()
            conexion.close()
