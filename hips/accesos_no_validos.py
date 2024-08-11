import re
import subprocess
import escribir_log, enviar_email

def bloquear_ips_intentos_fallidos():
    texto = ''
    try:
        # Comando para leer el archivo de log
        comando = f"sudo cat /var/log/remote_connection.log"
        proceso = subprocess.run(comando, shell=True, capture_output=True, text=True, check=True)
        texto_email = ""

        # Expresión regular para capturar intentos fallidos de conexión por SSH
        regex = r"Failed password for .* from (\d+\.\d+\.\d+\.\d+)"
        intentos_ip = {}

        # Procesar cada línea del log
        for line in proceso.stdout.splitlines():
            match = re.search(regex, line)
            if match:
                ip = match.group(1)
                intentos_ip[ip] = intentos_ip.get(ip, 0) + 1

        # Bloquear IPs que superan el umbral y guardarlas en un archivo
        for ip, intentos in intentos_ip.items():
            if intentos > 3: # Umbral
                try:
                    # Comando iptables para bloquear la IP
                    comando_bloqueo = f"sudo iptables -A INPUT -s {ip} -j DROP"
                    subprocess.run(comando_bloqueo, shell=True, check=True)
                    texto_email = f"Bloqueada la IP por ssh: {ip} después de {intentos} intentos fallidos de conexion ssh."
                    # print(texto_email)
                    texto = texto_email
                    print(texto)
                    escribir_log.escribir_log("prevencion", texto_email, ip)
                    # enviar_email.send_email("Prevencion", "Multiples accesos fallidos de ssh", texto_email)
                except subprocess.CalledProcessError as e:
                    print(f"Error al bloquear la IP {ip}: {e}")

    except subprocess.CalledProcessError as e:
        print(f"Error al leer el archivo de log: {e.stderr}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
        
    # return texto

bloquear_ips_intentos_fallidos()
