import mysql.connector

class BaseDatos:
    def __init__(self, host="localhost", user="root", password="", database="crud_taller"):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    def conectar(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as e:
            print(f"Error al conectar a la base de datos: {e}")
            return None
