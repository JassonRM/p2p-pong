import socket
import select


def msg_to_addr(data):
    ip, port = data.decode('utf-8').strip().split(':')
    return (ip, int(port))


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sendToAddress = 0
        self.socket = 0

    def hole_punching(self):
        self.socket = socket.socket(socket.AF_INET,  # Internet
                                    socket.SOCK_DGRAM)  # UDP
        self.socket.sendto(b'0', (self.host,self.port))
        while True:
            data, addr = self.socket.recvfrom(1024)
            print('client received: {} {}'.format(addr, data))
            addr = msg_to_addr(data)
            self.sendToAddress = addr
            self.socket.sendto(b'0', addr)
            data, addr = self.socket.recvfrom(1024)
            print('client received: {} {}'.format(addr, data))

    def write(self, message):
        message = message.encode(encoding='UTF-8', errors='strict')
        self.socket.sendto(message, self.sendToAddress)

    def read(self):
        ready_sockets, _, _ = select.select(
            [self.socket], [], [], 10
        )
        if ready_sockets:
            message = self.socket.recvfrom(1024)
            return message.decode('utf8', 'strict')
        else:
            return "No"
