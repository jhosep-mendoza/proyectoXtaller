from base_datos import BaseDatos

class CrearTweetGUI:
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.db = BaseDatos()
        self.imagen_url = None

    def obtener_contenido(self):
        """Solicita el contenido del tweet al usuario"""
        contenido = input("Contenido del Tweet (máximo 280 caracteres): ")
        return contenido.strip()

    def publicar_tweet(self):
        """Guarda el tweet en la base de datos."""
        contenido = self.obtener_contenido()
        
        if not contenido:
            print("❌ Error: El contenido del tweet no puede estar vacío.")
            return
        if len(contenido) > 280:
            print("❌ Error: El tweet no puede tener más de 280 caracteres.")
            return

        # Guardamos el tweet en la base de datos
        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO publicaciones (id_usuario, contenido)
                VALUES (%s, %s)
                """,
                (self.id_usuario, contenido)
            )
            conexion.commit()
            print("✅ Éxito: Tweet publicado con éxito.")
        except Exception as e:
            print(f"❌ Error al publicar el tweet: {e}")
        finally:
            cursor.close()
            conexion.close()

    def iniciar(self):
        """Inicia el proceso de creación del tweet desde la terminal."""
        print("\n--- Crear Tweet ---")
        self.publicar_tweet()
