import os
import subprocess
import psycopg2
from dotenv import load_dotenv
import escribir_log
import enviar_email


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

# Funcion para obtener los hashes actuales
def obtener_hashes_actuales():
    comando_passwd = "md5sum /etc/passwd"
    comando_shadow = "sudo md5sum /etc/shadow"

    # LLamadas al sistema
    resultado_passwd = subprocess.run(comando_passwd, shell=True, capture_output=True, text=True)
    resultado_shadow = subprocess.run(comando_shadow, shell=True, capture_output=True, text=True)

    passwd = resultado_passwd.stdout
    shadow = resultado_shadow.stdout

    passwd = passwd.split(' ')[0]
    shadow = shadow.split(' ')[0]
    
    return (passwd, shadow)

# Funcion que obtiene los hashes de la BD
def obtener_hashes_bd(cursor, nombre_tabla):
    query_obtener_hashes = f"select (hash) from {nombre_tabla}"
    cursor.execute(query_obtener_hashes)
    resultado = cursor.fetchall()
    return resultado

# Funcion para comparar los hashes
def comparar_hashes(hashes_actuales, hashes_bd):
    passwd_actual = hashes_actuales[0]
    shadow_actual = hashes_actuales[1]
    hashes_aux = [item[0] for item in hashes_bd]
    passwd_bd = hashes_aux[0]
    shadow_bd = hashes_aux[1]
    
    comparacion1 = passwd_actual == passwd_bd
    comparacion2 = shadow_actual == shadow_bd
    
    return comparacion1 and comparacion2

def verificar_hashes():
    nombre_tabla = 'hashes'
    texto = ""
    try:
        conn = conectar_bd() # Conectar a la BD
        cursor = conn.cursor()
        # print("Conexion exitosa")
        hashes_actuales = obtener_hashes_actuales() # Obtiene los hashes actuales de los archivos passwd y shadow
        hashes_bd = obtener_hashes_bd(cursor, nombre_tabla) # Obtiene los hashes de la BD
        
        resultado = comparar_hashes(hashes_actuales, hashes_bd) 
        
        if(resultado):
            texto = "No hubo cambios en los archivos"
            print(texto)
            return texto
        else:
            texto = "Los binarios han sido cambiados, checkear"
            print("Hashes distintos")
            escribir_log.escribir_log("alarmas", "binarios cambiados")
            enviar_email.send_email("Alarma", "Binarios", texto)
            return texto
            
        
    except psycopg2.Error as e:
        print(e)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        # print("conexion terminada")

verificar_hashes()