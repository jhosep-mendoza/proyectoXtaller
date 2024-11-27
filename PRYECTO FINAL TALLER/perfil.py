import bcrypt
from PIL import Image, ImageTk
import base64
import io

class Perfil:
    def __init__(self, db):
        self.db = db

    def ver_perfil(self, usuario_actual):
        """Muestra los datos del perfil del usuario actual."""
        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT nombre_usuario, email, bio, foto_perfil FROM usuarios WHERE id_usuario = %s",
                (usuario_actual,)
            )
            perfil = cursor.fetchone()

            if perfil:
                nombre_usuario, email, bio, foto_perfil = perfil
                print(f"\n--- Perfil de {nombre_usuario} ---")
                print(f"Nombre de usuario: {nombre_usuario}")
                print(f"Correo electrónico: {email}")
                print(f"Biografía: {bio}")

                # Mostrar menú de opciones del perfil
                self.menu_perfil(usuario_actual)
            else:
                print("Perfil no encontrado.")
        except Exception as e:
            print(f"❌ Error al mostrar perfil: {e}")
        finally:
            cursor.close()
            conexion.close()

    def menu_perfil(self, usuario_actual):
        """Muestra el menú de opciones del perfil."""
        while True:
            print("\n--- Menú Perfil ---")
            print("1. Actualizar perfil")
            print("2. Volver al menú principal")
            opcion = input("Elige una opción: ")
            if opcion == "1":
                self.actualizar_perfil(usuario_actual)
            elif opcion == "2":
                break
            else:
                print("❌ Opción no válida. Intenta nuevamente.")

    def actualizar_perfil(self, usuario_actual):
        """Permite al usuario actualizar su perfil."""
        print("\n--- Actualizar Perfil ---")
        print("1. Actualizar nombre de usuario")
        print("2. Actualizar email")
        print("3. Actualizar contraseña")
        print("4. Actualizar biografía")
        print("5. Volver al menú del perfil")
        
        opcion = input("Elige una opción: ")
        
        if opcion == "1":
            self.actualizar_nombre_usuario(usuario_actual)
        elif opcion == "2":
            self.actualizar_email(usuario_actual)
        elif opcion == "3":
            self.actualizar_contrasena(usuario_actual)
        elif opcion == "4":
            self.actualizar_biografia(usuario_actual)
        elif opcion == "5":
            self.menu_perfil(usuario_actual)
        else:
            print("❌ Opción no válida. Intenta nuevamente.")

    def actualizar_nombre_usuario(self, usuario_actual):
        nuevo_nombre = input("Nuevo nombre de usuario: ")
        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET nombre_usuario = %s WHERE id_usuario = %s",
                (nuevo_nombre, usuario_actual)
            )
            conexion.commit()
            print("✅ Nombre de usuario actualizado exitosamente.")
        except Exception as e:
            print(f"❌ Error al actualizar nombre de usuario: {e}")
        finally:
            cursor.close()
            conexion.close()

    def actualizar_email(self, usuario_actual):
        nuevo_email = input("Nuevo correo electrónico: ")
        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET email = %s WHERE id_usuario = %s",
                (nuevo_email, usuario_actual)
            )
            conexion.commit()
            print("✅ Correo electrónico actualizado exitosamente.")
        except Exception as e:
            print(f"❌ Error al actualizar correo electrónico: {e}")
        finally:
            cursor.close()
            conexion.close()

    def actualizar_contrasena(self, usuario_actual):
        """Permite al usuario actualizar su contraseña."""
        antigua_contrasena = input("Contraseña actual: ")
        nueva_contrasena = input("Nueva contraseña: ")

        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT contraseña FROM usuarios WHERE id_usuario = %s",
                (usuario_actual,)
            )
            resultado = cursor.fetchone()
            
            if resultado and bcrypt.checkpw(antigua_contrasena.encode('utf-8'), resultado[0].encode('utf-8')):
                nueva_contrasena_encriptada = bcrypt.hashpw(nueva_contrasena.encode('utf-8'), bcrypt.gensalt())
                cursor.execute(
                    "UPDATE usuarios SET contraseña = %s WHERE id_usuario = %s",
                    (nueva_contrasena_encriptada, usuario_actual)
                )
                conexion.commit()
                print("✅ Contraseña actualizada exitosamente.")
            else:
                print("Contraseña antigua incorrecta.")
        except Exception as e:
            print(f"❌ Error al actualizar contraseña: {e}")
        finally:
            cursor.close()
            conexion.close()

    def actualizar_biografia(self, usuario_actual):
        nueva_biografia = input("Nueva biografía: ")    
        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "UPDATE usuarios SET bio= %s WHERE id_usuario = %s",
                (nueva_biografia, usuario_actual)
            )
            conexion.commit()
            print("✅ Biografía actualizada exitosamente.")
        except Exception as e:
            print(f"❌ Error al actualizar biografía: {e}")
        finally:
            cursor.close()
            conexion.close()
