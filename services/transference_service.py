#Modulo para gestionar transferencias entre usuarios
# transferencia_service.py
import uuid
from services.saldo_service import obtener_saldo, actualizar_saldo
#from services.usuario_service import obtener_usuario_por_alias

TRANSFERENCIAS_PATH = 'data/transferencias.txt'

# Funcion lambda para generar codigo unico de transferencia
generar_codigo_transferencia = lambda: f"RC-{str(uuid.uuid4())[:8]}"

# Funcion para realizar una transferencia entre usuarios, se le agregara un token en el futuro para confirmar la transferencia
def realizar_transferencia(usuario_origen, usuario_destino, monto):
    #usuario_destino = obtener_usuario_por_alias(alias_destino)

    if not usuario_destino:
        print("❌ Alias destino no encontrado.")
        return

    saldo_origen = obtener_saldo(usuario_origen)
    if saldo_origen < monto:
        print("❌ Saldo insuficiente.")
        return

    saldo_destino = obtener_saldo(usuario_destino)
    codigo = generar_codigo_transferencia()

    # Actualizar saldos
    actualizar_saldo(usuario_origen, saldo_origen - monto)
    actualizar_saldo(usuario_destino, saldo_destino + monto)

    # Registrar transferencia
    with open(TRANSFERENCIAS_PATH, 'a') as f:
        f.write(f"{codigo},{usuario_origen},{usuario_destino},{monto}\n")

    print(f"✅ Transferencia realizada con éxito. Código: {codigo}")
