import subprocess
import escribir_log
import enviar_email

def main():
    comando = "w | awk 'NR>1 {print $1, $3}'" # LLama al comando w que muestra quienes estan conectados y hace un pipe al comando awk que sirve para formatear mejor el output
    texto = ""
    try:
        conectados = subprocess.run(comando, shell=True, capture_output=True, text=True)
        # print(conectados.stdout)
        texto += f"Usuarios conectados: {conectados.stdout}"
        escribir_log.escribir_log("alarmas", f"usuarios conectados: {conectados.stdout}")
        enviar_email.send_email("Alarmas", "Usuarios conectados", texto)
    except subprocess.CalledProcessError as e:
        print(f"Hubo un error al llamar a la funcion w y awk: {e.stderr}")
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        
    return texto
    
if __name__ == "__main__":
    main()