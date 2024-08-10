from datetime import datetime
import subprocess
import os


def escribir_log(prev_alarma, tipo_alarma, ip_o_email=''):
    
        
    try:
        fecha = datetime.now().strftime("%d/%m/%Y")
    
        log = f"{fecha} :: {tipo_alarma} :: {ip_o_email}"
    
        if prev_alarma == "prevencion" or prev_alarma == "alarmas":
            texto = f"echo '{log}' >> /var/log/hips/{prev_alarma}.log"
            os.system(texto)
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")


