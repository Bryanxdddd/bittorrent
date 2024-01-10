import socket
import threading

class Seeder:

    def __init__(self, ip, puerto):
        self.ip = ip
        self.puerto = puerto
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
        # Obtenemos la lista de archivos que solicita el leecher
        lista_archivos_solicitados = conexion.recv(1024).decode()

        # Enviamos la lista de archivos que compartimos
        lista_archivos_compartidos = ";".join(self.archivos)
        conexion.send(lista_archivos_compartidos.encode())

        # Iteramos sobre la lista de archivos solicitados
        for archivo_solicitado in lista_archivos_solicitados.split(";"):

            # Si el archivo está disponible, lo enviamos al leecher
            if archivo_solicitado in self.archivos:
                with open(archivo_solicitado, "rb") as f:
                    while True:
                        data = f.read(1024)
                        if not data:
                            break
                        conexion.sendall(data)

            # Si el archivo no está disponible, cerramos la conexión
            else:
                conexion.close()

    def agregar_archivo(self, archivo):
        self.archivos.append(archivo)

