from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from dotenv import load_dotenv
import os
from hips import ./01_verificar_binarios


app = Flask(__name__)

def conectar_bd():
    bd_name = os.getenv('BD_HIPS')
    bd_user = os.getenv('BD_USER')
    bd_password = os.getenv('BD_PASSWORD')
    bd_host = os.getenv('BD_HOST')
    bd_port = os.getenv('BD_PORT')
    
    try:
    
        conexion = psycopg2.connect(
            dbname=bd_name,
            user=bd_user,
            password=bd_password,
            host=bd_host,
            port=bd_port
        )
        print("Conexion a la bd exitosa")
        return conexion
    except Exception as e:
        print(f"Hubo un error: {e}")
        return None

# Página de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        usuario = request.form['username'] 
        contra = request.form['password'] 

        # Conexion bd
        conn = conectar_bd() 
        cur = conn.cursor() 

        # Query the database for the user 
        cur.execute("SELECT * FROM users WHERE username = %s AND password = %s", (usuario, contra)) 
        user = cur.fetchall() 

        # Close the cursor  
        cur.close() 
        conn.close() 

        if user: 
            return redirect(url_for('success')) 
        else: 
            error = "Credenciales no validas, probar otra vez" 
            return error
    else: 
        return render_template('login.html')
    

@app.route('/success')
def success():
    return "¡Inicio de sesión exitoso!"


@app.route('/')
def root():
    return redirect(url_for('login'))



if __name__ == "__main__":
    config_previa()
    app.run(debug=True)