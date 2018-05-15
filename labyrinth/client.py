from socket import socket


def main():
    host_name, bind_to = 'localhost', 80005
    client_socket = socket()
    client_socket.connect((host_name, bind_to))
    to_send = b''
    while to_send != b'end':
        to_send = input('> ')
        to_send = to_send.encode()
        client_socket.send(to_send)
        receive = client_socket.recv(1024)
        print(receive.decode())
    print('Client closed...')
    client_socket.close()


if __name__ == '__main__':
    main()
