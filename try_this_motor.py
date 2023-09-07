import RPi.GPIO as GPIO
import time
import keyboard

# Your motor control functions and setup code
# ...

# Define the speed increase step
speed_step = 10

# Setup GPIO
GPIO.setmode(GPIO.BOARD)

in1_pin = 3  # Use physical pin 3 for IN1
in2_pin = 5  # Use physical pin 5 for IN2
pwm_pin_1 = 12  # Use physical pin 12 for EnA (PWM)

in3_pin = 11
in4_pin = 13
pwm_pin_2 = 35

GPIO.setup(in1_pin, GPIO.OUT)
GPIO.setup(in2_pin, GPIO.OUT)
GPIO.setup(pwm_pin_1, GPIO.OUT)

GPIO.setup(in3_pin, GPIO.OUT)
GPIO.setup(in4_pin, GPIO.OUT)
GPIO.setup(pwm_pin_2, GPIO.OUT)

lower_speed_limit = 50                   #min duty cycle
upper_speed_limit = 97                   #max duty cycle

current_duty_cycle_1 = lower_speed_limit           # Duty cycle for motor 1
current_duty_cycle_2 = lower_speed_limit           # Duty cycle for motor 2
direction = "s"       

##last_press_time = time.time()

# Initialize PWM
pwm_1 = GPIO.PWM(pwm_pin_1, 100)   # Frequency = 100 Hz
pwm_1.start(current_duty_cycle_1)  # Start PWM with 0% duty cycle

pwm_2 = GPIO.PWM(pwm_pin_2, 100)   # Frequency = 100 Hz
pwm_2.start(current_duty_cycle_2)  # Start PWM with 0% duty cycle

                             # Initial direction

debounce_time = 0.01

turning_speed = 15

while True:
    try:
        if keyboard.is_pressed('q'):
            print("q pressed")
            
            temp_1 = current_duty_cycle_1 + speed_step
            temp_2 = current_duty_cycle_2 + speed_step

            current_duty_cycle_1 = min(temp_1, upper_speed_limit)
            current_duty_cycle_2 = min(temp_2, upper_speed_limit)

            pwm_1.ChangeDutyCycle(current_duty_cycle_1)
            pwm_2.ChangeDutyCycle(current_duty_cycle_2)

            # Display the result
            print(f"Duty Cycle: {current_duty_cycle_1}%")
            print(f"Duty Cycle: {current_duty_cycle_2}%")

            time.sleep(0.01)

        elif keyboard.is_pressed('e'):
            print("e pressed")
            
            temp_1 = current_duty_cycle_1 - speed_step
            temp_2 = current_duty_cycle_2 - speed_step

            current_duty_cycle_1 = max(temp_1, lower_speed_limit)
            current_duty_cycle_2 = max(temp_2, lower_speed_limit)

            pwm_1.ChangeDutyCycle(current_duty_cycle_1)
            pwm_2.ChangeDutyCycle(current_duty_cycle_2)

            # Display the result
            print(f"Duty Cycle: {current_duty_cycle_1}%")
            print(f"Duty Cycle: {current_duty_cycle_2}%")

            time.sleep(0.01)

        elif keyboard.is_pressed('w'):
            print("w pressed")
            direction = "w"
            #set_motor_direction(direction)

        elif keyboard.is_pressed('s'):
            print("s pressed")
            direction = "s"
            #set_motor_direction(direction)

        elif keyboard.is_pressed('a'):
            print("a pressed")
            direction = "a"
            #set_motor_direction(direction)

        elif keyboard.is_pressed('d'):
            print("d pressed")
            direction = "d"
            #set_motor_direction(direction)

    except KeyboardInterrupt:
        break

# Clean up GPIO
GPIO.cleanup()