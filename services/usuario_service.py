import hashlib
import os
data_dir = "data"
users_file = os.path.join(data_dir, "usuarios.txt")

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
