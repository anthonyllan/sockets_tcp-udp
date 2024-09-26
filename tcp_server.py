import socket

# Crear un socket TCP/IP
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('192.168.234.88', 9999))
server.listen()

print("Servidor escuchando en el puerto 9999...")

while True:
    client, address = server.accept()
    print(f"Se conectó {address}")
    
    try:
        # Recibir primer mensaje del cliente
        message = client.recv(1024).decode('utf-8')
        print(f"Cliente: {message}")
        
        # Enviar respuesta al cliente
        client.send("Hola cliente!".encode('utf-8'))
        
        # Recibir segundo mensaje del cliente
        message = client.recv(1024).decode('utf-8')
        print(f"Cliente: {message}")
        
        # Enviar segunda respuesta al cliente
        client.send("Adios!".encode('utf-8'))

    except socket.error as e:
        print(f"Error de socket: {e}")
    finally:
        # Cerrar la conexión
        client.close()
        print("Conexión cerrada")
