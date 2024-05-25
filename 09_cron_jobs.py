import pwd
import subprocess

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
    
    for nombre in nombres_usuarios:
        print(f"Crontab de usuario {nombre}:")
        crontab = obtener_usuario_crontab(nombre)
        print(crontab)

if __name__ == "__main__":
    main()