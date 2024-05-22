import os
import psycopg2
import subprocess
from psycopg2 import sql
from dotenv import load_dotenv

load_dotenv('.env')    
    

def config_previa() -> None:
    bd_name = os.getenv('BD_HIPS')
    bd_user = os.getenv('BD_USER')
    bd_password = os.getenv('BD_PASSWORD')
    bd_host = os.getenv('BD_HOST')
    bd_port = os.getenv('BD_PORT')
    
    try:
        conn = psycopg2.connect(dbname=bd_name, user=bd_user, password=bd_password, host=bd_host, port=bd_port)
        print("Conexion exitosa")
        
        cursor = conn.cursor()
        nombre_tabla = 'hashes'
        
        cursor.execute(f"select count(*) from {nombre_tabla}")
        
        contador = cursor.fetchone()[0]
                
        if contador > 0:
            print("Ya hay valores en la tabla")
        else:
            comando_passwd = "md5sum /etc/passwd"
            comando_shadow = "sudo md5sum /etc/shadow"
            
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
            cursor.executemany(query_insertar_hashes, datos)
            
            conn.commit()
            
            print("Datos insertados")
                
    except psycopg2.Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        print("Conexion terminada")


config_previa()