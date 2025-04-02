from flask import Flask, redirect, render_template, send_file, request
from Funciones import Show_File as Show_File
from flask_socketio import SocketIO
import os
import json

Files_Carpet = './static/File/'

app = Flask(__name__)
socketio = SocketIO(app)

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
        
        except Exception as e:
            # Loguear error
            print(f"Error al descargar archivo: {e}")
            return "Error al procesar la descarga", 500
    else:
        # Si no es GET, redirigir de vuelta a la página principal
        return redirect('/')


@app.route('/update')
def UpDate():
    return render_template('Up_Data.html')


@app.route('/upload', methods=['POST'])
def update():
    if request.method == 'POST':   
        # Obtener el archivo y el título desde el formulario
        f = request.files['file']
        title = request.form['title']  # El título proporcionado en el formulario
        
        # Renombrar el archivo con el título y mantener su extensión original
        file_extension = f.filename.split('.')[-1]  # Obtener la extensión del archivo
        new_filename = f"{title}.{file_extension}"  # Renombrar el archivo
        
        # Guardar el archivo con el nuevo nombre
        f.save(Files_Carpet + new_filename)
        
    return redirect('/update')

@app.route('/comunicados')
def Comunicados():
    with open('comunicados.json', 'r') as file:
        comunicados = json.load(file)
    return render_template('Comunicados.html',comunicados=comunicados)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html')

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', debug=True)

    #,host='0.0.0.0', debug=True