import hashlib
import os
from services import saldo_service
data_dir = "data"
users_file = os.path.join(data_dir, "usuarios.txt")

#Modulo que gestione el inicio de sesion y el registro de usuarios

# Funcion para hashear la contraseña del usuario utilizando SHA256 de la librearia hashlib
def hash_password(password):
    # Devuelve el hash SHA256 de una contraseña
    return hashlib.sha256(password.encode()).hexdigest()

def registrar_usuario():
    # Registra un nuevo usuario
    username = input("Ingrese un nombre de usuario: ")
    password = input("Ingrese una contraseña: ")
    hashed_password = hash_password(password)
    # Se le asigna el saldo incial al usuario
    referido = input("¿Fue referido por otro usuario? (s/n): ")
    if referido == "s":
        referido_username = input("Ingrese el nombre de usuario del referido: ")
        saldo_service.asignar_saldo_inicial(username,True)
    elif referido == "n":
        saldo_service.asignar_saldo_inicial(username,False)
    else:
        print("⚠️ Opción invalida.")

    # Verificar si el usuario ya existe
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            for line in f:
                stored_user, _ = line.strip().split("|")
                if stored_user == username:
                    print("\n⚠️ Usuario ya registrado. Pruebe con otro nombre.\n")
                    return
                
    # Guardar el usuario y la contraseña encriptada en el archivo
    with open(users_file, "a") as f:
        f.write(f"{username}|{hashed_password}\n")
    
    print("\n✅ Registro exitoso. Ahora puede iniciar sesión.\n")
    print("✅ Su saldo actual es:", saldo_service.obtener_saldo(username), "\n")


def iniciar_sesion():
    #Permite a un usuario iniciar sesión
    username = input("Ingrese su nombre de usuario: ")
    password = input("Ingrese su contraseña: ")
    hashed_password = hash_password(password)
    
    if not os.path.exists(users_file):
        print("\n⚠️ No hay usuarios registrados aún.\n")
        return None
    
    # Abre el archivo de usuarios y verifica que el usuario y la contraseña
    with open(users_file, "r") as f:
        for line in f:
            stored_user, stored_hash = line.strip().split("|")
            if stored_user == username and stored_hash == hashed_password:
                print("\n✅ Inicio de sesión exitoso.\n")
                return username
    
    print("\n❌ Usuario o contraseña incorrectos.\n")
    return None

def verificar_usuario(username, password):
    """
    Verifica las credenciales de un usuario para el login web.
    Retorna un diccionario con la información del usuario si las credenciales son correctas,
    o None si son incorrectas.
    """
    if not os.path.exists(users_file):
        return None
    
    hashed_password = hash_password(password)
    
    with open(users_file, "r") as f:
        for line in f:
            stored_user, stored_hash = line.strip().split("|")
            if stored_user == username and stored_hash == hashed_password:
                return {
                    'id': username,  # Usando username como ID por ahora
                    'username': username,
                    'nombre': username  # Por ahora usamos el username como nombre
                }
    
    return None

