import socket


class Connection:
    def __init__(self, server, port, mode):
        self.address = server
        self.port = port
        self.mode = mode
        self.sock = 0
        self.connection = 0
 #
    def init_host(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.address, self.port)
        self.sock.bind(server_address)
        self.sock.listen(1)
        self.connection, client = self.sock.accept()

    def write(self, data):
        data += "\r"
        self.connection.sendall(data.encode())

    def receive(self):
        char = self.connection.recv(1024).decode()
        return char

    def init_client(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.address, self.port)
        self.sock.connect(server_address)
        self.connection = self.sock

    def set_port(self, port):
        self.port = port
