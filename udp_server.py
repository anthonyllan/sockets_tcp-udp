import socket
import tkinter as tk
from tkinter import simpledialog

def show_message_dialog(message):
    root = tk.Tk()
    root.withdraw()  
    response = simpledialog.askstring("Mensaje recibido", f"Mensaje de {address}: {message}\n\nEscribe tu respuesta:")
    root.destroy() 
    return response 

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(('192.168.234.88', 9999))  

print("Servidor UDP listo para recibir mensajes...")

while True:
    message, address = server.recvfrom(1024)  
    print(f"Mensaje recibido de {address}: {message.decode('utf-8')}")  
    response = show_message_dialog(message.decode('utf-8')) 
    if response:  
        print(f"Respuesta enviada a {address}: {response}") 
        server.sendto(response.encode('utf-8'), address)  
        
