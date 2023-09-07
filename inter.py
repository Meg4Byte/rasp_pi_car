import RPi.GPIO as GPIO
import time
import pygame
import threading

# Initialize Pygame
pygame.init()

# Your motor control functions and setup code

# Define a function to handle keyboard events
def handle_keyboard_events():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    print("Key 'w' is pressed")
                    # Perform action for pressing 'w' key
                elif event.key == pygame.K_s:
                    print("Key 's' is pressed")
                    # Perform action for pressing 's' key
                elif event.key == pygame.K_a:
                    print("Key 'a' is pressed")
                    # Perform action for pressing 'a' key
                elif event.key == pygame.K_d:
                    print("Key 'd' is pressed")
                    # Perform action for pressing 'd' key
                elif event.key == pygame.K_q:
                    print("Key 'q' is pressed")
                    # Perform action for pressing 'q' key
                elif event.key == pygame.K_e:
                    print("Key 'e' is pressed")
                    # Perform action for pressing 'e' key

# Start the thread for handling keyboard events
keyboard_thread = threading.Thread(target=handle_keyboard_events)
keyboard_thread.daemon = True
keyboard_thread.start()

# Your main loop code here
while True:
    try:
        # Your code for controlling the motors goes here
        # ...

        pygame.event.pump()  # Process Pygame events

        time.sleep(0.1)  # Add a small delay to avoid excessive CPU usage
    except KeyboardInterrupt:
        break

# Clean up GPIO
GPIO.cleanup()
