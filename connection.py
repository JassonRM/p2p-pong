import socket


class Connection:
    def __init__(self, server, port, mode):
        self.address = server
        self.port = port
        self.mode = mode
        self.sock = 0
        self.connection = 0

    def init_host(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.address, self.port)
        self.sock.bind(server_address)
        self.sock.listen(1)
        self.connection, client = self.sock.accept()

    def write(self, data):
        data += "\r"
        self.connection.sendall(data)

    def receive(self):
        char = ""
        new_char = ""
        while new_char != '\r':
            new_char = self.connection.recv(1)
            char += new_char
        return  char

    def init_client(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (self.address, self.port)
        self.sock.connect(server_address)
        self.connection = self.sock
