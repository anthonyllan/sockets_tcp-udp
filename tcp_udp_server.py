import socket
import threading
import tkinter as tk
from tkinter import simpledialog
import mysql.connector

# Función para mostrar un cuadro de diálogo y obtener una respuesta del usuario
def show_message_dialog(message, address):
    root = tk.Tk()
    root.withdraw() 
    response = simpledialog.askstring("Mensaje recibido", f"Mensaje de {address}: {message}\n\nEscribe tu respuesta:")
    root.destroy()  # Cierra la ventana principal después de obtener la respuesta
    return response  # Devuelve la respuesta del usuario

# Función para manejar la comunicación con un cliente TCP
def handle_tcp_client(client_socket, address):
    while True:
        try:
            message = client_socket.recv(1024)  # Espera a recibir un mensaje del cliente
            if not message:
                break
            message_decoded = message.decode('utf-8')
            print(f"Mensaje recibido de {address}: {message_decoded}")  # Imprime el mensaje recibido y la dirección del remitente
            store_message_in_db(address, message_decoded)  # Almacena el mensaje en la base de datos
        except:
            break
    client_socket.close()

# Función para almacenar un mensaje en la base de datos MySQL
def store_message_in_db(address, message):
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='1221',
            database='servidor_mensajes'
        )
        cursor = connection.cursor()
        query = "INSERT INTO mensajes (direccion, mensaje) VALUES (%s, %s)"
        cursor.execute(query, (str(address), message))
        connection.commit()
        cursor.close()
        connection.close()
    except mysql.connector.Error as error:
        print(f"Error al conectar con la base de datos: {error}")

# Configuración del servidor UDP
udp_server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_server.bind(('localhost', 9999))
#udp_server.bind(('192.168.234.88', 9999))  # Asocia el socket UDP a la dirección IP y puerto especificados

# Configuración del servidor TCP
tcp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_server.bind(('localhost', 9998))
#tcp_server.bind(('192.168.234.88', 9998))  # Asocia el socket TCP a la dirección IP y puerto especificados
tcp_server.listen(5)  # Escucha conexiones entrantes

print("Servidor UDP y TCP listo para recibir mensajes...")

# Bucle principal del servidor para manejar múltiples clientes
def udp_handler():
    while True:
        message, address = udp_server.recvfrom(1024)  # Espera a recibir un mensaje de un cliente UDP
        message_decoded = message.decode('utf-8')
        print(f"Conexión UDP establecida con {address}")
        print(f"Mensaje recibido de {address}: {message_decoded}")  # Imprime el mensaje recibido y la dirección del remitente
        store_message_in_db(address, message_decoded)  # Almacena el mensaje en la base de datos
        response = show_message_dialog(message_decoded, address)  # Muestra el cuadro de diálogo y obtiene la respuesta del usuario
        if response:  # Verifica si el usuario ingresó una respuesta
            print(f"Respuesta enviada a {address}: {response}")  # Imprime la respuesta en la consola
            udp_server.sendto(response.encode('utf-8'), address)  # Envía la respuesta del usuario de vuelta al cliente

def tcp_handler():
    while True:
        client_socket, address = tcp_server.accept()  # Acepta una nueva conexión TCP
        print(f"Conexión TCP establecida con {address}")
        threading.Thread(target=handle_tcp_client, args=(client_socket, address)).start()  # Maneja el cliente TCP en un nuevo hilo

# Inicia los manejadores UDP y TCP en hilos separados
threading.Thread(target=udp_handler).start()
threading.Thread(target=tcp_handler).start()
