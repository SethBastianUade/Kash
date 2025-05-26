from flask import Flask, render_template, request, redirect, url_for, flash, send_file
import os
import json
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from services import cuenta_service, usuario_service, saldo_service, transference_service
from services.cuenta_service import marcar_principal, cargar_bancos
from services.qr_service import generar_qr_pago, leer_qr_pago
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'clave_cookies'  # clave de la session

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Directorio de donde se guardaran los datos
data_dir = "data"
users_file = os.path.join(data_dir, "usuarios.json")
accounts_file = os.path.join(data_dir, "cuentas.json")
bancos_file = os.path.join(data_dir, "bancos.json")

# Modelo de usuario para Flask-Login
class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username

    @staticmethod
    def get(username):
        if not os.path.exists(users_file):
            return None
        with open(users_file, 'r', encoding='utf-8') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}
        if username in users:
            return User(username)
        return None

@login_manager.user_loader
def load_user(username):
    return User.get(username)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        referido = request.form.get('referido')
        if not username or not password:
            flash('Usuario y contraseña requeridos', 'error')
            return redirect(url_for('registro'))
        hashed_password = usuario_service.hash_password(password)
        users = {}
        if os.path.exists(users_file):
            with open(users_file, 'r', encoding='utf-8') as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = {}
        if username in users:
            flash('El usuario ya existe', 'error')
            return redirect(url_for('registro'))
        users[username] = {'password': hashed_password}
        with open(users_file, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=2)
        # Asignar saldo inicial según referido
        if referido:
            saldo_service.asignar_saldo_inicial(username, True, referido)
        else:
            saldo_service.asignar_saldo_inicial(username, False)
        flash('Registro exitoso', 'success')
        return redirect(url_for('login'))
    return render_template('registro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if not os.path.exists(users_file):
            flash('No hay usuarios registrados', 'error')
            return redirect(url_for('login'))
        hashed_password = usuario_service.hash_password(password)
        with open(users_file, 'r', encoding='utf-8') as f:
            try:
                users = json.load(f)
            except json.JSONDecodeError:
                users = {}
        if username in users and users[username]['password'] == hashed_password:
            user = User(username)
            login_user(user)
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('dashboard'))
        flash('Usuario o contraseña incorrectos', 'error')
        return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/dashboard')
@login_required
def dashboard():
    # Mostrar saldo real
    saldo = 0.0
    try:
        with open('data/saldos.json', 'r', encoding='utf-8') as f:
            saldos = json.load(f)
            saldo = saldos.get(current_user.username, 0.0)
    except Exception:
        pass
    return render_template('dashboard.html', saldo=saldo)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada exitosamente', 'success')
    return redirect(url_for('index'))

@app.route('/ayuda')
def ayuda():
    return render_template('ayuda.html')

@app.route('/terminos')
def terminos():
    return render_template('terminos.html')

@app.route('/privacidad')
def privacidad():
    return render_template('privacidad.html')

@app.route('/transferencias', methods=['GET', 'POST'])
@login_required
def transferencias():
    mensaje = None
    # Validar que el usuario tenga al menos una cuenta bancaria
    cuentas_usuario = []
    try:
        with open('data/cuentas.json', 'r', encoding='utf-8') as f:
            todas = json.load(f)
            cuentas_usuario = [c for c in todas if c['usuario'] == current_user.username]
    except Exception:
        pass
    if not cuentas_usuario:
        mensaje = 'Debes tener al menos una cuenta bancaria vinculada para realizar transferencias.'
        return render_template('transferencias.html', transferencias=[], mensaje=mensaje)
    if request.method == 'POST':
        destino = request.form.get('destino')
        monto = float(request.form.get('monto'))
        from services.transference_service import realizar_transferencia
        ok, mensaje = realizar_transferencia(current_user.username, destino, monto)
    # Mostrar historial
    transferencias = []
    try:
        with open('data/transferencias.json', 'r', encoding='utf-8') as f:
            todas = json.load(f)
            transferencias = [t for t in todas if t['origen'] == current_user.username or t['destino'] == current_user.username]
    except Exception:
        pass
    return render_template('transferencias.html', transferencias=transferencias, mensaje=mensaje)

@app.route('/qr', methods=['GET', 'POST'])
@login_required
def qr():
    qr_path = None
    qr_data = None
    mensaje = None
    if request.method == 'POST':
        if 'monto' in request.form:
            monto = request.form.get('monto')
            monto = float(monto) if monto else None
            qr_path = generar_qr_pago(current_user.username, monto)
        elif 'qr_img' in request.files:
            file = request.files['qr_img']
            if file and file.filename:
                filename = secure_filename(file.filename)
                filepath = f'data/qr_codes/{filename}'
                file.save(filepath)
                qr_data = leer_qr_pago(filepath)
                if qr_data:
                    mensaje = f"QR leído: Usuario destino: {qr_data['usuario']}, Monto: {qr_data['monto']}, Fecha: {qr_data['fecha']}"
                else:
                    mensaje = "No se pudo leer el QR."
    return render_template('qr.html', qr_path=qr_path, qr_data=qr_data, mensaje=mensaje)

@app.route('/qr_img/<path:filename>')
@login_required
def qr_img(filename):
    return send_file(f'data/qr_codes/{filename}', mimetype='image/png')

@app.route('/perfil')
@login_required
def perfil():
    return render_template('perfil.html')

@app.route('/cuentas', methods=['GET', 'POST'])
@login_required
def cuentas():
    mensaje = None
    # Agregar nueva cuenta
    if request.method == 'POST' and 'cbu' in request.form:
        cbu = request.form.get('cbu')
        alias = request.form.get('alias')
        bancos = cargar_bancos()
        banco_encontrado = None
        if not cbu or len(cbu) != 22 or not cbu.isdigit():
            mensaje = 'CBU inválido. Debe tener 22 dígitos numéricos.'
        else:
            for nombre, codigo in bancos.items():
                if cbu.startswith(codigo):
                    banco_encontrado = nombre
                    break
            if not banco_encontrado:
                mensaje = 'El CBU no coincide con ningún banco registrado.'
            else:
                # Guardar la cuenta en el JSON
                cuentas = []
                if os.path.exists(accounts_file):
                    with open(accounts_file, 'r', encoding='utf-8') as f:
                        cuentas = json.load(f)
                es_principal = not any(c['usuario'] == current_user.username for c in cuentas)
                cuentas.append({
                    "usuario": current_user.username,
                    "banco": banco_encontrado,
                    "cbu": cbu,
                    "alias": alias,
                    "principal": es_principal
                })
                if es_principal:
                    for c in cuentas:
                        if c['usuario'] == current_user.username and c is not cuentas[-1]:
                            c['principal'] = False
                with open(accounts_file, 'w', encoding='utf-8') as f:
                    json.dump(cuentas, f, indent=2)
                mensaje = f'Cuenta de {banco_encontrado} agregada exitosamente.'
    # Cambiar principal
    if request.method == 'POST' and 'principal_cbu' in request.form:
        cbu_principal = request.form.get('principal_cbu')
        marcar_principal(current_user.username, cbu_principal)
        mensaje = 'Cuenta principal actualizada.'
    # Mostrar cuentas vinculadas del usuario actual
    cuentas = []
    try:
        with open('data/cuentas.json', 'r', encoding='utf-8') as f:
            todas = json.load(f)
            cuentas = [c for c in todas if c['usuario'] == current_user.username]
    except Exception:
        pass
    return render_template('cuentas.html', cuentas=cuentas, mensaje=mensaje)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 