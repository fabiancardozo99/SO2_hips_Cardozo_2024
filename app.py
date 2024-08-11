from flask import Flask, render_template, request, redirect, url_for
import psycopg2
from dotenv import load_dotenv
import os
import subprocess
from hips import configuracion_previa



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
            return redirect(url_for('menu')) 
        else: 
            error = "Credenciales no validas, probar otra vez" 
            return error
    else: 
        return render_template('login.html')
    
@app.route('/menu') 
def menu(): 
    return render_template('menu.html')
    

@app.route('/hips/<program_name>')
def ejecutar_herramienta(program_name):
    # se ejecuta la herramienta correspondiente
    resultado = subprocess.run(["python3", f"./hips/{program_name}"], capture_output=True, text=True)
    output = resultado.stdout
    # se muestran los datos en la interfaz de resultado
    return render_template('output.html', output=output)



@app.route('/')
def root():
    return redirect(url_for('login'))



if __name__ == "__main__":
    configuracion_previa.config_previa()
    app.run(debug=True)