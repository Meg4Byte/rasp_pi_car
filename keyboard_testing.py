import keyboard


while True:
    if keyboard.is_pressed('w'):
        #client_socket.send('w'.encode())
        print("w")
    elif keyboard.is_pressed('s'):
        #client_socket.send('s'.encode())
        print("s")
    elif keyboard.is_pressed('a'):
        #client_socket.send('a'.encode())
        print("a")
    elif keyboard.is_pressed('d'):
        #client_socket.send('d'.encode())
        print("d")
    elif keyboard.is_pressed('q'):
        break