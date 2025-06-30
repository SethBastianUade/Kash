import os
import json
data_dir = "data"
SALDOS_PATH = os.path.join(data_dir, "saldos.json")
USERS_FILE = os.path.join(data_dir, "usuarios.json")

#Gestiona el saldo de los usuarios

def usuario_existe(username):
    """Verifica si un usuario existe en el sistema."""
    if not os.path.exists(USERS_FILE):
        return False
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        try:
            users = json.load(f)
        except json.JSONDecodeError:
            return False
    return username in users

# Asigna un saldo inicial a los usuarios al registrarse, si el usuario fue referido inicia con mas saldo
def asignar_saldo_inicial(username, con_referido=False, referido_username=None):
    if os.path.exists(SALDOS_PATH):
        with open(SALDOS_PATH, 'r', encoding='utf-8') as f:
            saldos = json.load(f)
    else:
        saldos = {}
    
    # Validar que el referido 
    if con_referido and referido_username:
        if not usuario_existe(referido_username):
            # Si el referido no existe, asignar saldo normal 
            saldo_inicial = 1000
            saldos[username] = saldo_inicial
            with open(SALDOS_PATH, 'w', encoding='utf-8') as f:
                json.dump(saldos, f, indent=2)
            return False, f"El usuario referido '{referido_username}' no existe. Se asignó saldo normal."
    
    saldo_inicial = 5000 if con_referido else 1000
    saldos[username] = saldo_inicial
    # Si hay referido, ambos ganan $2000 extra
    if con_referido and referido_username:
        saldos[username] += 2000
        if referido_username in saldos:
            saldos[referido_username] += 2000
        else:
            saldos[referido_username] = 2000
    
    with open(SALDOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(saldos, f, indent=2)
    
    return True, "Saldo asignado correctamente"

# Obtenemos el saldo del usuario, y si no existe devolvemos None
def obtener_saldo(username):
    if not os.path.exists(SALDOS_PATH):
        return None
    with open(SALDOS_PATH, 'r', encoding='utf-8') as f:
        saldos = json.load(f)
    return float(saldos.get(username, 0.0))

# Actualiza los saldos 
def actualizar_saldo(username, nuevo_saldo):
    if os.path.exists(SALDOS_PATH):
        with open(SALDOS_PATH, 'r', encoding='utf-8') as f:
            saldos = json.load(f)
    else:
        saldos = {}
    saldos[username] = nuevo_saldo
    with open(SALDOS_PATH, 'w', encoding='utf-8') as f:
        json.dump(saldos, f, indent=2)
