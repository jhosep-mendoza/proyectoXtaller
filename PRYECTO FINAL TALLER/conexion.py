# conexion.py
import mysql.connector  # Importamos mysql.connector para usar la conexión a MySQL

def conectar():
    return mysql.connector.connect(
        host="localhost",
        user="root",       # Reemplaza con tu usuario de la base de datos
        password="", # Reemplaza con tu contraseña de la base de datos
        database="crud_taller"
    )
