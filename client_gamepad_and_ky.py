import socket
import pygame

# Set up socket client
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.1.16', 8001))  # Replace with your Pi's IP

# Initialize Pygame and the joystick
pygame.init()
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"Using joystick: {joystick.get_name()}")
print("current joystick is : {}".format(pygame.joystick.Joystick(0)))

# Define the buttons and their corresponding commands
button_commands = {
    0: 'w',
    1: 's',
    2: 'a',
    3: 'd',
    4: 'e',
    5: '3',
    6: 't'
}

try:
    while True:
        pygame.event.get()

        if joystick.get_button(7):  # Check if button is pressed
            client_socket.send('t'.encode())
        elif joystick.get_button(2):  # Check if button is pressed
            client_socket.send('q'.encode())
        elif joystick.get_button(5):  # Check if button is pressed
            client_socket.send('s'.encode())
        elif joystick.get_button(6):  # Check if button is pressed
            client_socket.send('a'.encode())
        elif joystick.get_button(4):  # Check if button is pressed
            client_socket.send('d'.encode())
        elif joystick.get_button(8):  # Check if button is pressed
            client_socket.send('e'.encode())
        elif joystick.get_button(9):  # Check if button is pressed
            client_socket.send('3'.encode())
        
        
except KeyboardInterrupt:
    pass

# Close the client socket and Pygame
client_socket.close()
pygame.quit()
