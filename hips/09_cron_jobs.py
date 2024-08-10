import pwd
import subprocess
import escribir_log, enviar_email

# Funcion para obtener todos los usuarios del sistema
def obtener_nombre_usuarios():
    # Obtenemos toda la informacion de los usuarios del sistema
    usuarios = pwd.getpwall()
    
    # Guardamos solo los nombres de usuarios
    nombre_usuarios = [usuario.pw_name for usuario in usuarios]
    
    return nombre_usuarios

# Funcion para obtener el crontab de un usuario
def obtener_usuario_crontab(nombre_usuario):
    try:
        # LLamada a sistema y guarda el stdout y stderr
        crontab_usuario = subprocess.run(["crontab", "-l", "-u", nombre_usuario], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return crontab_usuario.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
        

def main():
    nombres_usuarios = obtener_nombre_usuarios() 
    resultado = "" 
    nombre_cron = ""  
    texto = ''
    
    for nombre in nombres_usuarios:
        crontab = obtener_usuario_crontab(nombre)
        
        if crontab.strip() and "no crontab for" not in crontab:  # Verifica si el crontab no está vacío
            resultado += f"Crontab de usuario {nombre}:\n"
            resultado += crontab
            nombre_cron = nombre
    
    if resultado:
        texto += f"El usuario {nombre_cron} tiene algun cronjob"
        escribir_log.escribir_log("alarmas", f"cronjob: el usuario {nombre_cron} tiene algun cronjob")
        enviar_email.send_email("Alarma", "cronjob activo", texto)
    
    return texto

if __name__ == "__main__":
    main()