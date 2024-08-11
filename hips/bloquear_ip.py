import subprocess

def bloquear_ip(dir_ip):
    try:
        # Comando para bloquear la IP usando iptables
        command = ['sudo', 'iptables', '-A', 'INPUT', '-s', dir_ip, '-j', 'DROP']
        
        # Ejecutar el comando
        subprocess.run(command, check=True)
        # print(f"La IP {dir_ip} ha sido bloqueada exitosamente.")
    # Por si algo sale mal
    except subprocess.CalledProcessError as e:
        print(f"Error al intentar bloquear la IP: {e}")
    except Exception as e:
        print(f"Ha ocurrido un error inesperado: {e}")