# De database.py importamos la función get_db. Esta función nos permite obtener una conexión a nuestra base de datos
from app.database import get_db


#-----------------------------------------------------------------Clase Muestra--------------------------------------------------------


class Muestra:

    contador_muestras = 0
    # Lista que contiene los id de las muestras inactivas
    inactivas = []

    # Método Constructor
    def __init__(self, id_muestra=None, id_plataforma=None, url_img=None, nombre_img=None, fecha_img=None, ubicación=None, destacado="0", alt_img=None, muestra_activa="1"):

        # Atributos de clase (compartidos por todas las instancias)
        Muestra.contador_muestras += 1

        # Atributos de objeto
        self.id_muestra=id_muestra
        self.id_plataforma=id_plataforma
        self.url_img=url_img
        self.nombre_img=nombre_img
        self.fecha_img=fecha_img
        self.ubicación=ubicación
        self.destacado=destacado
        self.alt_img=alt_img
        self.muestra_activa=muestra_activa
        # Relación de agregación entre Muestra y Usuario (las clases Muestra y Usuario pueden existir independientemente). Lista de usuarios que han descargado esta muestra
        self.usuarios=[]

    # Metodo para dar formato de texto a la instancia de la clase (caso contrario las instancias de la case devolverán algo __main__.Muestra object at 0x0000020C38507310> cuando se las llame)
    def __str__(self):
        return f"id_muestra: {self.id_muestra}, id_plataforma: {self.id_plataforma}, url_img: {self.url_img}, nombre_img: {self.nombre_img}, fecha_img: {self.fecha_img} , ubicación: {self.ubicación}, destacado: {self.destacado}, alt_img: {self.alt_img}, muestra_activa: {self.muestra_activa}"

    # Método para dar formato de diccionario a la instancia de la clase
    def serialize(self):
        return {
            "id_muestra":self.id_muestra,
            "id_plataforma":self.id_plataforma,
            "url_img":self.url_img,
            "nombre_img":self.nombre_img,
            "fecha_img":self.fecha_img,
            "ubicación":self.ubicación,
            "destacado":self.destacado,
            "alt_img":self.alt_img,
            "muestra_activa":self.muestra_activa
        }
    
    # Método estático para obtener todas las muestras de la base de datos. Los metodos estáticos se pueden llamar directamente desde la clase, no necesitan una instancia de la clase para ser ejecutados
    @staticmethod
    def get_all():
        db = get_db()   # Se genera/obtiene una conexion a la base de datos
        cursor = db.cursor()    # Para ejecutar una instrucción SQL necesito implementar un objeto "cursor"
        # Nos vamos a traer toda la tabla muestras más la "columna" nombre_plat de la tabla plataformas
        query1 = "SELECT * FROM muestras"    # Variable con la instrucción SQL (seleccionamos la tabla muestras de nuestra db)
        query2 = "SELECT id_plataforma, nombre_plat FROM plataformas"   # Seleccionamos las "columnas" id_plataforma, nombre_plat FROM de nuestra tabla plataformas
        cursor.execute(query1)   # Se ejecuta la instrucción SQL por medio del método execute del objeto cursor
        rows_tuples_1 = cursor.fetchall()   # Se guardan los resultados en rows_tuples_1
        rows_lists_1 = [list(row) for row in rows_tuples_1] # Se generan listas a partir de las tuplas (las listas se pueden editar)
        cursor.execute(query2)
        rows_tuples_2 = cursor.fetchall()
        rows_lists_2 = [list(row) for row in rows_tuples_2]
        # Crear una nueva "columna" en row_lists_1 con los valores correspondientes del campo nombre_plat de la tabla plataformas
        plataformas = {row[0]: row[1] for row in rows_lists_2}    # Crear un diccionario a partir de rows_lists_2 para facilitar la búsqueda
        for row in rows_lists_1:
            if row[1] in plataformas:
                row.append(plataformas[row[1]])
        muestras = [Muestra(row[0], row[9], row[2], row[3], row[4], row[5], row[6], row[7], row[8]) for row in rows_lists_1]    # Convertir row_lists_1 en una lista de objetos de la clase Muestra               
        cursor.close()  # Cerrar el cursor
        return muestras

    # Método para agregar un usuario a la lista de usuarios que han descargado esta muestra. Relación de agregación entre Muestra y Usuario (las clases Muestra y Usuario pueden existir independientemente)
    def add_usuario(self, usuario):
        self.usuarios.append(usuario)

    # Método para mostrar todos los usuarios que han descargado esta muestra
    def show_usuarios(self):
        for usuario in self.usuarios:
            print(usuario)

    # Método para conectarse a la tabla de muestras e insertar un nuevo registro
    def create(self):
        pass

    # Método para conectarse a la tabla de muestras y borrar un registro
    def delete(self):
        pass

    # Metodo para hacer un borrado lógico de la muestra
    def desactivar(self):
        if not self.id_muestra in Muestra.inactivas:
            Muestra.inactivas.append(self.id_muestra)

    # Metodo para activar una muestra que está inactiva
    def activar(self):
        if self.id_muestra in Muestra.inactivas:
            Muestra.inactivas.remove(self.id_muestra)

    # muestra1 = Muestra("1", "3", "url1", "Atardecer en el lago", "2020-05-05", "El Calafate", "imagen del Glaciar Perito Moreno", "1")
    # # print(muestra1.nombre_img)
    # muestra2 = Muestra("2", "1", "url2", "Valcán violento", "2020-01-05", "Hawái", "imagen volcán en erupción", "1")
    # # print(muestra2.nombre_img)
    # muestra3 = Muestra("3", "2", "url3", "Playita", "2018-01-05", "Brasil", "imagen playa", "0")
    # muestra4 = Muestra("4", "6", "url4", "Peligro Rojo", "2023-03-09", "Rusia", "imagen base militar rusa", "0")
    # muestra5 = Muestra("5", "4", "url5", "Verde Esmeralda", "2020-12-12", "Costa Rica", "imagen selva", "1")
    # muestra6 = Muestra("6", "5", "url6", "Efectos Calentamiento Global", "2020-01-05", "Canadá", "imagen glaciar")

    # print(f"Se definieron {Muestra.contador_muestras} instancias de la clase Muestra:")
    # print(muestra1)  # Al estar definido el método __str__, se muestra el texto que retorna este método

    # muestra1.desactivar()


