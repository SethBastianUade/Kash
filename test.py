import os
import hashlib
from services import cuenta_service, usuario_service

# Directorio donde se guardaran los datos
data_dir = "data"
users_file = os.path.join(data_dir, "usuarios.txt")
accounts_file = os.path.join(data_dir, "cuentas.txt")

# Directorio donde se guarda la logica de negocio
services_dir = "services"

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


def cerrar_sesion():
    """Cierra la sesión del usuario."""
    print("\n👋 Sesión cerrada. Hasta luego!\n")
    return None



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
            usuario_service.registrar_usuario()
        elif opcion == "2":
            usuario_actual = usuario_service.iniciar_sesion()
        elif opcion == "3":
            usuario_actual = cerrar_sesion()
        elif opcion == "4":
            if usuario_actual:
                cuenta_service.vincular_cuenta(usuario_actual)
            else:
                print("\n⚠️ Debe iniciar sesión primero.\n")
        elif opcion == "5":
            if usuario_actual:
                cuenta_service.mostrar_cuentas(usuario_actual)
            else:
                print("\n⚠️ Debe iniciar sesión primero.\n")
        elif opcion == "6":
            print("\n👋 Gracias por usar UADE-Pay!\n")
            break
        else:
            print("\n⚠️ Opción inválida. Intente nuevamente.\n")

if __name__ == "__main__":
    main()
