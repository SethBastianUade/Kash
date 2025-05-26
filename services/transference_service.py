#Modulo para gestionar transferencias entre usuarios
# transferencia_service.py
import uuid
import json
import os
from services.saldo_service import obtener_saldo, actualizar_saldo
from services.cuenta_service import accounts_file
#from services.usuario_service import obtener_usuario_por_alias

TRANSFERENCIAS_PATH = 'data/transferencias.json'

# Funcion lambda para generar codigo unico de transferencia
generar_codigo_transferencia = lambda: f"RC-{str(uuid.uuid4())[:8]}"

def usuario_tiene_cuenta(usuario):
    if not os.path.exists(accounts_file):
        return False
    with open(accounts_file, 'r', encoding='utf-8') as f:
        cuentas = json.load(f)
    return any(c['usuario'] == usuario for c in cuentas)

# Funcion para realizar una transferencia entre usuarios, se le agregara un token en el futuro para confirmar la transferencia
def realizar_transferencia(usuario_origen, usuario_destino, monto):
    if not usuario_destino:
        return False, "❌ Alias destino no encontrado."
    if usuario_origen == usuario_destino:
        return False, "❌ No puedes transferirte a ti mismo."
    if monto is None or monto <= 0:
        return False, "❌ El monto debe ser mayor a cero."
    if not usuario_tiene_cuenta(usuario_destino):
        return False, "❌ El usuario destino no tiene cuentas bancarias vinculadas."
    saldo_origen = obtener_saldo(usuario_origen)
    if saldo_origen < monto:
        return False, "❌ Saldo insuficiente."
    saldo_destino = obtener_saldo(usuario_destino)
    codigo = generar_codigo_transferencia()
    actualizar_saldo(usuario_origen, saldo_origen - monto)
    actualizar_saldo(usuario_destino, saldo_destino + monto)
    if os.path.exists(TRANSFERENCIAS_PATH):
        with open(TRANSFERENCIAS_PATH, 'r', encoding='utf-8') as f:
            transferencias = json.load(f)
    else:
        transferencias = []
    transferencias.append({
        "codigo": codigo,
        "origen": usuario_origen,
        "destino": usuario_destino,
        "monto": monto
    })
    with open(TRANSFERENCIAS_PATH, 'w', encoding='utf-8') as f:
        json.dump(transferencias, f, indent=2)
    return True, f"✅ Transferencia realizada con éxito. Código: {codigo}"