#-----------------------------------------------------------------Clase Plataforma--------------------------------------------------------


class Plataforma:

    contador_plataformas = 0
    inactivas = []

    def __init__(self, id_plataforma=None, nombre_plat=None, fabricante=None, plataforma_activa="1"):

        Plataforma.contador_plataformas += 1
        self.id_plataforma=id_plataforma
        self.nombre_plat=nombre_plat
        self.fabricante=fabricante
        self.plataforma_activa=plataforma_activa
        # Relación de composición entre Plataforma y Muestra (sin la clase Plataforma, la clase Muestra no existiría). Lista de muestras tomadas por esta plataforma
        self.muestras=[]
        
    def __str__(self):
        return f"id_plataforma: {self.id_plataforma}, nombre_plat: {self.nombre_plat}, fabricante: {self.fabricante}, plataforma_activa: {self.plataforma_activa}, muestras: {len(self.muestras)}"
    
    def serialize(self):
        return {
            "id_plataforma":self.id_plataforma,
            "nombre_plat":self.nombre_plat,
            "fabricante":self.fabricante,
            "plataforma_activa":self.plataforma_activa,
            "muestras":len(self.muestras)
        }
    
    # Método para agregar una muestra a la lista de muestras tomadas por la plataforma. Relación de composición entre Plataforma y Muestra (sin la clase Plataforma, la clase Muestra no existiría)
    def add_muestra(self, id_muestra, id_plataforma, url_img, nombre_img, fecha_img, ubicación, destacado, alt_img, muestra_activa):
        # Se crea una instancia de la clase Muestra
        muestra = Muestra(id_muestra, id_plataforma, url_img, nombre_img, fecha_img, ubicación, destacado, alt_img, muestra_activa)
        # Se agrega la instancia a la lista muestras
        if muestra.id_plataforma == self.id_plataforma:
            self.muestras.append(muestra)

    # Método para mostrar todas las muestras tomadas por la plataforma
    def show_muestras(self):  
        for muestra in self.muestras:
            print(muestra)

    def desactivar(self):
        if not self.id_plataforma in Plataforma.inactivas:
            Plataforma.inactivas.append(self.id_plataforma)

    def activar(self):
        if self.id_plataforma in Plataforma.inactivas:
            Plataforma.inactivas.remove(self.id_plataforma)

# plataforma1 = Plataforma("1", "WORLDVIEW-3", "Ball Aerospace")
# plataforma2 = Plataforma("2", "WORLDVIEW-2", "Ball Aerospace")
# plataforma3 = Plataforma("3", "GEOEYE-1", "General Dynamics")
# plataforma4 = Plataforma("4", "PLÉIADES 1", "EADS Astrium Satellites")
# plataforma5 = Plataforma("5", "PLANETSCOPE", "Planet Labs")
# plataforma6 = Plataforma("6", "PLÉIADES NEO", "Airbus")

