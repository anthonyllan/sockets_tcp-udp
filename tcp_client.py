import socket

# Crear un socket TCP/IP
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 9999))

client.send("Hola servidor!".encode('utf-8'))
print(client.recv(1024).decode('utf-8'))

client.send("Adios!".encode('utf-8'))
print(client.recv(1024).decode('utf-8'))

client.close()
