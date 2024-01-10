import socket
import threading

class Leecher:

    def __init__(self, ip, puerto):
        self.ip = ip
        self.puerto = puerto

    def iniciar(self):
        # Creamos un socket y nos conectamos al tracker
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.ip, self.puerto))

        # Enviamos el rol del cliente
        self.socket.send("leecher".encode())

        # Obtenemos la lista de seeders
        lista_seeders = self.socket.recv(1024).decode()

        # Iteramos sobre la lista de seeders
        for seeder_ip in lista_seeders.split(";"):

            # Nos conectamos a un seeder
            self.conectarse_a_seeder(seeder_ip)

    def conectarse_a_seeder(self, seeder_ip):
        # Creamos un socket y nos conectamos al seeder
        socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket.connect((seeder_ip, 8080))

        # Enviamos el rol del cliente
        socket.send("leecher".encode())

        # Obtenemos la lista de archivos que comparte el seeder
        lista_archivos_compartidos = socket.recv(1024).decode()

        # Iteramos sobre la lista de archivos compartidos
        for archivo in lista_archivos_compartidos.split(";"):

            # Solicitamos el archivo al seeder
            socket.send(archivo.encode())

            # Recibimos el archivo del seeder
            data = socket.recv(1024)

            # Guardamos el archivo en el disco duro
            with open(archivo, "wb") as f:
                f.write(data)

        # Cerramos la conexión con el seeder
        socket.close()

