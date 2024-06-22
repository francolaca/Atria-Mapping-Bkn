Estructura del Proyecto:

app
    __init__.py
    database.py
    models.py
    views.py
venv
    Include
    Lib
    Scripts
    pyvenv.cfg
.env
.env.example
.gitignore
DER.drawio
README.txt
requirements.txt
run.py


Entorno Virtual en Python:

Un "Entorno Virtual en Python", es una herramienta que nos permite generar un espacio aislado (incluyendo una copia de la instalacion de python en su versión actual), donde vamos a poder instalar y gestionar paquetes, librerias y dependencia de forma independiente entre distintos proyectos. Solo existe para el proyecto en el que estamos trabajando, manteniéndolo aislado de los otros proyectos. Antes de instalar paquetes, librerias, dependencias, etc, primero se debe activar el entorno. Es buena practica generar un archivo "requirements.txt" que lleve el registro de todas las dependencias instaladas en el entorno virtual.

    Comandos para windows:
    Comando para generar el entorno virtual: python -m venv nombre_entorno (nosotros lo llamaremos venv => python -m venv venv)
    Comando para activar el entorno virtual: source ./venv/Scripts/activate   
    comando para instalar dependencias: pip install flask (para instalar flask)
                                        pip install mysql-connector-python (instala una librería que nos permite conectar una aplicación de flask/phyton con una base de datos mySQL)
                                        pip install python-dotenv (librería para manejar variables de entorno)
    Comando para ver todas las dependencias instaladas en el entorno virtual: pip freeze 
    Comando para generar/actualizar requirements.txt: pip freeze > requirements.txt
    Comando para leer un archivo requirements.txt e instalar todas las dependencias listadas en él: pip install -r requirements.txt 


Variables de Entorno:

Las variables de entorno nos permiten almacenar datos sencibles, que no tenemos porque divulgar o subir a un repositorio (por ejemplo contraseñas, secrets, claves, etc) y que tenemos que resguardar de posibles accesos externos. Para ello generamos el archivo ".env" que almacena estas variables. El archivo .env debe estar incluido en .gitignore (no se debe subir al repositorio). Sí se sube un archivo ".env.example" con una copia de los nombres de las variables de entorno pero SIN SUS VALORES. El archivo .env.example es de utilidad a los integrantes del equipo para que sepan que variables de entorno deben crear.  


Archivo de configuración de la base de datos:

Dentro de app se crea un archivo "database.py". Este archivo contiene el código para cargar las variables de entorno, abrir una conexion a la base de datos (cuando el servidor recibe una peticion HTTP) y cerrar la conexion cuando dejamos de utilizarla.


Git:

El archivo ".gitignore" contiene todos los archivos que no quiero que git rastree. En nuestro caso utilizamos la página "gitignore.io" para generar una plantilla de .gitignore (se utilizaron los filtros Python, Flask, Windows, Linux y MacOS) 


Python:

El archivo "run.py" es el que debemos ejecutar para correr nuestro proyecto (contiene la aplicación de Flask)

En python, a los archivos .py se los denomina "módulos". Por otro lado, a las carpetas que contienen multiples archivos .py podemos darle la funcionalidad de que sean consideradas como "paquetes". Esto es útil para que después podamos importar estos paquetes en algun otro archivo .py, y así poder reutilizar código. Para que una carpeta sea considerada paquete, debe contener un archivo "__init__.py". En nuestro proyecto creamos una paquete "app"


Flask:

Patron de arquitectura que maneja Flask: MVT (Model - View - Template)

La capa del modelo contiene la lógica necesaria para acceder a la base de datos. Se implementa por medio de un archivo "models.py", donde se definen las clases con sus asociaciones a las tablas de la base de datos.

La capa de las vistas contiene la lógica de negocios del proyecto. Se implementa por medio de un archivo "views.py", donde se definen las funciones propias del proyecto web que estamos desarrollando. 

La capa de plantillas (o capa de presentación) contiene los archivos .html, .css y .js que nuestro proyecto web podría llegar a servir o devolver. En el caso de una API REST esta capa no se implementa. Este es nuestro caso, ya que nuestro proyecto de frontend lo tenemos por separado. Estamos desarrollando un proyecto de backend con API REST integrada.


drawio:

Se incluye archivo "DER.drawio" con el modelo DER y diagramado de tablas de la base de datos
