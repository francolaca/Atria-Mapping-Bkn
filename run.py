# Desde la librería flask que está instalada en nuestro entorno virtual importamos la clase Flask
from flask import Flask

# Desde views.py importamos las función necesarias (en este caso todas las funciones de views.py)
from app.views import *

# Desde database.py importamos la función init_app
from app.database import init_app

# Inicialización de la aplicación con Flask (generamos una instancia de la clase Flask)
app = Flask(__name__)

# Llamamos a la función init_app y le pasamos el objeto app de flask. Esta función llama automáticamente a la función close_db cada vez que el servidor termine de responder una petición.  
init_app(app)


# Registrar una ruta asociada a una vista (asociamos una ruta a una vista). Cuando mi servidor recibe la ruta "/api/muestras" ejecuta la función get_all_muestras
app.route("/api/muestras/",methods=["GET"])(get_all_muestras)
app.route("/api/muestra/",methods=["GET"])(get_muestra)
app.route("/api/create/",methods=["GET"])(create_muestra)
app.route("/api/update/",methods=["GET"])(update_muestra)
app.route("/api/delete/",methods=["GET"])(delete_muestra)




# instrucción que permite separar el código que queremos que se ejecute del resto del código (__main__ => hacer click al icono de play o al ejecutar el archivo .py desde la terminal)
if __name__== "__main__":
    # Correr el servidor de desarrollo de flask
    app.run(debug=True)