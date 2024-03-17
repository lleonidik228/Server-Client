import socket
from Main_Server import get_local_ip

server_support = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_support.bind((get_local_ip(), 6969))
server_support.listen(1)

print("[+] Listener listen on ip -", get_local_ip())

connection, address = server_support.accept()

print(connection.recv(1024).decode())

