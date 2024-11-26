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

    def eliminar_tweet(self, id_tweet):
        """Permite al usuario eliminar un tweet específico de la base de datos."""
        confirmacion = input("¿Estás seguro de que deseas eliminar este tweet? Esta acción es irreversible (sí/no): ")
    
        if confirmacion.lower() == 'sí':
            conexion = self.db.conectar()
            cursor = conexion.cursor()
            try:
                # Borrar el tweet de la base de datos
                cursor.execute("DELETE FROM publicaciones WHERE id_tweet = %s", (id_tweet,))
                conexion.commit()
                print("✅ Tweet eliminado exitosamente.")
            except Exception as e:
                print(f"❌ Error al eliminar el tweet: {e}")
            finally:
                cursor.close()
                conexion.close()
        else:
            print("❌ La acción de eliminar el tweet ha sido cancelada.")
