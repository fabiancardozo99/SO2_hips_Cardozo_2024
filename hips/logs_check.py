import subprocess
import enviar_email
import escribir_log
import generar_passw


def secure_check():
    texto_comando = "sudo grep -i 'smtp:auth' /var/log/secure | grep -i 'authentication failure'"
    proceso = subprocess.run(texto_comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    texto = ''
    
    contador_user = {}
    texto_email = ''

    if proceso.stdout:
        lineas = proceso.stdout.strip().splitlines()
        
        for linea in lineas:
            user = linea.split('user=')[-1].strip()
            
            if user in contador_user:
                contador_user[user] += 1
            else:
                contador_user[user] = 1
            
            if contador_user[user] == 5:
                try:
                    contra_nueva = generar_passw.generar_contraseña()
                    comando_nueva_contra = f"sudo echo '{user}:{contra_nueva}' | sudo chpasswd"
                    subprocess.run(comando_nueva_contra, shell=True, check=True)
                    escribir_log.escribir_log('prevencion', f"multiples fallas de autenticacion de {user}")
                    
                    texto_email += f"multiples fallas de autenticacion de {user}, contrasenha cambiada a {contra_nueva}"
                    texto = texto_email
                except Exception as e:
                    print(f"Error al cambiar la contraseña para {user}: {e}")
    
    if texto_email:
        enviar_email.send_email('Prevención:', "Errores de autenticación detectados", texto_email)
        
    return texto


def block_email(email):
    try:
        # Comando para bloquear el email, por ejemplo, añadiéndolo a un archivo de blacklist
        with open("/etc/postfix/blocked_emails", "a") as blacklist_file:
            blacklist_file.write(f"{email}\n")
        
        # Recargar Postfix para aplicar los cambios
        subprocess.run(["sudo", "postfix", "reload"], check=True)
        print(f"Email {email} bloqueado exitosamente.")
        
    except Exception as e:
        print(f"Error al intentar bloquear el email {email}: {e}")        
        
        
def maillog_check():
    texto = ''
    # Comando para leer el archivo de log y filtrar por 'authid'
    comando = "sudo cat /var/log/maillog | grep -i 'authid'"
    
    try:
        # Ejecuta el comando en la terminal
        proceso = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Verificar si el comando se ejecutó correctamente
        if proceso.returncode != 0:
            print("Error al ejecutar el comando:")
            print(proceso.stderr)
            return
        
        # Dividir la salida en líneas
        archivo = proceso.stdout.strip().split("\n")

    except Exception as e:
        print(f"Error al intentar ejecutar el comando: {e}")
        return

    contador_email = {}

    # Analizar línea por línea del contenido obtenido en 'archivo'
    for linea in archivo:
        try:
            # Extraer el 'authid=' y obtener el email
            email = [word for word in linea.split() if 'authid=' in word][0]
            email = email.split("=")[-1].strip(",")  # Eliminar 'authid=' y la coma al final
            
            # Contar las ocurrencias de cada email
            if email in contador_email:
                contador_email[email] += 1
                
                # Si el email ha alcanzado 30 intentos, tomar medidas
                if contador_email[email] == 30:
                    block_email(email)
                    texto = f"El email {email} ha sido bloqueado por spam"
                    escribir_log.escribir_log("prevencion", f"mail bloqueado: {email} ha sido bloqueado por spam", email)
                    enviar_email.send_email("Prevencion", "email bloquado por spam", texto)
            else:
                contador_email[email] = 1

        except IndexError:
            print(f"Error: No se pudo extraer el email de la línea: {linea}")
        except Exception as e:
            print(f"Error al procesar la línea: {linea}. Detalles: {e}")
    
    return texto
            
if __name__ == "__main__":
    maillog_check()