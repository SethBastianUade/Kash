import os
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

def mostrar_cuentas(usuario):
    """Muestra las cuentas bancarias vinculadas del usuario."""
    if not os.path.exists(accounts_file):
        print("\n⚠️ No hay cuentas registradas aún.\n")
        return
    
    print(f"\n💳 Cuentas vinculadas de {usuario}:")
    with open(accounts_file, "r") as f:
        for line in f:
            stored_user, banco, cbu, alias = line.strip().split("|")
            if stored_user == usuario:
                print(f"🏦 {banco} - CBU: {cbu} - Alias: {alias}")