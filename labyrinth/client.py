from socket import socket

host_name, bind_to = 'localhost', 8200

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
