import socket
import select


def msg_to_addr(data):
    ip, port = data.decode('utf-8').strip().split(':')
    return ip, int(port)


class Connection:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sendToAddress = None
        self.socket = None

    def hole_punching(self):
        self.socket = socket.socket(socket.AF_INET,  # Internet
                                    socket.SOCK_DGRAM)  # UDP

        # Request IP address and port from server
        self.socket.sendto(b'0', (self.host, self.port))
        data, addr = self.socket.recvfrom(1024)
        print('Client received: {} {}'.format(addr, data))
        addr = msg_to_addr(data)
        self.sendToAddress = addr

        self.socket.setblocking(0)
        self.socket.settimeout(0.002)

    def write(self, message):
        message = message.encode(encoding='UTF-8', errors='strict')
        self.socket.sendto(message, self.sendToAddress)

    def read(self):
        messages = []
        while True:
            try:
                data, _ = self.socket.recvfrom(1024)
                messages.append(data.decode('utf8', 'strict'))
            except socket.timeout:
                break
            except OSError:
                break

        if len(messages) != 0:
            return messages[-1]
        else:
            return None

