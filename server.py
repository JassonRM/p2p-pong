import socket
import _thread


def addr_to_msg(addr):
    return '{}:{}'.format(addr[0], str(addr[1])).encode('utf-8')


def simple_udp_server():
    addresses = []
    sock = socket.socket(socket.AF_INET,  # Internet
                         socket.SOCK_DGRAM)  # UDP
    sock.bind(("", 8000))
    print("Server started, waiting for connections...")
    while True:
        data, addr = sock.recvfrom(1024)  # buffer size is 1024 bytes
        print("Connection from: ", addr)
        addresses.append(addr)
        if len(addresses) >= 2:
            print("Server: sending client ", addresses[1], " info for: ", addresses[0])
            sock.sendto(addr_to_msg(addresses[1]), addresses[0])
            print("Server: sending client ", addresses[0], " info for: ", addresses[1])
            sock.sendto(addr_to_msg(addresses[0]), addresses[1])
            addresses.pop(1)
            addresses.pop(0)


if __name__ == '__main__':
    _thread.start_new_thread(simple_udp_server, ())
    while True:
        pass
