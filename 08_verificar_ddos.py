import subprocess
import bloquear_ip
import escribir_log
import enviar_email

def parse_ips_from_log(linea):
    try:
        parts = linea.split()
        
        # Parsear las dos ip's
        ip1 = parts[2].split('.')[0:4]  
        ip2 = parts[4].split('.')[0:4]  
        
        # Unir las partes
        ip1 = ".".join(ip1)
        ip2 = ".".join(ip2)
        
        return ip1, ip2
    
    except IndexError:
        print(f"Malformed linea: {linea}")
        return None, None


# Funcion para verificar logs y bloquear ip's en caso de posible ataque dns
def verificar_ddos():
    comando = "cat /var/log/Ataque_DNS"
    ocurrencias_ip = {}
    
    mensaje = '' # Si no pasa nada, queda vacio
    
    try:
        proceso = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        if proceso.stdout:
            archivo = proceso.stdout.splitlines() # Hay una linea vacia al final
            for linea in archivo:
                ip1, ip2 = parse_ips_from_log(linea)
                
                ocurrencias_ip[(ip1, ip2)] = ocurrencias_ip.get((ip1, ip2), 0) + 1
        
                
            for (ip1, ip2), ocurrencia in ocurrencias_ip.items():
                if ocurrencia >= 5:
                    bloquear_ip.bloquear_ip(ip1)
                    escribir_log.escribir_log("prevencion", "DDOS: ip bloquada", ip1)
                    mensaje += f"Ip bloqueada por ataque ddos: {ip1}"
                    if mensaje != '':
                        enviar_email.send_email("Prevencion", "DDOS", mensaje)
                        mensaje = ''
                        

    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
        
        
if __name__ == "__main__":
    verificar_ddos()
    