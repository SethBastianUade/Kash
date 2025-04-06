import os
from services import cuenta_service, usuario_service, saldo_service

# Directorio donde se guardaran los datos
data_dir = "data"
users_file = os.path.join(data_dir, "usuarios.txt")
accounts_file = os.path.join(data_dir, "cuentas.txt")
bancos_file = os.path.join(data_dir, "bancos.txt")

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
        print("6. Consultar saldo")
        print("7. Salir")
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
            saldo_service.obtener_saldo(usuario_actual)
        elif opcion == "7":
            print("\n👋 Gracias por usar UADE-Pay!\n")
            break
        else:
            print("\n⚠️ Opción inválida. Intente nuevamente.\n")

main()
