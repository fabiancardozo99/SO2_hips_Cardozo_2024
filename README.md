# HIPS - SO2
## Alumno: Fabian Cardozo

Puntos cubridos por el hips:

 - Verificar archivos binarios de sistema y en particular modificaciones realizadas
en el archivo /etc/passwd o /etc/shadow.
 - Verificar los usuarios conectados al sistema y sus respectivos origenes.
 - Se examinan los logs del sistema en busca de patrones de accesos indebidos. Los logs examinados son:
	 - /var/log/secure
	 - /var/log/maillog
 - Se verifica el tamaño de la cola de mail en busca de envios de correos masivos desde una misma direccion.
 - Se verifica la existencia de archivos sospechosos en el directorio /tmp.
 - Se verifican ataques ddos.
 - Se verifica la existencia de archivos en ejecucion como cron.
 - Se verifican intentos de accesos indebidos al sistema.
 

### El hips fue construido con:

 - Python
 - Flask
 - PostgreSQL


##  Pre-requisitos

#### Del sistema:

 - Linux mint
 - Tener acceso como usuario root

#### Python3

Instalar instalar Python3 y Pip3
 
    sudo apt install python3
    sudo apt install python3-pip

### Instalacion de Postfix

    sudo apt install postfix
    
##### Intalación de modulos de Python
    
Psycopg2
 
    pip3 install psycopg2

 Flask

    pip3 install flask

dotenv

    pip3 install python-dotenv

#### PostgreSQL
Instalar y configurar PostgreSQL

    sudo apt install postgresql postgresql-contrib
    
##### Pasos para configurar la Base de Datos
Iniciamos con la cuenta de postgres

    sudo -i -u postgres

Creamos un nuevo rol

    create user hips with password 'password';
    
Creamos una base de datos

    createdb hips
    
Le asignamos los permisos necesarios al rol hips

    GRANT ALL PRIVILEGES ON DATABASE hips TO hips;
    
Creamos un usuario linux

    adduser hips

## Instalacion

Descarga el programa en tu Desktop.

    git clone https://github.com/fabiancardozo99/SO2_hips_Cardozo_2024
    
Entra dentro del directorio y establece la contrasena que elegiste para la base de datos

## Crear los logs

    touch mkdir /var/log/hips/alarmas.log
    touch mkdir /var/log/hips/prevencion.log
    touch mkdir /var/log/secure
    touch mkdir /var/log/maillog

## Modo de Uso
Abrir una terminal estando como root en la carpeta HIPS

Correr el sgte comando:

    python3 app.py

En el navegador abre el siguiente link:

http://127.0.0.1:5000

usuario y contrasenha por defecto
admin , admin