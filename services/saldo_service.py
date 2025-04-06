import os
data_dir = "data"
SALDOS_PATH = os.path.join(data_dir, "saldos.txt")

#Modulo que gestiona el saldo de los usuarios, incluyendo la asignacion de saldo inicial y la actualizacion del saldo

def asignar_saldo_inicial(username, con_referido=False):
    if con_referido:
        saldo_inicial = 5000
    else: 
        saldo_inicial = 1000
    with open(SALDOS_PATH, 'a') as f:
        f.write(f'{username}:{saldo_inicial}\n')

def obtener_saldo(username):
    with open(SALDOS_PATH, 'r') as f:
        for linea in f:
            user, saldo = linea.strip().split(':')
            if user == username:
                return float(saldo)
    return None

def actualizar_saldo(username, nuevo_saldo):
    lineas = []
    with open(SALDOS_PATH, 'r') as f:
        lineas = f.readlines()

    with open(SALDOS_PATH, 'w') as f:
        for linea in lineas:
            user, saldo = linea.strip().split(':')
            if user == username:
                f.write(f'{username}:{nuevo_saldo}\n')
            else:
                f.write(f'{user}:{saldo}\n')
