import mysql.connector
import bcrypt
from conexion import conectar
import home  # Importa el módulo home

# Función para mostrar el menú principal
def mostrar_menu():
    print("\n--- Menú Principal ---")
    print("1. Iniciar Sesión")
    print("2. Regístrate")
    print("3. Salir")

# Función para registrar un nuevo usuario
def registrar():
    nombre_usuario = input("Nombre de Usuario: ")
    email = input("Correo Electrónico: ")
    contrasena = input("Contraseña: ")

    # Encriptar la contraseña
    contrasena_encriptada = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

    # Guardar el usuario en la base de datos
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuarios (nombre_usuario, email, contraseña) VALUES (%s, %s, %s)",
            (nombre_usuario, email, contrasena_encriptada)
        )
        conexion.commit()
        print("Registro exitoso.")
    except mysql.connector.Error as err:
        print(f"Error al registrar el usuario: {err}")
    finally:
        cursor.close()
        conexion.close()

# Función para iniciar sesión
def iniciar_sesion():
    nombre_usuario = input("Nombre de Usuario: ")
    contrasena = input("Contraseña: ")

    # Comprobar el usuario y la contraseña
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "SELECT id_usuario, contraseña FROM usuarios WHERE nombre_usuario = %s",
            (nombre_usuario,)
        )
        resultado = cursor.fetchone()
        
        if resultado and bcrypt.checkpw(contrasena.encode('utf-8'), resultado[1].encode('utf-8')):
            print("Inicio de sesión exitoso.")
            id_usuario = resultado[0]
            home.menu_usuario(id_usuario)  # Llama al menú del home y pasa el id_usuario
        else:
            print("Usuario o contraseña incorrectos.")
    except mysql.connector.Error as err:
        print(f"Error al iniciar sesión: {err}")
    finally:
        cursor.close()
        conexion.close()

# Bucle principal
while True:
    mostrar_menu()
    opcion = input("Elige una opción: ")
    if opcion == "1":
        iniciar_sesion()
        break  # Detiene el menú principal si se inicia sesión exitosamente
    elif opcion == "2":
        registrar()
    elif opcion == "3":
        print("Saliendo del programa...")
        break
    else:
        print("Opción no válida. Por favor, elige una opción correcta.")
