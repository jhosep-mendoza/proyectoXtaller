from perfil import Perfil
from tweet import Tweet
from base_datos import BaseDatos
import bcrypt
from crear_tweet_gui import CrearTweetGUI
from ver_tweets_con_imagen_gui import VerTweetsConImagenGUI


class Menu:
    def __init__(self):
        self.db = BaseDatos()
        self.tweet_manager = Tweet()
        self.usuario_actual = None
        self.perfil = Perfil(self.db)  # Instanciamos la clase Perfil
        self.opciones_menu_principal = {
            "1": self.visualizar_tweets,
            "2": self.crear_tweet,
            "3": self.ver_perfil,
            "4": self.salir
        }

    def bienvenida(self):
        print("\n--- Bienvenido a Twitter ---")
        print("1. Iniciar Sesión")
        print("2. Registrarse")
        print("3. Salir")
        opcion = input("Elige una opción: ")
        if opcion == "1":
            self.iniciar_sesion()
        elif opcion == "2":
            self.registrarse()
        elif opcion == "3":
            print("Gracias por usar Twitter. ¡Hasta luego!")
            exit()
        else:
            print("❌ Opción no válida. Por favor, intenta de nuevo.")
            self.bienvenida()

    def iniciar_sesion(self):
        print("\n--- Iniciar Sesión ---")
        nombre_usuario = input("Nombre de Usuario: ")
        contrasena = input("Contraseña: ")

        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT id_usuario, contraseña FROM usuarios WHERE nombre_usuario = %s",
                (nombre_usuario,)
            )
            resultado = cursor.fetchone()

            if resultado and bcrypt.checkpw(contrasena.encode('utf-8'), resultado[1].encode('utf-8')):
                print("✅ Inicio de sesión exitoso.")
                self.usuario_actual = resultado[0]
                self.menu_principal()
            else:
                print("❌ Usuario o contraseña incorrectos ")
                self.bienvenida()
        except Exception as e:
            print(f"❌ Error al iniciar sesión: {e}")
        finally:
            cursor.close()
            conexion.close()

    def registrarse(self):
        print("\n--- Registrarse ---")
        nombre_usuario = input("Nombre de Usuario: ")
        email = input("Correo Electrónico: ")
        contrasena = input("Contraseña: ")

        # Encriptar la contraseña
        contrasena_encriptada = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "INSERT INTO usuarios (nombre_usuario, email, contraseña) VALUES (%s, %s, %s)",
                (nombre_usuario, email, contrasena_encriptada)
            )
            conexion.commit()
            print("✅ Registro exitoso. Ahora puedes iniciar sesión.")
            self.bienvenida()
        except Exception as e:
            print(f"❌ Error al registrar el usuario: {e}")
        finally:
            cursor.close()
            conexion.close()

    def mostrar_menu_principal(self):
        print("\n--- Menú Principal ---")
        print("1. Visualizar Tweets")
        print("2. Crear Tweet")
        print("3. Ver Perfil")
        print("4. Salir")

    def ejecutar_opcion_principal(self, opcion):
        accion = self.opciones_menu_principal.get(opcion)
        if accion:
            accion()
        else:
            print("❌ Opción no válida. Por favor, elige una opción correcta.")

    def visualizar_tweets(self):
        """Muestra los tweets con el nombre del usuario y accede al menú 'Para ti'."""
        tweets = self.tweet_manager.obtener_tweets()
        print("\n--- Tweets ---")
        if not tweets:
            print("No hay tweets disponibles.")
            return

        for tweet in tweets:
            id_tweet, nombre_usuario, contenido, imagen_url, fecha = tweet
            print(f"\nUsuario: {nombre_usuario} | Fecha: {fecha}")
            print(f"Contenido: {contenido}")
            if imagen_url:
                print(f"Imagen: {imagen_url}")
        
        # Mostrar menú secundario
        self.menu_para_ti()

    def menu_para_ti(self):
        """Muestra el menú 'Para ti'."""
        while True:
            print("\n--- Para ti ---")
            print("1. Ver tweets con imágenes")
            print("2. Volver al menú principal")
            opcion = input("Elige una opción: ")
            if opcion == "1":
                self.ver_tweets_con_imagenes()
            elif opcion == "2":
                break
            else:
                print("❌ Opción no válida. Intenta nuevamente.")

    def ver_tweets_con_imagenes(self):
        """Abre una ventana de Tkinter para mostrar tweets con imágenes."""
        tweets = self.tweet_manager.obtener_tweets()
        tweets_con_imagen = [t for t in tweets if t[3]]  # Filtra tweets con imagen

        if not tweets_con_imagen:
            print("No hay tweets con imágenes.")
            return

        gui = VerTweetsConImagenGUI(tweets_con_imagen)
        gui.iniciar()

    def ver_perfil(self):
        """Llama al método 'ver_perfil' de la clase Perfil"""
        self.perfil.ver_perfil(self.usuario_actual)

    def salir(self):
        print("Cerrando sesión...")
        self.usuario_actual = None
        self.bienvenida()

    def menu_principal(self):
        while True:
            self.mostrar_menu_principal()
            opcion = input("Elige una opción: ")
            self.ejecutar_opcion_principal(opcion)

    def iniciar(self):
        self.bienvenida()

    def crear_tweet(self):
        """Inicia la interfaz gráfica para crear un tweet."""
        gui = CrearTweetGUI(self.usuario_actual)
        gui.iniciar()

