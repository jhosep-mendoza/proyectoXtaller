import bcrypt
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import base64
import io

class Perfil:
    def __init__(self, db):
        self.db = db
        self.imagen_seleccionada = None  # Para almacenar la imagen seleccionada

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
                print(f"Foto de perfil: {foto_perfil if foto_perfil else 'No disponible'}")

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
            print("2. Ver perfil gráfico")
            print("3. Volver al menú principal")
            opcion = input("Elige una opción: ")
            if opcion == "1":
                self.actualizar_perfil(usuario_actual)
            elif opcion == "2":
                self.ver_perfil_grafico(usuario_actual)
            elif opcion == "3":
                break
            else:
                print("❌ Opción no válida. Intenta nuevamente.")
                
                
    def ver_perfil_grafico(self, usuario_actual):
        """Muestra el perfil gráfico en una ventana Tkinter."""
        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                "SELECT nombre_usuario, email, bio, foto_perfil, fecha_creacion FROM usuarios WHERE id_usuario = %s",
                (usuario_actual,)
            )
            perfil = cursor.fetchone()

            if perfil:
                nombre_usuario, email, bio, foto_perfil, fecha_creacion = perfil
        
                # Crear la ventana de Tkinter
                ventana = tk.Tk()
                ventana.title(f"Perfil de {nombre_usuario}")
        
                # Mostrar la foto de perfil
                if foto_perfil:
                    try:
                        foto_imagen = Image.open(foto_perfil)  # Abrir la imagen desde la ruta
                        foto_imagen.thumbnail((150, 150))
                        foto_photo = ImageTk.PhotoImage(foto_imagen)
                        label_foto = tk.Label(ventana, image=foto_photo)
                        label_foto.image = foto_photo
                        label_foto.grid(row=0, column=0, rowspan=4, padx=20, pady=20)
                    except Exception as e:
                        label_foto = tk.Label(ventana, text="Error al cargar la imagen")
                        label_foto.grid(row=0, column=0, rowspan=4, padx=20, pady=20)
                        print(f"❌ Error al cargar la imagen: {e}")
                else:
                    label_foto = tk.Label(ventana, text="No hay foto de perfil")
                    label_foto.grid(row=0, column=0, rowspan=4, padx=20, pady=20)
        
                # Mostrar los detalles del perfil
                tk.Label(ventana, text=f"Nombre de usuario: {nombre_usuario}", font=("Arial", 14, "bold")).grid(row=0, column=1, sticky="w")
                tk.Label(ventana, text=f"Correo electrónico: {email}", font=("Arial", 12)).grid(row=1, column=1, sticky="w")
                tk.Label(ventana, text=f"Biografía: {bio}", font=("Arial", 12)).grid(row=2, column=1, sticky="w")
                tk.Label(ventana, text=f"Fecha de creación: {fecha_creacion.strftime('%d-%m-%Y')}", font=("Arial", 12)).grid(row=3, column=1, sticky="w")
        
                # Botón para cerrar la ventana
                boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
                boton_cerrar.grid(row=4, column=1, pady=10)
        
                ventana.mainloop()
            else:
                print("Perfil no encontrado.")
        except Exception as e:
            print(f"❌ Error al mostrar perfil gráfico: {e}")
        finally:
            cursor.close()
            conexion.close()



    def actualizar_perfil(self, usuario_actual):
        """Permite al usuario actualizar su perfil."""
        print("\n--- Actualizar Perfil ---")
        print("1. Actualizar nombre de usuario")
        print("2. Actualizar email")
        print("3. Actualizar contraseña")
        print("4. Actualizar biografía")
        print("5. Actualizar foto de perfil")
        print("6. Volver al menú del perfil")
        
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
            self.actualizar_foto_perfil(usuario_actual)
        elif opcion == "6":
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

    def actualizar_foto_perfil(self, usuario_actual):
        """Permite al usuario elegir una foto de perfil desde su dispositivo y actualizarla en la base de datos con la ruta del archivo."""
        def elegir_foto():
            ruta_imagen = filedialog.askopenfilename(filetypes=[("Imagen", "*.png;*.jpg;*.jpeg")])
            if ruta_imagen:
                image = Image.open(ruta_imagen)
                image.thumbnail((150, 150))
                photo = ImageTk.PhotoImage(image)
                label_imagen.config(image=photo)
                label_imagen.image = photo
                self.imagen_seleccionada = ruta_imagen  # Guardamos la ruta de la imagen seleccionada
                print(f"Foto de perfil seleccionada: {ruta_imagen}")

        def actualizar_foto():
            """Actualiza la foto de perfil en la base de datos (guardando la ruta del archivo)."""
            if self.imagen_seleccionada:
                conexion = self.db.conectar()
                cursor = conexion.cursor()
                try:
                    cursor.execute(
                        "UPDATE usuarios SET foto_perfil = %s WHERE id_usuario = %s",
                        (self.imagen_seleccionada, usuario_actual)  # Guardamos la ruta de la imagen
                    )
                    conexion.commit()
                    messagebox.showinfo("✅ Éxito", " Foto de perfil actualizada exitosamente.")
                except Exception as e:
                    messagebox.showerror("❌ Error", f"No se pudo actualizar la foto: {e}")
                finally:
                    cursor.close()
                    conexion.close()
 
                cursor.close()
                conexion.close()
            else:
                messagebox.showwarning("Advertencia", "Por favor, selecciona una foto antes de actualizar.")

        ventana = tk.Tk()
        ventana.title("Actualizar Foto de Perfil")

        label_imagen = tk.Label(ventana, text="Aquí se verá tu foto de perfil.")
        label_imagen.pack()

        boton_elegir_foto = tk.Button(ventana, text="Elegir foto de perfil", command=elegir_foto)
        boton_elegir_foto.pack()

        boton_actualizar = tk.Button(ventana, text="Actualizar Foto de Perfil", command=actualizar_foto)
        boton_actualizar.pack()

        boton_cerrar = tk.Button(ventana, text="Cerrar", command=ventana.quit)
        boton_cerrar.pack()

        ventana.mainloop()
