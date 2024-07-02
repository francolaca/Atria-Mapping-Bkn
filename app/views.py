# En este archivo se definen las funciones (vistas) que queremos que flask asocie a las rutas

# Importamos las funciones jsonify y request de la librería flask. Jsonify permite convertir listas y diccionarios de python al formato json y a su vez cuando esto sea devuelto al cliente, agregará las cabeceras necesarias a la respuesta. Request devuelve un objeto de Flask que contiene todos los datos de la solicitud HTTP realizada al servidor (esto incluye datos como los encabezados de la solicitud, los datos del formulario, los parámetros de la URL, los archivos subidos, etc).
from flask import jsonify, request

from app.models import Muestra, Plataforma


def get_all_samples():
    todas_las_muestras = Muestra.get_all()  # Llamar al método estático get.all() de la clase Muestra
    return jsonify([muestra.serialize() for muestra in todas_las_muestras]) # Llamar al método serialize() para convertir los objetos de la clase Muestra en diccionarios. Luego convertir la lista de diccionarios al formato JSON


def get_all_platforms():
    todas_las_plataformas = Plataforma.get_all()
    return jsonify([plataforma.serialize() for plataforma in todas_las_plataformas])


def reload_samples():
    Muestra.activate_all()
    todas_las_muestras = Muestra.get_all()
    return jsonify([muestra.serialize() for muestra in todas_las_muestras])


def delete_sample(id_muestra):
    muestra = Muestra.get_by_id(id_muestra)
    if not muestra:
        return jsonify({'message': 'Muestra no encontrada'}), 404
    muestra.delete()
    return jsonify({'message': 'La muestra se ha eliminado'})


def get_sample(id_muestra):
    muestra = Muestra.get_by_id(id_muestra)
    if not muestra:
        return jsonify({'message': 'Muestra no encontrada'}), 404
    return jsonify(muestra.serialize())


def update_sample(id_muestra):
    muestra = Muestra.get_by_id(id_muestra)
    if not muestra:
        return jsonify({'message': 'Muestra no encontrada'}), 404
    data = request.json   # Accede a los datos JSON enviados en el cuerpo de la solicitud

    muestra.id_plataforma=data["id_plataforma"]
    muestra.url_img=data["url_img"]
    muestra.nombre_img=data["nombre_img"]
    muestra.fecha_img=data["fecha_img"]
    muestra.ubicación=data["ubicación"]
    muestra.destacado=data["destacado"]
    muestra.alt_img=data["alt_img"]
    muestra.muestra_activa=data["muestra_activa"]
    muestra.nombre_plat=data["nombre_plat"]

    muestra.save()
    return jsonify({'message': 'La muestra se ha actualizado'})


def create_sample():
    data = request.json
    muestra = Muestra(url_img=data["url_img"], nombre_img=data["nombre_img"], fecha_img=data["fecha_img"], ubicación=data["ubicación"], destacado=data["destacado"], alt_img=data["alt_img"], muestra_activa=data["muestra_activa"], nombre_plat=data["nombre_plat"])
    muestra.save()
    return jsonify({'message': 'La muestra se ha creado correctamente'}), 201