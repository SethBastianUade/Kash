import qrcode
import json
import os
from datetime import datetime

def generar_qr_pago(usuario, monto=None):
    """
    Genera un código QR para recibir pagos.
    
    Args:
        usuario (str): Usuario que recibirá el pago
        monto (float, optional): Monto específico a recibir
    
    Returns:
        str: Ruta del archivo QR generado
    """
    # Crear directorio para QRs si no existe
    qr_dir = "data/qr_codes"
    if not os.path.exists(qr_dir):
        os.makedirs(qr_dir)
    
    # Crear datos del QR
    qr_data = {
        "usuario": usuario,
        "monto": monto,
        "fecha": datetime.now().isoformat()
    }
    
    # Generar QR
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(json.dumps(qr_data))
    qr.make(fit=True)
    
    # Crear imagen
    qr_image = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar QR
    filename = f"qr_{usuario}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    filepath = os.path.join(qr_dir, filename)
    qr_image.save(filepath)
    
    return filepath

def leer_qr_pago(imagen_path):
    """
    Lee un código QR de pago.
    
    Args:
        imagen_path (str): Ruta de la imagen del QR
    
    Returns:
        dict: Datos del QR (usuario, monto, fecha)
    """
    try:
        import cv2
        from pyzbar.pyzbar import decode
        
        # Leer imagen
        imagen = cv2.imread(imagen_path)
        decoded_objects = decode(imagen)
        
        if not decoded_objects:
            return None
            
        # Decodificar datos
        qr_data = json.loads(decoded_objects[0].data.decode('utf-8'))
        return qr_data
        
    except Exception as e:
        print(f"Error al leer QR: {str(e)}")
        return None 