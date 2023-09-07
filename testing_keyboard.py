import keyboard
import time
# Your while loop code here
while True:
    try:
        if keyboard.is_pressed('w'):
            print("Key 'w' is pressed")
            # Perform action for pressing 'w' key
        elif keyboard.is_pressed('s'):
            print("Key 's' is pressed")
            # Perform action for pressing 's' key
        else:
            # Perform other actions within the loop
           print("time is : {}".format(time.time())) 
           time.sleep(0.1)
    except KeyboardInterrupt:
        break
