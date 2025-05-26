import os
from services import cuenta_service, usuario_service, saldo_service, transference_service, qr_service

# Directorio de donde se guardaran los datos
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
        print("6. Realizar transferencia")
        print("7. Consultar saldo")
        print("8. Generar código QR para recibir pago")
        print("9. Escanear código QR para pagar")
        print("10. Salir")
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
            if usuario_actual:
                usuario_destino = input("Ingrese el usuario de destino: ")
                usuario_origen = usuario_actual
                monto = int(input("Ingrese el monto a transferir: "))
                transference_service.realizar_transferencia(usuario_origen, usuario_destino, monto)
            else:
                print("\n⚠️ Debe iniciar sesión primero.\n")
        elif opcion == "7":
            if usuario_actual:
                saldo_service.obtener_saldo(usuario_actual)
            else:
                print("\n⚠️ Debe iniciar sesión primero.\n")
        elif opcion == "8":
            if usuario_actual:
                monto = input("Ingrese el monto a recibir (opcional, presione Enter para omitir): ")
                monto = float(monto) if monto else None
                qr_path = qr_service.generar_qr_pago(usuario_actual, monto)
                print(f"\n✅ Código QR generado exitosamente en: {qr_path}\n")
            else:
                print("\n⚠️ Debe iniciar sesión primero.\n")
        elif opcion == "9":
            if usuario_actual:
                imagen_path = input("Ingrese la ruta de la imagen del código QR: ")
                qr_data = qr_service.leer_qr_pago(imagen_path)
                if qr_data:
                    print(f"\n📱 Datos del QR:")
                    print(f"Usuario destino: {qr_data['usuario']}")
                    print(f"Monto: {qr_data['monto'] if qr_data['monto'] else 'A definir'}")
                    confirmar = input("\n¿Desea realizar el pago? (s/n): ")
                    if confirmar.lower() == 's':
                        monto = float(input("Ingrese el monto a transferir: ")) if not qr_data['monto'] else qr_data['monto']
                        transference_service.realizar_transferencia(usuario_actual, qr_data['usuario'], monto)
                else:
                    print("\n❌ No se pudo leer el código QR.\n")
            else:
                print("\n⚠️ Debe iniciar sesión primero.\n")
        elif opcion == "10":
            print("\n👋 Gracias por usar Kash!\n")
            break
        else:
            print("\n⚠️ Opción inválida. Intente nuevamente.\n")

if __name__ == "__main__":
    main()
