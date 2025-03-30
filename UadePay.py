import os
import hashlib

# Directorio donde se guardarán los datos
data_dir = "data"
users_file = os.path.join(data_dir, "usuarios.txt")
accounts_file = os.path.join(data_dir, "cuentas.txt")

# Asegurar que el directorio existe
os.makedirs(data_dir, exist_ok=True)

bancos_file = os.path.join(data_dir, "bancos.txt")

# Crear el archivo de bancos si no existe
if not os.path.exists(bancos_file):
    with open(bancos_file, "w") as f:
        f.write("072|Santander\n017|BBVA\n007|Galicia\n285|Macro\n011|Nación\n")

def cargar_bancos():
    """Carga los bancos desde el archivo bancos.txt."""
    bancos = {}
    if os.path.exists(bancos_file):
        with open(bancos_file, "r") as f:
            for line in f:
                codigo, nombre = line.strip().split("|")
                bancos[nombre] = codigo
    return bancos

def hash_password(password):
    """Devuelve el hash SHA256 de una contraseña."""
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_usuario():
    """Registra un nuevo usuario."""
    username = input("Ingrese un nombre de usuario: ")
    password = input("Ingrese una contraseña: ")
    hashed_password = hash_password(password)
    
    # Verificar si el usuario ya existe
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            for line in f:
                stored_user, _ = line.strip().split("|")
                if stored_user == username:
                    print("\n⚠️ Usuario ya registrado. Pruebe con otro nombre.\n")
                    return
    
    # Guardar usuario en el archivo
    with open(users_file, "a") as f:
        f.write(f"{username}|{hashed_password}\n")
    
    print("\n✅ Registro exitoso. Ahora puede iniciar sesión.\n")

def iniciar_sesion():
    """Permite a un usuario iniciar sesión."""
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    hashed_password = hash_password(password)
    
    if not os.path.exists(users_file):
        print("\n⚠️ No hay usuarios registrados aún.\n")
        return None
    
    with open(users_file, "r") as f:
        for line in f:
            stored_user, stored_hash = line.strip().split("|")
            if stored_user == username and stored_hash == hashed_password:
                print("\n✅ Inicio de sesión exitoso.\n")
                return username
    
    print("\n❌ Usuario o contraseña incorrectos.\n")
    return None

def cerrar_sesion():
    """Cierra la sesión del usuario."""
    print("\n👋 Sesión cerrada. Hasta luego!\n")
    return None

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

def main():
    """Menú principal del sistema."""
    usuario_actual = None
    
    while True:
        print("\n=== UADE-Pay ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Cerrar sesión")
        print("4. Vincular cuenta bancaria")
        print("5. Mostrar cuentas bancarias")
        print("6. Salir")
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            usuario_actual = iniciar_sesion()
        elif opcion == "3":
            usuario_actual = cerrar_sesion()
        elif opcion == "4":
            if usuario_actual:
                vincular_cuenta(usuario_actual)
            else:
                print("\n⚠️ Debe iniciar sesión primero.\n")
        elif opcion == "5":
            if usuario_actual:
                mostrar_cuentas(usuario_actual)
            else:
                print("\n⚠️ Debe iniciar sesión primero.\n")
        elif opcion == "6":
            print("\n👋 Gracias por usar UADE-Pay!\n")
            break
        else:
            print("\n⚠️ Opción inválida. Intente nuevamente.\n")

if __name__ == "__main__":
    main()
