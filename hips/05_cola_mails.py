import subprocess
import enviar_email, escribir_log

def obtener_tam_cola():
    texto = ''
    try:
        # Ejecuta el comando mailq para obtener la cola de correos
        comando = "mailq"
        resultado = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if resultado.returncode != 0:
            print(f"Error al ejecutar mailq: {resultado.stderr}")
            return
        
        # Obtiene el tamaño de la cola
        cola_salida = resultado.stdout
        lineas = cola_salida.splitlines()
        
        # Cuenta las líneas que comienzan con un ID de mensaje (que suelen ser de la cola de correos)
        tam_cola = len([linea for linea in lineas if linea.startswith(" " * 7)])
        
        texto_email = ""
        
        if tam_cola > 40:
            texto_email = f"Hay {tam_cola} mensajes en cola de correos"
            texto += texto_email
            print(f"Hay {tam_cola} mensajes en cola de correos")
            escribir_log.escribir_log("alarmas", "cola mails: Muchos mensajes en la cola de correos")
            enviar_email.send_email("Alarma", "Cola de correos", texto_email)
        else:    
            print(f"Tamaño de la cola de correos: {tam_cola} mensajes")
    
    except Exception as e:
        print(f"Error al obtener el tamaño de la cola de correos: {e}")
    
    return texto

if __name__ == "__main__":
    obtener_tam_cola()
