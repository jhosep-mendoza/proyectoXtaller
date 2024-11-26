import tkinter as tk
from tkinter import filedialog, messagebox
from base_datos import BaseDatos


class CrearTweetGUI:
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario
        self.db = BaseDatos()

        # Configuración de la ventana principal
        self.ventana = tk.Tk()
        self.ventana.title("Crear Tweet")
        self.ventana.geometry("400x300")

        # Campo para el contenido del tweet
        self.etiqueta_contenido = tk.Label(self.ventana, text="Contenido del Tweet (280 caracteres):")
        self.etiqueta_contenido.pack(pady=10)
        self.texto_contenido = tk.Text(self.ventana, height=5, width=40)
        self.texto_contenido.pack()

        # Botón para seleccionar una imagen
        self.boton_seleccionar_imagen = tk.Button(
            self.ventana, text="Seleccionar Imagen", command=self.seleccionar_imagen
        )
        self.boton_seleccionar_imagen.pack(pady=10)

        # Etiqueta para mostrar la ruta de la imagen seleccionada
        self.etiqueta_imagen = tk.Label(self.ventana, text="No se ha seleccionado una imagen.")
        self.etiqueta_imagen.pack()

        # Botón para publicar el tweet
        self.boton_publicar = tk.Button(
            self.ventana, text="Publicar", command=self.publicar_tweet
        )
        self.boton_publicar.pack(pady=20)

        # Almacena la ruta de la imagen seleccionada
        self.imagen_url = None

    def seleccionar_imagen(self):
        """Abre un cuadro de diálogo para seleccionar una imagen y almacena la ruta."""
        ruta_imagen = filedialog.askopenfilename(
            title="Seleccionar Imagen",
            filetypes=[("Archivos de imagen", "*.jpg;*.jpeg;*.png;*.gif")]
        )
        if ruta_imagen:
            self.imagen_url = ruta_imagen
            self.etiqueta_imagen.config(text=f"Imagen seleccionada: {ruta_imagen}")
        else:
            self.etiqueta_imagen.config(text="No se ha seleccionado una imagen.")

    def publicar_tweet(self):
        """Guarda el tweet en la base de datos."""
        contenido = self.texto_contenido.get("1.0", tk.END).strip()
        if not contenido:
            messagebox.showerror("❌ Error", "El contenido del tweet no puede estar vacío.")
            return
        if len(contenido) > 280:
            messagebox.showerror("❌ Error", "El tweet no puede tener más de 280 caracteres.")
            return

        conexion = self.db.conectar()
        cursor = conexion.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO publicaciones (id_usuario, contenido, imagen_url)
                VALUES (%s, %s, %s)
                """,
                (self.id_usuario, contenido, self.imagen_url)
            )
            conexion.commit()
            messagebox.showinfo("✅ Éxito", "Tweet publicado con éxito.")
            self.texto_contenido.delete("1.0", tk.END)
            self.etiqueta_imagen.config(text="No se ha seleccionado una imagen.")
            self.imagen_url = None
        except Exception as e:
            messagebox.showerror("❌ Error", f"Error al publicar el tweet: {e}")
        finally:
            cursor.close()
            conexion.close()

    def iniciar(self):
        """Inicia la ventana de la interfaz gráfica."""
        self.ventana.mainloop()
