import socket
import RPi.GPIO as GPIO
import motors_almost_done as mc
# Initialize GPIO and motor control functions

# Set up socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.23', 8004))  # Use the Pi's IP address
server_socket.listen(1)

conn, addr = server_socket.accept()

while True:
    
    data = conn.recv(1024).decode()
    if not data:
        break
    # Process the received data and control the motors
    if data == 'w':
        # Move forward
        print("Moving forward")
        mc.set_motor_direction("w")
        ##mc.set_motor_speed("q")
    elif data == 's':
        # Move backward
        print("Moving backward")
        mc.set_motor_direction("s")
    elif data == 'a':
        # Turn left
        print("Turning left")
        mc.set_motor_direction("a")
    elif data == 'd':
        # Turn right
        print("Turning right")
        mc.set_motor_direction("d")
    elif data == 'q':
        mc.set_motor_speed("q")
        print("speeding up")
    elif data == 'e':
        mc.set_motor_speed("e")
        print("slowing down")
    elif data == 't':
        mc.turn_on_motor()
        print("motor on")
    

conn.close()
