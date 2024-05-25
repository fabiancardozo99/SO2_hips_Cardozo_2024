import subprocess

def main():
    try:
        comando = "w | awk 'NR>1 {print $1, $3}'" # LLama al comando w que muestra quienes estan conectados y hace un pipe al comando awk que sirve para formatear mejor el output
        conectados = subprocess.run(comando, shell=True, capture_output=True, text=True)
        print(conectados.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Hubo un error al llamar a la funcion w y awk: {e.stderr}")
    
if __name__ == "__main__":
    main()