import qrcode as qr
import socket as sok
from PIL import Image

def Generar_QR():
    # Obtenemos la dirección IP de la máquina
    hostname = sok.gethostname()
    Ip = sok.gethostbyname(hostname)

    Urls = "http://" + Ip + ":5000/"

    New_QR = qr.QRCode(version=1, box_size=100, border=0)
    New_QR.add_data(Urls)
    New_QR.make(fit=True)

    img = New_QR.make_image(fill='black', back_color='white')

    logo = Image.open("./static/Logo/icono.png")

    imgW, imgH = img.size
    Logo_size = imgW // 4
    logo = logo.resize((Logo_size, Logo_size))

    logo_x = (imgW - Logo_size) // 2
    logo_y = (imgH - Logo_size) // 2

    img.paste(logo,(logo_x,logo_y), logo)

    img.save('./static/QR/Qr.png')

