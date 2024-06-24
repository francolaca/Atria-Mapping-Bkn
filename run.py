# Desde la librería flask que está instalada en nuestro entorno virtual importamos la clase Flask
from flask import Flask

# Desde la librería flask_cors importamos la clase CORS
from flask_cors import CORS

# Desde views.py importamos las función necesarias (en este caso todas las funciones de views.py)
from app.views import *

# Desde database.py importamos la función init_app
from app.database import init_app

# Inicialización de la aplicación con Flask (generamos una instancia de la clase Flask)
app = Flask(__name__)

# Llamamos a la función init_app y le pasamos el objeto app de flask. Esta función Inicializa la base de datos con la aplicación Flask y también llama automáticamente a la función close_db cada vez que el servidor termine de responder una petición.  
init_app(app)

#permitir solicitudes desde cualquier origen
CORS(app)

#permitir solicitudes desde un origen específico
#CORS(app, resources={r"/api/*": {"origins": "http://127.0.0.1:5500"}})


# Registrar una ruta asociada a una vista (asociamos una ruta a una vista). Cuando mi servidor recibe la ruta "/api/muestras" ejecuta la función get_all_muestras. Rutas para el CRUD de la entidad Muestra
app.route("/api/muestras/",methods=["GET"])(get_all_muestras)
app.route("/api/muestras/",methods=["GET"])(get_muestra)
app.route("/api/create/",methods=["GET"])(create_muestra)
app.route("/api/update/",methods=["GET"])(update_muestra)
app.route("/api/delete/",methods=["GET"])(delete_muestra)




# Rutas para el CRUD de la entidad Movie
# app.route('/', methods=['GET'])(index)
# app.route('/api/movies/', methods=['POST'])(create_movie)
# app.route('/api/movies/', methods=['GET'])(get_all_movies)
# app.route('/api/movies/<int:movie_id>', methods=['GET'])(get_movie)
# app.route('/api/movies/<int:movie_id>', methods=['PUT'])(update_movie)
# app.route('/api/movies/<int:movie_id>', methods=['DELETE'])(delete_movie)





# instrucción que permite separar el código que queremos que se ejecute del resto del código (__main__ => hacer click al icono de play o al ejecutar el archivo .py desde la terminal)
if __name__== "__main__":
    # Correr el servidor de desarrollo de flask
    app.run(debug=True)