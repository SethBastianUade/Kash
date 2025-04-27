Integrantes:
   Sebastián Arroyo
   Sebastián Jorge
   Agustín Hoffmann
   Juan Ventola
 
 Objetivo: Desarrollar una aplicación funcional basada en Python que permita realizar pagos digitales y transferencias bancarias de forma fácil y segura.
 
 Funcionalidades principales
 •	Registro de usuario: Creación de cuenta con username, contraseña y posibilidad de ingresar un código de referido.
 •	Inicio de sesión: Acceso a la plataforma con credenciales registradas.
 •	Vinculación de cuentas bancarias: Asociación de cuentas mediante CBU, verificando que el número pertenezca al banco correspondiente.
 •	Gestión de saldo: Cada usuario inicia con $1000 y puede realizar transacciones con otros usuarios.
 •	Transferencias: Permite transferir saldo entre usuarios de Kash, validando la existencia de la cuenta destino y confirmando la operación con clave TOKEN.
 •	Sistema de referidos: Otorga $5000 de reintegro en pagos a los usuarios que ingresen un código de referido al registrarse
 
 Entregables
 Fase |	Características incluidas
 40%	|  Registro, inicio de sesión, vinculación de cuentas bancarias y gestión de saldo inicial.
 80%	|  Transferencias entre usuarios, validación de cuenta destino y sistema de referidos.
 100% |	Implementación de logs de transferencias, implementación de sistema de seguridad y mejorar la experiencia del usuario con una interfaz grafica

UADE-Pay/
│── ui/
│   ├── app.py  # Punto de entrada, interfaz de usuario
│── services/
│   ├── usuario_service.py  # Lógica de usuarios
│   ├── cuenta_service.py   # Lógica de cuentas bancarias
│   ├── transaccion_service.py  # Lógica de transferencias
│── data/
│   ├── usuario_repository.py  # Manejo de archivos para usuarios
│   ├── transaccion_repository.py  # Manejo de archivos para transacciones
│── utils/
│   ├── helpers.py  # Funciones auxiliares como generación de códigos únicos
│── main.py  # Ejecuta la aplicación
