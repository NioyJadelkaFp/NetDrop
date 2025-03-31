from cv2 import broadcast
from flask import Flask, redirect, render_template, send_file, request
from Funciones import Qr_Generator
from Funciones import Show_File as Show_File
from flask_socketio import SocketIO, send
import os
import webbrowser
import socket as sok

Files_Carpet = './static/File/'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'
socketio = SocketIO(app)

Qr_Generator.Generar_QR()

@app.route('/')
def index():
    File = Show_File.Show_File()
    return render_template('index.html', File=File)

@app.route('/descarga/<string:File>', methods=['GET'])
def Descarga(File=''):
    if request.method == 'GET':
        try:
            Base_Ruta = os.path.dirname(__file__)
            Url_File = os.path.join(Base_Ruta, 'static/File', File)
            
            # Verificaciones de seguridad
            if not os.path.exists(Url_File):
                return "Archivo no encontrado", 404
            
            if not os.path.isfile(Url_File):
                return "No es un archivo válido", 400
            
            # Enviar archivo para descarga
            return send_file(Url_File, as_attachment=True, download_name=File)
        
<<<<<<< Updated upstream
        except Exception as e:
            # Loguear error
            print(f"Error al descargar archivo: {e}")
            return "Error al procesar la descarga", 500
    else:
        # Si no es GET, redirigir de vuelta a la página principal
        return redirect('/')

=======
        # Verificaciones de seguridad
        if not os.path.exists(Url_File):
            return "Archivo no encontrado", 404
        
        if not os.path.isfile(Url_File):
            return "No es un archivo válido", 400
        
        # Enviar archivo sin forzar la descarga
        return send_file(Url_File, mimetype="application/octet-stream")  # O el tipo adecuado para el archivo
    
    except Exception as e:
        print(f"Error al procesar la descarga: {e}")
        return "Error al procesar la descarga", 500
>>>>>>> Stashed changes


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

@app.route('/chat')
def chat():
    return render_template('Chat.html')

@socketio.on('message')
def Message(msg):
    send(msg, broadcast = True)

if __name__ == '__main__':
    Qr_Generator.Generar_QR()
    socketio.run(app,host="0.0.0.0", port=5000, debug=True )