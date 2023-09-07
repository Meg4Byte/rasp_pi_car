from evdev import InputDevice, categorize, ecodes

# Find the event ID of your gamepad. You can check it with the 'evtest' command.
event_id = '/dev/input/event7'  # Replace 'X' with the event number of your gamepad.

gamepad = InputDevice(event_id)

print("Gamepad found:", gamepad)

for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        key_event = categorize(event)

        if key_event.keystate == 1:  # Key press event
            if key_event.keycode == 'BTN_NORTH':
                print("Button 'A' pressed")
                # Perform action for pressing 'A' button

            elif key_event.keycode == 'BTN_SOUTH':
                print("Button 'B' pressed")
                # Perform action for pressing 'B' button

            # Add other button mappings as needed

    elif event.type == ecodes.EV_ABS:
        abs_event = categorize(event)

        if abs_event.event.code == ecodes.ABS_X:
            x_axis_value = abs_event.event.value
            print(f"Analog stick X axis value: {x_axis_value}")

            # Process X-axis movement here

        elif abs_event.event.code == ecodes.ABS_Y:
            y_axis_value = abs_event.event.value
            print(f"Analog stick Y axis value: {y_axis_value}")

            # Process Y-axis movement here

    elif event.type == ecodes.EV_SYN:
        # Syn event indicates the end of a set of events, you can use it to synchronize data processing
        pass
