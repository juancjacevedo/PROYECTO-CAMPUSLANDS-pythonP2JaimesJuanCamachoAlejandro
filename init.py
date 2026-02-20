import json
import os

RUTA = os.path.join(os.path.dirname(__file__), '../DATOS/data.json')

def cargarDatos():
    try:
        with open(RUTA, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Archivo no encontrado")
        return None

def guardarDatos(data):
    try:
        with open(RUTA, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print("Datos guardados correctamente")
    except Exception as e:
        print(f"Error al guardar: {e}")