import socket
import threading

class Tracker:

    def __init__(self, ip, puerto):
        self.ip = ip
        self.puerto = puerto
        self.nodos = []
        self.archivos = []

    def iniciar(self):
        # Creamos un socket y lo escuchamos en un puerto especificado
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.ip, self.puerto))
        self.socket.listen(5)

        # Creamos un hilo para atender las conexiones entrantes
        hilo_atender = threading.Thread(target=self.atender_conexiones)
        hilo_atender.daemon = True
        hilo_atender.start()

    def atender_conexiones(self):
        while True:
            # Aceptamos una conexión entrante
            conexion, direccion = self.socket.accept()

            # Creamos un hilo para atender la conexión
            hilo_atender_conexion = threading.Thread(target=self.atender_conexion, args=(conexion, direccion))
            hilo_atender_conexion.daemon = True
            hilo_atender_conexion.start()

    def atender_conexion(self, conexion, direccion):
        # Obtenemos el rol del cliente
        rol_cliente = conexion.recv(1024).decode()

        # Si el cliente es un leecher, le enviamos la lista de seeders
        if rol_cliente == "leecher":
            lista_seeders = ";".join([nodo.ip for nodo in self.nodos])
            conexion.send(lista_seeders.encode())

        # Si el cliente es un seeder, le enviamos la lista de archivos que comparte
        elif rol_cliente == "seeder":
            lista_archivos = ";".join(self.archivos)
            conexion.send(lista_archivos.encode())

        # Si el cliente es un desconocido, cerramos la conexión
        else:
            conexion.close()

    def agregar_nodo(self, nodo):
        self.nodos.append(nodo)

    def agregar_archivo(self, archivo):
        self.archivos.append(archivo)

    def obtener_lista_nodos(self):
        return self.nodos

    def obtener_lista_archivos(self):
        return self.archivos
