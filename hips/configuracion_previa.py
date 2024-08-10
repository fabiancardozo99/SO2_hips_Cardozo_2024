import os
import psycopg2
import subprocess
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv('.env')   

# Funcion para conectar a la BD del hips
def conectar_bd():
    bd_name = os.getenv('BD_HIPS')
    bd_user = os.getenv('BD_USER')
    bd_password = os.getenv('BD_PASSWORD')
    bd_host = os.getenv('BD_HOST')
    bd_port = os.getenv('BD_PORT')
    
    conexion = psycopg2.connect(
        dbname=bd_name,
        user=bd_user,
        password=bd_password,
        host=bd_host,
        port=bd_port
    )
    
    return conexion 

# Funcion para eliminar los hashes de la tabla en la BD
def eliminar_hashes_bd(conexion, cursor, nombre_tabla):
    query_eliminar = sql.SQL("delete from {}").format(sql.Identifier(nombre_tabla))
    cursor.execute(query_eliminar) # Ejecutamos el query
    
    conexion.commit()
    
    print("Datos eliminados exitosamente")
    

# Funcion para guardar los hashes actuales de los archivos
def guardar_hashes_bd(conexion, cursor, nombre_tabla):
    comando_passwd = "md5sum /etc/passwd"
    comando_shadow = "sudo md5sum /etc/shadow"
    
    # LLamada al sistema
    resultado_passwd = subprocess.run(comando_passwd, shell=True, capture_output=True, text=True)
    resultado_shadow = subprocess.run(comando_shadow, shell=True, capture_output=True, text=True)
    
    passwd = resultado_passwd.stdout
    shadow = resultado_shadow.stdout
    
    passwd = passwd.split(' ')[0]
    shadow = shadow.split(' ')[0]
    
    datos = [
        ('/etc/passwd', passwd),
        ('/etc/shadow', shadow)
    ]
    
    query_insertar_hashes = "insert into {} values (%s, %s)".format(nombre_tabla)
    cursor.executemany(query_insertar_hashes, datos) # Guarda los hashes
    
    conexion.commit()
    
    print("Datos insertados")
    

def config_previa():
    
    try:
        conn = conectar_bd()
        print("Conexion exitosa")
        
        cursor = conn.cursor()
        nombre_tabla = 'hashes'
        
        # Eliminar valores de la tabla hashes para poder cargarlos de nuevo
        eliminar_hashes_bd(conn, cursor, nombre_tabla)
                
        guardar_hashes_bd(conn, cursor, nombre_tabla)
                
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Conexion terminada")


if __name__ == "__main__":
    config_previa()