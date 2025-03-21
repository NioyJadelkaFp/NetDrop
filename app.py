from flask import Flask, redirect, render_template, send_file, request
from Funciones import Qr_Generator
from Funciones import Show_File as Show_File
import os

Files_Carpet = './static/File'

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
    file = request.files['file']
    file.save(Files_Carpet + file.filename)
    redirect('/update')
    return 



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)