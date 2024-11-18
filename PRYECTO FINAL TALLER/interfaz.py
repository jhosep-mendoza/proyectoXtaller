import tkinter as tk
#IMportar los modulos restantes de tkinter
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
class formularioLogin:
    
 def Formulario():
  try: 
    base = Tk()
    base.geometry("1200x300")
    base.title("Formulario Twiter")
    base.mainloop()
            
  except ValueError as error:
            print ('Error al mostrar la interfaz, error: {}'.format(error))
            
 Formulario()