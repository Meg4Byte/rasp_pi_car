from evdev import InputDevice, categorize, ecodes

# Find the event ID of your gamepad. You can check it with the 'evtest' command.
event_id = '/dev/input/eventX'  # Replace 'X' with the event number of your gamepad.

gamepad = InputDevice(event_id)

print("Gamepad found:", gamepad)

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        print(categorize(event))
