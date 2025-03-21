import qrcode as qr
import socket as sok

def Generar_QR():
    # Obtenemos la dirección IP de la máquina
    hostname = sok.gethostname()
    Ip = sok.gethostbyname(hostname)

    Urls = "http://" + Ip + ":5000/"

    New_QR = qr.QRCode(version=1, box_size=100, border=0)
    New_QR.add_data(Urls)
    New_QR.make(fit=True)

    img = New_QR.make_image(fill='black', back_color='white')

    img.save('./static/QR/Qr.jpg')
