import socket

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto("Hola servidor!".encode('utf-8'), ("127.0.0.1", 9999))
message, address = client.recvfrom(1024)
print(message.decode('utf-8'))