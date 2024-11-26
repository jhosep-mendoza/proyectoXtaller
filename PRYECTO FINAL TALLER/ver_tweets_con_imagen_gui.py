import tkinter as tk
from PIL import Image, ImageTk

class VerTweetsConImagenGUI:
    def __init__(self, tweets):
        self.tweets = tweets
        self.ventana = tk.Tk()
        self.ventana.title("Tweets con Imágenes")
        self.ventana.geometry("600x600")

        self.canvas = tk.Canvas(self.ventana)
        self.scrollbar = tk.Scrollbar(self.ventana, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        for tweet in self.tweets:
            id_tweet, nombre_usuario, contenido, imagen_url, fecha = tweet
            self.mostrar_tweet(nombre_usuario, contenido, imagen_url, fecha)

        # Botón para cerrar la ventana
        cerrar_btn = tk.Button(self.ventana, text="Cerrar", command=self.cerrar_ventana)
        cerrar_btn.pack(pady=10)

    def mostrar_tweet(self, nombre, contenido, imagen_url, fecha):
        """Muestra un tweet con imagen en la interfaz."""
        frame = tk.Frame(self.scrollable_frame, padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=10)

        # Mostrar nombre y fecha
        label_nombre = tk.Label(frame, text=f"{nombre} | {fecha}", font=("Arial", 10, "bold"))
        label_nombre.pack(anchor="w")

        # Mostrar contenido
        label_contenido = tk.Label(frame, text=contenido, font=("Arial", 12))
        label_contenido.pack(anchor="w", pady=5)

        # Mostrar imagen
        if imagen_url:
            try:
                img = Image.open(imagen_url)
                img.thumbnail((400, 300))  # Ajustar tamaño
                img_tk = ImageTk.PhotoImage(img)

                label_imagen = tk.Label(frame, image=img_tk)
                label_imagen.image = img_tk  # Guardar referencia para evitar recolección de basura
                label_imagen.pack(anchor="center", pady=5)
            except Exception as e:
                print(f"Error al cargar imagen {imagen_url}: {e}")

    def cerrar_ventana(self):
        """Cierra la ventana."""
        self.ventana.destroy()

    def iniciar(self):
        """Inicia la ventana."""
        self.ventana.mainloop()
