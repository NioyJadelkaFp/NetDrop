from flask import Flask, redirect, render_template
from Funciones import Qr_Generator

Qr_Generator.Generar_QR()

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')
@app.route('/qrgenerator')
def QR_Generador():
    return render_template('Qr_Generator.html')

@app.route('/qr')
def qr():
    Qr_Generator.Generar_QR()
    return redirect('/qrgenerator')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)