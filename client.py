import socket
import keyboard  

# Set up socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.23', 8000))                   # Replace with your Pi's IP

while True:
    if keyboard.is_pressed('w'):
        client_socket.send('w'.encode())
    elif keyboard.is_pressed('s'):
        client_socket.send('s'.encode())
    elif keyboard.is_pressed('a'):
        client_socket.send('a'.encode())
    elif keyboard.is_pressed('d'):
        client_socket.send('d'.encode())
    elif keyboard.is_pressed('e'):
        client_socket.send('e'.encode())
    elif keyboard.is_pressed('3'):
        client_socket.send('3'.encode())
    elif keyboard.is_pressed('t'):
        client_socket.send('t'.encode())
    elif keyboard.is_pressed('q'):
        break

client_socket.close()
