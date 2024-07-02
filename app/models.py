# De database.py importamos la función get_db. Esta función nos permite obtener una conexión a nuestra base de datos
from app.database import get_db


#-----------------------------------------------------------------Clase Muestra--------------------------------------------------------


class Muestra:

    contador_muestras = 0
    # Lista que contiene los id de las muestras inactivas
    inactivas = []


    # Método Constructor
    def __init__(self, id_muestra=None, id_plataforma=None, url_img=None, nombre_img=None, fecha_img=None, ubicación=None, destacado="0", alt_img=None, muestra_activa="1", nombre_plat=None):

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
        self.nombre_plat=nombre_plat
        # Relación de agregación entre Muestra y Usuario (las clases Muestra y Usuario pueden existir independientemente). Lista de usuarios que han descargado esta muestra
        self.usuarios=[]


    # Metodo para dar formato de texto a la instancia de la clase (caso contrario las instancias de la case devolverán algo __main__.Muestra object at 0x0000020C38507310> cuando se las llame)
    def __str__(self):
        return f"id_muestra: {self.id_muestra}, id_plataforma: {self.id_plataforma}, url_img: {self.url_img}, nombre_img: {self.nombre_img}, fecha_img: {self.fecha_img} , ubicación: {self.ubicación}, destacado: {self.destacado}, alt_img: {self.alt_img}, muestra_activa: {self.muestra_activa}, nombre_plat: {self.nombre_plat}"


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
            "muestra_activa":self.muestra_activa,
            "nombre_plat":self.nombre_plat
        }


    # Método estático para obtener todas las muestras de la base de datos. Los metodos estáticos se pueden llamar directamente desde la clase, no necesitan una instancia de la clase para ser ejecutados
    @staticmethod
    def get_all():
        db = get_db()   # Se genera/obtiene una conexion a la base de datos
        cursor = db.cursor()    # Para ejecutar una instrucción SQL necesito implementar un objeto "cursor"
        # Traer toda la tabla muestras más la "columna" nombre_plat de la tabla plataformas
        query1 = "SELECT * FROM muestras"    # Variable con la instrucción SQL (seleccionamos la tabla muestras de nuestra db)
        query2 = "SELECT id_plataforma, nombre_plat FROM plataformas"   # Seleccionamos las "columnas" id_plataforma, nombre_plat FROM de nuestra tabla plataformas
        cursor.execute(query1)   # Se ejecuta la instrucción SQL por medio del método execute del objeto cursor
        rows_tuples_1 = cursor.fetchall()   # Se guardan los resultados en rows_tuples_1
        rows_lists_1 = [list(row) for row in rows_tuples_1] # Se generan listas a partir de las tuplas (las listas se pueden editar)
        cursor.execute(query2)
        rows_tuples_2 = cursor.fetchall()
        rows_lists_2 = [list(row) for row in rows_tuples_2]        
        # Crear una nueva "columna" en row_lists_1 con los valores correspondientes del campo nombre_plat de la tabla plataformas
        plataformas = {row[0]: row[1] for row in rows_lists_2}  # Crear un diccionario a partir de rows_lists_2 para facilitar la búsqueda
        for row in rows_lists_1:
            if row[1] in plataformas:
                row.append(plataformas[row[1]])
        muestras = [Muestra(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9]) for row in rows_lists_1]    # Convertir row_lists_1 en una lista de objetos de la clase Muestra               
        cursor.close()  # Cerrar el cursor
        return muestras


    # Método estático para obtener de la base de datos, la muestra con un dado id_muestra que se pasa como parámetro. Si no se encuentra devuelve None.
    @staticmethod
    def get_by_id(id_muestra):
        db = get_db()
        cursor = db.cursor()
        query1 = "SELECT * FROM muestras WHERE id_muestra = %s" # Por seguridad (ayuda a prevenir inyecciones SQL), se prefiere el uso de %s y una tupla (id_muestra,) como parámetros frente al uso de f strings
        query2 = "SELECT id_plataforma, nombre_plat FROM plataformas"
        cursor.execute(query1, (id_muestra,)) 
        row_tuple_1 = cursor.fetchone() # Se obtiene la primera fila del resultado de la consulta. Si no hay coincidencias, row_tuple_1 será None.
        row_list_1 = list(row_tuple_1)
        cursor.execute(query2)
        rows_tuples_2 = cursor.fetchall()
        rows_lists_2 = [list(row) for row in rows_tuples_2]
        plataformas = {row[0]: row[1] for row in rows_lists_2}
        if row_list_1[1] in plataformas:
            row_list_1.append(plataformas[row_list_1[1]])
        cursor.close()
        if row_list_1:
            return Muestra(row_list_1[0], row_list_1[1], row_list_1[2], row_list_1[3], row_list_1[4], row_list_1[5], row_list_1[6], row_list_1[7], row_list_1[8], row_list_1[9])    # Se retorna un objeto de la clase Muestra               
        return None


    @staticmethod 
    def activate_all():
        db = get_db()
        cursor = db.cursor()
        query = "UPDATE muestras SET muestra_activa = %s" 
        cursor.execute(query, (1,))
        db.commit()
        cursor.close()


    # Método para conectarse a la tabla de muestras y hacer un borrado lógico de un registro
    def delete(self):
        # Agregamos la muestra a la lista de muestras inactivas
        if not self.id_muestra in Muestra.inactivas:
            Muestra.inactivas.append(self.id_muestra)
            # Inactivamos la muestra en la base de datos:
            db = get_db()
            cursor = db.cursor()
            query = "UPDATE muestras SET muestra_activa = %s, destacado = %s WHERE id_muestra = %s" 
            cursor.execute(query, (0,0,self.id_muestra,))
            db.commit()
            cursor.close()


    # Método para conectarse a la tabla de muestras y actualizar un registro existente o insertar uno nuevo
    def save(self):
        db = get_db()
        cursor = db.cursor()
        if self.id_muestra:
            query = "UPDATE muestras SET id_plataforma = %s, url_img = %s, nombre_img = %s, fecha_img = %s, ubicación = %s, destacado = %s, alt_img = %s, muestra_activa = %s WHERE id_muestra = %s"
            cursor.execute(query, (self.id_plataforma, self.url_img, self.nombre_img, self.fecha_img, self.ubicación, self.destacado, self.alt_img, self.muestra_activa, self.id_muestra))
        else:

            # Buscar el id_plataforma correspondiente al nombre_plat en la tabla plataformas
            query1 = "SELECT id_plataforma FROM plataformas WHERE nombre_plat = %s"
            cursor.execute(query1, (self.nombre_plat,))
            row1 = cursor.fetchone()
            self.id_plataforma = row1[0]  # Asignar el id_plataforma encontrado

            # Insertar los valores en la tabla muestras, incluyendo el id_plataforma encontrado en la tabla plataformas
            query2 = "INSERT INTO muestras (id_plataforma, url_img, nombre_img, fecha_img, ubicación, destacado, alt_img, muestra_activa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(query2, (self.id_plataforma, self.url_img, self.nombre_img, self.fecha_img, self.ubicación, self.destacado, self.alt_img, self.muestra_activa))
            self.id_muestra = cursor.lastrowid  # Obtener el ID del último registro insertado

        db.commit()
        cursor.close()


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


    # Método para incluir la muestra en el carrusel de imagenes del sitio web
    def carousel(self):
        return ""


    # Metodo para activar una muestra que está inactiva
    def activar(self):
        if self.id_muestra in Muestra.inactivas:
            Muestra.inactivas.remove(self.id_muestra)


#--------------------------------------------------------------------------------------Clase Plataforma----------------------------------------------------------------------------------------------


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


    @staticmethod
    def get_all():
        db = get_db()    
        cursor = db.cursor()    
        query = "SELECT * FROM plataformas"
        cursor.execute(query)
        rows_tuples = cursor.fetchall()
        rows_lists = [list(row) for row in rows_tuples] # Se generan listas a partir de las tuplas (las listas se pueden editar)
        plataformas = [Plataforma(row[0], row[1], row[2], row[3]) for row in rows_lists]    # Convertir row_lists en una lista de objetos de la clase Plataforma               
        cursor.close()  # Cerrar el cursor
        return plataformas


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


#----------------------------------------------------------------------------------------------Clase Usuario-------------------------------------------------------------------------------------


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