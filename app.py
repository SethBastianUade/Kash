from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
from services import cuenta_service, usuario_service, saldo_service, transference_service

app = Flask(__name__)
app.secret_key = 'tu_clave_secreta_aqui'  # Necesario para las sesiones y flash messages

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
        # Aquí iría la lógica de login
        flash('Inicio de sesión exitoso', 'success')
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 