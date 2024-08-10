import subprocess
import escribir_log
import enviar_email

import os
import subprocess

def chequeo_tmp():
    cuarentena_dir = "/quarantine"
    if not os.path.exists(cuarentena_dir):
        os.makedirs(cuarentena_dir)

    comando = "sudo find /tmp -type f 2>/dev/null"
    proceso = subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    lista_archivos = proceso.stdout.splitlines()
    
    
    texto_email = ''
    archivos_cuarentena = []
    extensiones = (".perl", ".py", ".sh", ".php")

    for archivo in lista_archivos:
        cuarentena = {}
        _, extension = os.path.splitext(archivo)
        
        # Verifica si el archivo es de tipo sospechoso
        if extension in extensiones :
            # Busca si el archivo tiene un #! en la primera línea
            try:
                with open(archivo, "r") as f:
                    primera_linea = f.readline()
                    if "#!" in primera_linea:
                        # Guarda en el diccionario los datos importantes 
                        cuarentena['ruta_del_archivo'] = archivo
                        cuarentena['destino_cuarentena'] = os.path.join(cuarentena_dir, os.path.basename(archivo).replace("/", "-"))
                        cuarentena['razon'] = "Archivo sospechoso, es un script"
                        archivos_cuarentena.append(cuarentena)
            except (OSError, IOError) as e:
                print(f"Error al leer el archivo {archivo}: {e}")
    print(archivos_cuarentena)


    for archivo in archivos_cuarentena:
        try:
            # Movemos el archivo
            if not os.path.exists(archivo['destino_cuarentena']):
                comando = f"sudo mv '{archivo['ruta_del_archivo']}' '{archivo['destino_cuarentena']}'"
                subprocess.run(comando, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                # Extraemos solo el nombre del archivo y escribimos en el log y el email
                nombre_archivo = os.path.basename(archivo['ruta_del_archivo'])
                escribir_log.escribir_log('prevencion', f"tmp sospechoso: El archivo {nombre_archivo} es sospechoso")
                texto_email += f"Se encontro el archivo {nombre_archivo} en /tmp y se lo movio a /quarantine"
            else:
                print(f"El archivo {archivo} ya existe en la carpeta de cuarentena.")
        except Exception as e:
            print(f"No se pudo mover a cuarentena el archivo: {nombre_archivo}. Error: {e}")

    if archivos_cuarentena:
        print("Se movieron los archivos sospechosos a cuarentena.")
        enviar_email.send_email('Prevencion: ', "Scripts sospechosos en /tmp", texto_email)


if __name__ == "__main__":
    chequeo_tmp()