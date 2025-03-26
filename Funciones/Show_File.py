import os

def Show_File():
    Ruta = './static/File'
    archivos = []

    if os.path.exists(Ruta):  # Verifica si la carpeta existe
        for archivo in os.scandir(Ruta):
            if archivo.is_file():  # Asegura que sea un archivo
                archivos.append({
                    "nombre": archivo.name,
                    "ruta": f"/static/File/{archivo.name}",  # Ruta accesible desde la web
                    "tipo": archivo.name.split(".")[-1].lower()  # Extensión del archivo
                })

    return archivos