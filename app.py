from flask import Flask, redirect, render_template, send_file, request, jsonify, session
from Funciones import Show_File as Show_File
from flask_socketio import SocketIO
import os
import json
import secrets

Files_Carpet = './static/File/'
app = Flask(__name__)
app.secret_key = secrets.token_hex(16)
socketio = SocketIO(app)

REACTIONS_FILE = 'reactions.json'

USER_REACTIONS_FILE = 'user_reactions.json'

def init_reactions():
    if not os.path.exists(REACTIONS_FILE):
        with open(REACTIONS_FILE, 'w') as f:
            json.dump({}, f)
    

    with open(REACTIONS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def init_user_reactions():
    if not os.path.exists(USER_REACTIONS_FILE):
        with open(USER_REACTIONS_FILE, 'w') as f:
            json.dump({}, f)
    

    with open(USER_REACTIONS_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}


def save_reactions(reactions_data):
    with open(REACTIONS_FILE, 'w') as f:
        json.dump(reactions_data, f)


def save_user_reactions(user_reactions_data):
    with open(USER_REACTIONS_FILE, 'w') as f:
        json.dump(user_reactions_data, f)

@app.route('/login')
def Login():
    return render_template('Login.html')

@app.route('/')
def index():

    if 'user_id' not in session:
        session['user_id'] = secrets.token_hex(8) 

    File = Show_File.Show_File()
    reactions = init_reactions()
    user_reactions = init_user_reactions()
    user_id = session['user_id']

    for file in File:
        file_id = file['nombre']
        if file_id in reactions:
            file['likes'] = reactions[file_id].get('likes', 0)
            file['dislikes'] = reactions[file_id].get('dislikes', 0)
            file['love'] = reactions[file_id].get('love', 0)
            file['laugh'] = reactions[file_id].get('laugh', 0)

            file['user_reacted'] = False
            file['user_reaction'] = None
            
            if user_id in user_reactions and file_id in user_reactions[user_id]:
                file['user_reacted'] = True
                file['user_reaction'] = user_reactions[user_id][file_id]
        else:
            file['likes'] = 0
            file['dislikes'] = 0
            file['love'] = 0
            file['laugh'] = 0
            file['user_reacted'] = False
            file['user_reaction'] = None

        # Calcula el total de reacciones
        file['total_reacciones'] = file['likes'] + file['dislikes'] + file['love'] + file['laugh']

    # Ordenar la lista por total de reacciones (de mayor a menor)
    File.sort(key=lambda f: f['total_reacciones'], reverse=True)

    return render_template('index.html', File=File)


@app.route('/react/<string:file_name>/<string:reaction_type>', methods=['POST'])
def react_to_file(file_name, reaction_type):
    if request.method == 'POST':

        if 'user_id' not in session:
            session['user_id'] = secrets.token_hex(8)
        
        user_id = session['user_id']
        reactions = init_reactions()
        user_reactions = init_user_reactions()
        

        if file_name not in reactions:
            reactions[file_name] = {'likes': 0, 'dislikes': 0, 'love': 0, 'laugh': 0}
        

        valid_reactions = ['likes', 'dislikes', 'love', 'laugh']
        if reaction_type not in valid_reactions:
            return jsonify({"error": "Invalid reaction type"}), 400
        

        if user_id in user_reactions and file_name in user_reactions[user_id]:
            old_reaction = user_reactions[user_id][file_name]
            if old_reaction == reaction_type:

                reactions[file_name][reaction_type] -= 1
                del user_reactions[user_id][file_name]
                if not user_reactions[user_id]:  
                    del user_reactions[user_id]
            else:

                reactions[file_name][old_reaction] -= 1
                reactions[file_name][reaction_type] += 1
                user_reactions[user_id][file_name] = reaction_type
        else:

            reactions[file_name][reaction_type] += 1
            if user_id not in user_reactions:
                user_reactions[user_id] = {}
            user_reactions[user_id][file_name] = reaction_type
        
        save_reactions(reactions)
        save_user_reactions(user_reactions)
        

        response_data = reactions[file_name].copy()
        if user_id in user_reactions and file_name in user_reactions[user_id]:
            response_data['user_reaction'] = user_reactions[user_id][file_name]
        else:
            response_data['user_reaction'] = None
        
        return jsonify(response_data)

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
    with open('Comunicados.json', 'r') as file:
        comunicados = json.load(file)
    return render_template('Comunicados.html', comunicados=comunicados)

@app.errorhandler(404)
def pagina_no_encontrada(error):
    return render_template('404.html')

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000)