# plataforma1.add_muestra("2", "1", "url2", "Valcán violento 1", "2020-01-05", "Hawái", "WORLDVIEW-3", "imagen volcán en erupción, día 1", "1")
# plataforma2.add_muestra("3", "2", "url3", "Playita", "2018-01-05", "Brasil", "WORLDVIEW-2", "imagen playa", "0")
# plataforma3.add_muestra("1", "3", "url1", "Atardecer en el lago", "2020-05-05", "El Calafate", "GEOEYE-1", "imagen del Glaciar Perito Moreno", "1")
# plataforma4.add_muestra("5", "4", "url5", "Verde Esmeralda", "2020-12-12", "Costa Rica", "PLÉIADES 1", "imagen selva", "1") 
# plataforma5.add_muestra("6", "5", "url6", "Efectos Calentamiento Global", "2020-01-05", "Canadá", "PLANETSCOPE", "imagen glaciar") 
# plataforma6.add_muestra("4", "6", "url4", "Peligro Rojo", "2023-03-09", "Rusia", "PLÉIADES NEO", "imagen base militar rusa", "0")
# plataforma1.add_muestra("7", "1", "url7", "Valcán violento 2", "2020-01-06", "Hawái", "WORLDVIEW-3", "imagen volcán en erupción, día 2")
# plataforma1.add_muestra("8", "1", "url8", "Valcán violento 3", "2020-01-07", "Hawái", "WORLDVIEW-3", "imagen volcán en erupción, día 3")   

# plataforma1.show_muestras()

# print(plataforma1)


#-----------------------------------------------------------------Clase Usuario--------------------------------------------------------


class Usuario:
    
    contador_usuarios = 0
    inactivos = []

    def __init__(self, id_usuario=None, nombre_us=None, apellido=None, email=None, contraseña=None, usuario_activo="1"):

        Usuario.contador_usuarios += 1
        self.id_usuario=id_usuario
        self.nombre_us=nombre_us
        self.apellido=apellido
        self.email=email
        self.contraseña=contraseña
        self.usuario_activo=usuario_activo
        # Relación de agregación entre Usuario y Muestra (las clases Usuario y Muestra pueden existir independientemente). Lista de muestras descargadas por este usuario
        self.muestras=[]

    def __str__(self):
        return f"id_usuario: {self.id_usuario}, nombre_us: {self.nombre_us}, apellido: {self.apellido}, email: {self.email}, contraseña: {self.contraseña}, usuario_activo: {self.usuario_activo}, descargas: {len(self.muestras)}"
    
    def serialize(self):
        return {
            "id_usuario":self.id_usuario,
            "nombre_us":self.nombre_us,
            "apellido":self.apellido,
            "email":self.email,
            "contraseña":self.contraseña,
            "usuario_activo":self.usuario_activo,
            "descargas":len(self.muestras)
        }

    # Método para agregar una muestra a la lista de muestras gratis descargadas por el usuario. Relación de agregación entre Usuario y Muestra (las clases Usuario y Muestra pueden existir independientemente)
    def add_muestra(self, muestra):
        self.muestras.append(muestra)
    
    # Método para mostrar todas las muestras descargadas por el usuario
    def show_muestras(self):
        for muestra in self.muestras:
            print(muestra)

    def desactivar(self):
        if not self.id_usuario in Usuario.inactivos:
            Usuario.inactivos.append(self.id_usuario)

    def activar(self):
        if self.id_usuario in Usuario.inactivos:
            Usuario.inactivos.remove(self.id_usuario)

# usuario1 = Usuario("1", "Carlos", "García", "carlos.garcia@outlook.com", "Abc1234")
# usuario2 = Usuario("2", "María", "Rodríguez", "maria.rodriguez@gmail.com", "XyZ4567")
# usuario3 = Usuario("3", "Juan", "Martínez", "juan.martinez@yahoo.com", "QwErTy8")
# usuario4 = Usuario("4", "Ana", "López", "ana.lopez@hotmail.com", "1a2b3c4d")
# usuario5 = Usuario("5", "Pedro", "González", "pedro.gonzalez@live.com", "D4E5F6Gh")
# usuario6 = Usuario("6", "Lucía", "Hernández", "lucia.hernandez@protonmail.com", "gH7iJ8Kl")
# usuario7 = Usuario("7", "Sofía", "Pérez", "sofia.perez@aol.com", "kL9Mn0Op")
# usuario8 = Usuario("8", "Miguel", "Sánchez", "miguel.sanchez@icloud.com", "PqRstu12")
# usuario9 = Usuario("9", "Jorge", "Ramírez", "jorge.ramirez@yandex.com", "vWxYz3")
# usuario10 = Usuario("10", "Carmen", "Cruz", "carmen.cruz@zoho.com", "2AbCdE4")

# usuario1.add_muestra(plataforma1.muestras[0])
# usuario1.add_muestra(plataforma1.muestras[1])
# usuario1.add_muestra(plataforma1.muestras[2])

# usuario1.show_muestras()

# usuario2.desactivar()
# usuario5.desactivar()

# print(Usuario.inactivos)