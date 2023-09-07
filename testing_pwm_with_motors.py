import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BOARD)
in1_pin = 3  # Use physical pin 3 for IN1
in2_pin = 5  # Use physical pin 5 for IN2
pwm_pin = 12  # Use physical pin 12 for EnA (PWM)
GPIO.setup(in1_pin, GPIO.OUT)
GPIO.setup(in2_pin, GPIO.OUT)
GPIO.setup(pwm_pin, GPIO.OUT)

# Initialize PWM
pwm = GPIO.PWM(pwm_pin, 10)  # Frequency = 100 Hz
pwm.start(70)  # Start PWM with 0% duty cycle
current_duty_cycle = 0
direction = "f"
# Motor direction
def set_motor_direction(direction):
    if direction == "f":
        GPIO.output(in1_pin, GPIO.HIGH)
        GPIO.output(in2_pin, GPIO.LOW)
    elif direction == "b":
        GPIO.output(in1_pin, GPIO.LOW)
        GPIO.output(in2_pin, GPIO.HIGH)
    else:
        GPIO.output(in1_pin, GPIO.LOW)
        GPIO.output(in2_pin, GPIO.LOW)

try:
    while True:
        # Display duty cycle in the terminal
        print(f"Duty Cycle: {current_duty_cycle}%")

        if current_duty_cycle >= 0 and direction == "f":

            current_duty_cycle += 1
        # Set motor direction
        #direction = input("Enter 'forward' or 'backward': ")
            set_motor_direction(direction)

        # Set PWM duty cycle
        #current_duty_cycle = int(input("Enter duty cycle (0 to 100): "))
        #current_duty_cycle = max(0, min(100, current_duty_cycle))
            pwm.ChangeDutyCycle(current_duty_cycle)

            time.sleep(1)

            if current_duty_cycle == 100 :
                current_duty_cycle = 0 
                direction = "b"

        elif current_duty_cycle >=0 and direction == "b":

            current_duty_cycle +=1
            set_motor_direction(direction)
            pwm.ChangeDutyCycle(current_duty_cycle)

            time.sleep(1)

            if current_duty_cycle == 100:
                current_duty_cycle = 0
                direction = "f"
        


except KeyboardInterrupt:
    # Clean up GPIO on Ctrl+C
    pwm.stop()
    GPIO.cleanup()
