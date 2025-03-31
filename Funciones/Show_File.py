import os

def Show_File():
    Ruta = './static/File'
    archivos = []

    if os.path.exists(Ruta):
        # Ordenar archivos alfabéticamente para evitar sesgos
        lista_archivos = sorted(os.listdir(Ruta))
        
        for nombre_archivo in lista_archivos:
            ruta_completa = os.path.join(Ruta, nombre_archivo)
            
            # Verificar que sea un archivo
            if os.path.isfile(ruta_completa):
                archivos.append({
                    "nombre": nombre_archivo,
                    "ruta": f"/static/File/{nombre_archivo}",
                    "tipo": nombre_archivo.split(".")[-1].lower() if '.' in nombre_archivo else ''
                })

    return archivos