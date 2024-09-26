import socket

def main():
    # Dirección IP y puerto del servidor Java
    server_address = '192.168.237.143'  # O la IP del servidor si no está en la misma máquina
    port = 8080  # Debe coincidir con el puerto en el servidor

    # Crear el socket TCP
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        try:
            # Conectar al servidor
            client_socket.connect((server_address, port))
            print(f"Conectado al servidor en {server_address}:{port}")
            
            # Leer el mensaje a enviar
            mensaje = input("Ingrese el mensaje a enviar al Servidor (1, 2 o 3): ")

            # Enviar el mensaje al servidor
            client_socket.sendall(mensaje.encode('utf-8'))

            # Recibir la respuesta del servidor
            response = client_socket.recv(1024).decode('utf-8')
            print(f"Respuesta del servidor: {response}")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()