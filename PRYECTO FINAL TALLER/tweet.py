from base_datos import BaseDatos

class Tweet:
    def __init__(self):
        self.db = BaseDatos()

    def obtener_tweets(self):
        """Obtiene los tweets junto con el nombre del usuario que los publicó."""
        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                SELECT p.id_usuario, u.nombre_usuario, p.contenido, p.imagen_url, p.fecha_publicacion
                FROM publicaciones p
                INNER JOIN usuarios u ON p.id_usuario = u.id_usuario
                ORDER BY p.fecha_publicacion DESC
                """
            )
            tweets = cursor.fetchall()
            return tweets
        except Exception as e:
            print(f"❌ Error al obtener tweets: {e}")
            return []
        finally:
            cursor.close()
            conexion.close()
