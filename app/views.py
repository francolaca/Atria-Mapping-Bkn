# En este archivo se definen las funciones (vistas) que queremos que flask asocie a las rutas

# Importamos la función jsonify de la librería flask. Esta función me permite convertir listas y diccionarios de python al formato json y a su vez cuando esto sea devuelto al cliente, va agregar las cabeceras necesarias a la respuesta
from flask import jsonify

from app.models import Muestra

def get_all_muestras():
    todas_las_muestras = Muestra.get_all()  # Llamar al método estático get.all() de la clase Muestra
    # Llamar al método serialize() para convertir los objetos de la clase Muestra en diccionarios. Luego convertir la lista de diccionarios al formato JSON
    return jsonify([muestra.serialize() for muestra in todas_las_muestras]) 

def get_muestra():
    response = {"message":"Obteniendo una tarjeta"}
    return jsonify(response)

def create_muestra():
    response = {"message":"Creando"}
    return jsonify(response)

def update_muestra():
    response = {"message":"Actualizando"}
    return jsonify(response)

def delete_muestra():
    response = {"message":"Eliminando"}
    return jsonify(response)