import os

def Show_File():
    Ruta = './static/File'
    File = os.scandir(Ruta)
    return File