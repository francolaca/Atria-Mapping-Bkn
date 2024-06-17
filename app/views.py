# En este archivo se definen las funciones que queremos que flask asocie a las rutas

# Importamos la función jsonify de la librería flask.
# Esta función me permite convertir listas y diccionarios de python al formato json
# y a su vez cuando esto sea devuelto al cliente, va agregar las cabeceras necesarias a la respuesta
from flask import jsonify


# def index():
#     response = {"message":"Hola Mundo API-REST Flask-Python"}
#     return jsonify(response)


def get_all_cards():
    response = {"message":"Obteniendo todas las tarjetas"}
    return jsonify(response)

def get_card():
    response = {"message":"Obteniendo una tarjeta"}
    return jsonify(response)

def create_card():
    response = {"message":"Creando"}
    return jsonify(response)

def update_card():
    response = {"message":"Actualizando"}
    return jsonify(response)

def delete_card():
    response = {"message":"Eliminando"}
    return jsonify(response)