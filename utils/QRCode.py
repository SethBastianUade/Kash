import opencv as cv2

def escanear_qr():
    detector = cv2.QRCodeDetector()
    cap = cv2.VideoCapture(0)  
    tienda = None  # Inicializa la variable

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        datos, _, _ = detector.detectAndDecode(frame)

        if datos:
            tienda = datos
            print('La tienda a pagar es:', tienda)
            break  # Sale automáticamente al detectar un QR

    cap.release()
    cv2.destroyAllWindows