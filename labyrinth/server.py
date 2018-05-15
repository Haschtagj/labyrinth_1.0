from socket import socket, AF_INET, SOCK_STREAM

host_name, port = '', 8200

server_sock = socket(family=AF_INET, type=SOCK_STREAM)
server_sock.bind((host_name, port))
server_sock.listen(5)
print(f'Serveur is listen on the port {port}')

interchange_sock, client_info = server_sock.accept()

client_msg = ''
while client_msg != 'end':
    user_name = input("Your user name: ")
    client_msg = interchange_sock.recv(1024)
    client_msg = client_msg.decode()
    print("{user_name}: {client_msg}")
    interchange_sock.send("5/5")


print('Server closed..')
interchange_sock.close()
server_sock.close()
