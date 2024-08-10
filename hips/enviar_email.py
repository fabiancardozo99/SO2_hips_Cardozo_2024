import os 
from dotenv import load_dotenv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv('.env')

envio_desde = os.getenv('EMAIL_HIPS')
contra_desde = os.getenv('PASS_EMAIL_HIPS')
admin_email = os.getenv('EMAIL_ADMIN_HIPS')

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(alerta, subject, body):
    
    try:
        # Crear el mensaje
        msg = MIMEMultipart()
        msg['From'] = envio_desde
        msg['To'] = admin_email
        msg['Subject'] = f"{alerta} {subject}"
        
        # Agregar el cuerpo del correo
        msg.attach(MIMEText(body, 'plain'))
        
        # Conectar al servidor SMTP (por ejemplo, Gmail)
        server = smtplib.SMTP('smtp.outlook.com', 587)
        server.starttls()  # Iniciar la conexión segura
        
        # Iniciar sesión en el servidor
        server.login(envio_desde, contra_desde)
        
        # Enviar el correo
        text = msg.as_string()
        server.sendmail(envio_desde, admin_email, text)
        
        # Cerrar la conexión al servidor SMTP
        server.quit()
        
        print("Correo enviado exitosamente.")
    
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

