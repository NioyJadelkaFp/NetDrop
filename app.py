from flask import Flask, redirect, render_template, send_file, request
from Funciones import Qr_Generator
from Funciones import Show_File as Show_File
import os
import webbrowser
import socket as sok

Files_Carpet = './static/File/'

app = Flask(__name__)

Qr_Generator.Generar_QR()

@app.route('/')
def index():
    File = Show_File.Show_File()
    return render_template('index.html', File=File)

@app.route('/descarga/<string:File>', methods=['GET', 'POST'])
def Descarga(File=''):
    Base_Ruta = os.path.dirname(__file__)
    Url_File = os.path.join(Base_Ruta, 'static/File', File)
    result = send_file(Url_File, as_attachment=True)
    return result

@app.route('/update')
def UpDate():
    return render_template('Up_Data.html')

@app.route('/qrgenerator')
def QR_Generador():
    return render_template('Qr_Generator.html')

@app.route('/qr')
def qr():
    Qr_Generator.Generar_QR()
    return redirect('/qrgenerator')

@app.route('/upload', methods=['POST'])
def update():
    if request.method == 'POST':   
        f = request.files['file'] 
        f.save(Files_Carpet+ f.filename) 
    return redirect('/update')

def abrir_navegador():
    # Obtenemos la dirección IP de la máquina
    hostname = sok.gethostname()
    Ip = sok.gethostbyname(hostname)

    Urls = "http://" + Ip + ":5000/"
    webbrowser.open(Urls)

#abrir_navegador()

if __name__ == '__main__':
    Qr_Generator.Generar_QR()
    app.run(host="0.0.0.0", port=5000, debug=True)