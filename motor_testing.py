from gpiozero import Motor, PWMLED
import keyboard
import time

# Set up the motor objects
motor_a = Motor(forward=2, backward=3)
motor_b = Motor(forward=17, backward=27)

# Set up the PWM outputs using PWMLED (hardware PWM)
pwm_a = PWMLED(18)
pwm_b = PWMLED(19)

# Initial motor speeds (range from 0 to 1)
forward_speed = 0.5
backward_speed = 0.5
left_motor_speed = forward_speed
right_motor_speed = forward_speed

# Speed increment for 'w' and 's' keys
speed_increment = 0.2

def update_motors():
    # Set motor speeds based on direction and speed variables
    motor_a.forward(speed=forward_speed * left_motor_speed)
    motor_b.forward(speed=forward_speed * right_motor_speed)
    pwm_a.value = left_motor_speed
    pwm_b.value = right_motor_speed

def on_key_press(event):
    global forward_speed, left_motor_speed, right_motor_speed

    if event.name == 'up':
        # Move forward
        forward_speed = 0.5
        left_motor_speed = 1.0
        right_motor_speed = 1.0
    elif event.name == 'down':
        # Move backward
        forward_speed = 0.5
        left_motor_speed = -1.0
        right_motor_speed = -1.0
    elif event.name == 'left':
        # Turn left
        left_motor_speed = 0.1
        right_motor_speed = 1.0
    elif event.name == 'right':
        # Turn right
        left_motor_speed = 1.0
        right_motor_speed = 0.1
    elif event.name == 's':
        # Slow down (brake)
        left_motor_speed *= 0.8
        right_motor_speed *= 0.8
    elif event.name == 'w':
        # Speed up
        left_motor_speed += speed_increment
        right_motor_speed += speed_increment
        # Cap the speed at 1.0
        left_motor_speed = min(left_motor_speed, 1.0)
        right_motor_speed = min(right_motor_speed, 1.0)
    elif event.name == 'q':
        # Stop the motors and exit the program
        motor_a.stop()
        motor_b.stop()
        pwm_a.off()
        pwm_b.off()
        keyboard.unhook_all()
        quit()

    # Update motors based on the new settings
    update_motors()

if __name__ == "__main__":
    # Set up the keyboard event handlers
    keyboard.on_press(on_key_press)

    # Update motors to initial settings
    update_motors()

    try:
        while True:
            # Do other tasks if needed
            time.sleep(0.1)
    except KeyboardInterrupt:
        # Stop the motors and exit gracefully if Ctrl+C is pressed
        motor_a.stop()
        motor_b.stop()
        pwm_a.off()
        pwm_b.off()
