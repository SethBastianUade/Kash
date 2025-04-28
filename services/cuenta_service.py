import os
from functools import reduce
data_dir = "data"

users_file = os.path.join(data_dir, "usuarios.txt")
accounts_file = os.path.join(data_dir, "cuentas.txt")
bancos_file = os.path.join(data_dir, "bancos.txt")

def cargar_bancos():
    """Carga los bancos desde el archivo bancos.txt."""
    bancos = {}
    if os.path.exists(bancos_file):
        with open(bancos_file, "r") as f:
            for line in f:
                codigo, nombre = line.strip().split("|")
                bancos[nombre] = codigo
    return bancos

def vincular_cuenta(usuario):
    """Permite al usuario vincular una cuenta bancaria."""
    bancos = cargar_bancos()
    print("\n🏦 Bancos disponibles:")
    for banco, codigo in bancos.items():
        print(f"{banco}: {codigo}")
 
    cbu = input("Ingrese su CBU (22 dígitos): ")
    if len(cbu) != 22 or not cbu.isdigit():
        print("\n❌ CBU inválido. Debe tener 22 dígitos numéricos.\n")
        return
    
    # Verificar que el CBU coincide con algún banco
    banco_encontrado = None
    for banco, codigo in bancos.items():
        if cbu.startswith(codigo):
            banco_encontrado = banco
            break
    
    if not banco_encontrado:
        print("\n⚠️ CBU no coincide con ningún banco registrado.\n")
        return
    
    alias = input("Ingrese un alias para su cuenta: ")
    
    # Guardar cuenta en archivo
    with open(accounts_file, "a") as f:
        f.write(f"{usuario}|{banco_encontrado}|{cbu}|{alias}\n")
    
    print(f"\n✅ Cuenta de {banco_encontrado} vinculada exitosamente!\n")

"""def mostrar_cuentas(usuario):
    #Muestra las cuentas bancarias vinculadas del usuario.
    if not os.path.exists(accounts_file):
        print("\n⚠️ No hay cuentas registradas aún.\n")
        return
    """

#Funcion modificada para realizar los temas vistos en clase
def mostrar_cuentas(usuario):
   # Muestra las cuentas vinculadas de los usuarios.
    
    # Lee las cuentas desde el txt cuentas.txt y crea una lista de tuplas
    with open(accounts_file, "r", encoding="utf-8") as f:
        cuentas = [
            tuple(line.strip().split("|"))
            for line in f
            if "|" in line
        ]

    # Utilizamos comprension de listas y la funcion filter para filtrar las cuentas del usuario y la convertimos en una lista
    user_accounts = list(filter(lambda c: c[0] == usuario, cuentas))

    # Acá utilizamos el desempaquetado para obtener los datos
    alias_bancos = [(alias, banco) for (_, banco, _, alias) in user_accounts]

    # Map para crear strings de presentación
    user_bank_account = list(map(lambda tupla: f"🏦 {tupla[1]} - CBU: {tupla[2]} - Alias: {tupla[3]}",user_accounts))

    # Ordena alfabéticamente por banco
    detalles_sorted = sorted(user_bank_account, key=lambda s: s.split(" ")[1])

    # Utilzamos slice para mostrar las últimas 5 cuentas
    ultimas = detalles_sorted[-5:]

    # Reduce para contar cuántas cuentas tiene el usuario reduce(funcion, iterable, valor inicial)
    cuenta_count = reduce(lambda acc, _: acc + 1, user_accounts, 0)

    # Matriz de datos bancarios (lista de listas) queda cada fila: [banco, cbu, alias]
    matriz = [list(c[1:]) for c in user_accounts]

    # Muestra por consola la info
    print(f"\n🔢 Total de cuentas vinculadas: {cuenta_count}")

    print("\n📊 Matriz de cuentas (Banco, CBU, Alias):")
    for fila in matriz:
        print(fila)

    print("\n📋 Detalles de las últimas cuentas (ordenadas):")
    for det in ultimas:
        print(det)

    print(f"\n💳 Cuentas vinculadas de {usuario}:")
    with open(accounts_file, "r") as f:
        for line in f:
            stored_user, banco, cbu, alias = line.strip().split("|")
            if stored_user == usuario:
                print(f"🏦 {banco} - CBU: {cbu} - Alias: {alias}")