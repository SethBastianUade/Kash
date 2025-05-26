import os
import json
from functools import reduce

data_dir = "data"
accounts_file = os.path.join(data_dir, "cuentas.json")
bancos_file = os.path.join(data_dir, "bancos.json")

def cargar_bancos():
    """Carga los bancos desde el archivo bancos.json."""
    bancos = {}
    if os.path.exists(bancos_file):
        with open(bancos_file, "r", encoding="utf-8") as f:
            bancos_list = json.load(f)
            for banco in bancos_list:
                bancos[banco["nombre"]] = banco["codigo"]
    return bancos

def vincular_cuenta(usuario):
    bancos = cargar_bancos()
    print("\n🏦 Bancos disponibles:")
    for banco, codigo in bancos.items():
        print(f"{banco}: {codigo}")
    cbu = input("Ingrese su CBU (22 dígitos): ")
    if len(cbu) != 22 or not cbu.isdigit():
        print("\n❌ CBU inválido. Debe tener 22 dígitos numéricos.\n")
        return
    banco_encontrado = None
    for banco, codigo in bancos.items():
        if cbu.startswith(codigo):
            banco_encontrado = banco
            break
    if not banco_encontrado:
        print("\n⚠️ CBU no coincide con ningún banco registrado.\n")
        return
    alias = input("Ingrese un alias para su cuenta: ")
    cuentas = []
    if os.path.exists(accounts_file):
        with open(accounts_file, "r", encoding="utf-8") as f:
            cuentas = json.load(f)
    # Si es la primera cuenta del usuario, la marcamos como principal
    es_principal = not any(c['usuario'] == usuario for c in cuentas)
    cuentas.append({
        "usuario": usuario,
        "banco": banco_encontrado,
        "cbu": cbu,
        "alias": alias,
        "principal": es_principal
    })
    # Solo una cuenta principal por usuario
    if es_principal:
        for c in cuentas:
            if c['usuario'] == usuario and c is not cuentas[-1]:
                c['principal'] = False
    with open(accounts_file, "w", encoding="utf-8") as f:
        json.dump(cuentas, f, indent=2)
    print(f"\n✅ Cuenta de {banco_encontrado} vinculada exitosamente!\n")

def marcar_principal(usuario, cbu):
    if not os.path.exists(accounts_file):
        return
    with open(accounts_file, "r", encoding="utf-8") as f:
        cuentas = json.load(f)
    for c in cuentas:
        if c['usuario'] == usuario:
            c['principal'] = (c['cbu'] == cbu)
    with open(accounts_file, "w", encoding="utf-8") as f:
        json.dump(cuentas, f, indent=2)

def mostrar_cuentas(usuario):
    if not os.path.exists(accounts_file):
        print("\n⚠️ No hay cuentas registradas aún.\n")
        return
    with open(accounts_file, "r", encoding="utf-8") as f:
        cuentas = json.load(f)
    user_accounts = list(filter(lambda c: c["usuario"] == usuario, cuentas))
    alias_bancos = [(c["alias"], c["banco"]) for c in user_accounts]
    user_bank_account = list(map(lambda c: f"🏦 {c['banco']} - CBU: {c['cbu']} - Alias: {c['alias']}", user_accounts))
    detalles_sorted = sorted(user_bank_account, key=lambda s: s.split(" ")[1])
    ultimas = detalles_sorted[-5:]
    cuenta_count = reduce(lambda acc, _: acc + 1, user_accounts, 0)
    matriz = [[c["banco"], c["cbu"], c["alias"]] for c in user_accounts]
    print(f"\n🔢 Total de cuentas vinculadas: {cuenta_count}")
    print("\n📊 Matriz de cuentas (Banco, CBU, Alias):")
    for fila in matriz:
        print(fila)
    print("\n📋 Detalles de las últimas cuentas (ordenadas):")
    for det in ultimas:
        print(det)
    print(f"\n💳 Cuentas vinculadas de {usuario}:")
    for c in user_accounts:
        principal = " (PRINCIPAL)" if c.get('principal') else ""
        print(f"🏦 {c['banco']} - CBU: {c['cbu']} - Alias: {c['alias']}{principal}")