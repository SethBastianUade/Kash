from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from services import cuenta_service, usuario_service, saldo_service, transference_service

app = Flask(__name__)
app.secret_key = 'clave_cookies'  # clave de la session

# Directorio de donde se guardaran los datos
data_dir = "data"
users_file = os.path.join(data_dir, "usuarios.txt")
accounts_file = os.path.join(data_dir, "cuentas.txt")
bancos_file = os.path.join(data_dir, "bancos.txt")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        # Aquí iría la lógica de registro
        flash('Registro exitoso', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Verificar si el archivo de usuarios existe
        if not os.path.exists(users_file):
            flash('No hay usuarios registrados', 'error')
            return redirect(url_for('login'))
        
        # Hashear la contraseña ingresada
        hashed_password = usuario_service.hash_password(password)
        
        # Verificar credenciales
        with open(users_file, 'r') as f:
            for line in f:
                stored_user, stored_hash = line.strip().split('|')
                if stored_user == username and stored_hash == hashed_password:
                    # Guardar información del usuario en la sesión
                    session['usuario'] = {
                        'username': username,
                        'nombre': username  # Por ahora usamos el username como nombre
                    }
                    flash('Inicio de sesión exitoso', 'success')
                    return redirect(url_for('dashboard'))
        
        # Si llegamos aquí, las credenciales son incorrectas
        flash('Usuario o contraseña incorrectos', 'error')
        return redirect(url_for('login'))
            
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    # Verificar si el usuario está en sesión
    if 'usuario' not in session:
        flash('Debe iniciar sesión para acceder al dashboard', 'error')
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    # Eliminar la sesión del usuario
    session.pop('usuario', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 