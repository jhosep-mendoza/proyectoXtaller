from conexion import conectar

def mostrar_menu_home():
    print("\n--- Menú Principal de Usuario ---")
    print("1. Visualizar Tweets")
    print("2. Publicar un Tweet")
    print("3. Ver Perfil")
    print("4. Cerrar Sesión")

def visualizar_tweets():
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute("SELECT id_publicacion, contenido, fecha_publicacion FROM publicaciones ORDER BY fecha_publicacion DESC")
        publicaciones = cursor.fetchall()
        print("\n--- Lista de Tweets ---")
        if publicaciones:
            for publicacion in publicaciones:
                print(f"ID: {publicacion[0]} | Fecha: {publicacion[2]}")
                print(f"Tweet: {publicacion[1]}")
                print("-" * 40)
        else:
            print("No hay tweets disponibles.")
    except Exception as e:
        print(f"Error al visualizar los tweets: {e}")
    finally:
        cursor.close()
        conexion.close()

def publicar_tweet(id_usuario):
    contenido = input("Escribe tu tweet (máximo 280 caracteres): ")
    if len(contenido) > 280:
        print("Error: El tweet supera los 280 caracteres.")
        return
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            "INSERT INTO publicaciones (id_usuario, contenido) VALUES (%s, %s)",
            (id_usuario, contenido)
        )
        conexion.commit()
        print("Tweet publicado con éxito.")
    except Exception as e:
        print(f"Error al publicar el tweet: {e}")
    finally:
        cursor.close()
        conexion.close()

def ver_perfil(id_usuario):
    conexion = conectar()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            """
            SELECT u.nombre_usuario, u.email, 
                (SELECT COUNT(*) FROM publicaciones WHERE id_usuario = u.id_usuario) AS num_tweets,
                (SELECT COUNT(*) FROM seguidores WHERE id_usuario_seguido = u.id_usuario) AS num_seguidores
            FROM usuarios u WHERE u.id_usuario = %s
            """,
            (id_usuario,)
        )
        perfil = cursor.fetchone()
        if perfil:
            print("\n--- Perfil de Usuario ---")
            print(f"Nombre de Usuario: {perfil[0]}")
            print(f"Correo Electrónico: {perfil[1]}")
            print(f"Número de Tweets: {perfil[2]}")
            print(f"Número de Seguidores: {perfil[3]}")
        else:
            print("No se encontró el perfil.")
    except Exception as e:
        print(f"Error al visualizar el perfil: {e}")
    finally:
        cursor.close()
        conexion.close()

def menu_usuario(id_usuario):
    while True:
        mostrar_menu_home()
        opcion = input("Elige una opción: ")
        if opcion == "1":
            visualizar_tweets()
        elif opcion == "2":
            publicar_tweet(id_usuario)
        elif opcion == "3":
            ver_perfil(id_usuario)
        elif opcion == "4":
            print("Cerrando sesión...")
            break
        else:
            print("Opción no válida. Por favor, elige una opción correcta.")
