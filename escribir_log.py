from datetime import datetime
import subprocess


def escribir_log(prev_alarma, tipo_alarma, ip_o_email=''):
    fecha = datetime.now().strftime("%d/%m/%Y")
    
    log = f"{fecha} :: {tipo_alarma} :: {ip_o_email}"
    
    if prev_alarma == "prevencion" or prev_alarma == "alarma":
        comando = f"echo '{log}' >> /var/log/hips/{prev_alarma}.log"
        
    try:
        subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")



if __name__ == "__main__":
    escribir_log('hola')