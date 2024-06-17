# Desde la librería flask que está instalada en nuestro entorno virtual importamos la clase Flask
from flask import Flask

# Desde views.py importamos las función necesarias (en este caso todas las funciones de views.py)
from app.views import *

# Inicialización de la aplicación con Flask (generamos una instancia de la clase Flask)
app = Flask(__name__)

# Registrar una ruta asociada a una vista (asociamos una ruta a una vista)
# Cuando mi servidor recibe la ruta "/api/cards" ejecuta la función get_all_cards

app.route("/api/cards",methods=["GET"])(get_all_cards)
app.route("/api/card",methods=["GET"])(get_card)
app.route("/api/create",methods=["GET"])(create_card)
app.route("/api/update",methods=["GET"])(update_card)
app.route("/api/delete",methods=["GET"])(delete_card)




# instrucción que permite separar el código que queremos que se ejecute del resto del código
# (__main__ => hacer click al icono de play o al ejecutar el archivo .py desde la terminal)
if __name__== "__main__":
    # Correr el servidor de desarrollo de flask
    app.run(debug=True)