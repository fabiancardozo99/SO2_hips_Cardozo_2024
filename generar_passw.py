import secrets
import string

def generar_contraseña(longitud=12):
    # Define los caracteres que se pueden usar en la contraseña
    caracteres = string.ascii_letters + string.digits + string.punctuation

    # Genera la contraseña utilizando la función choice de secrets para garantizar seguridad criptográfica
    contraseña = ''.join(secrets.choice(caracteres) for _ in range(longitud))
    return contraseña