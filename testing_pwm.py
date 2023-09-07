import RPi.GPIO as GPIO
import time

# Setup GPIO
GPIO.setmode(GPIO.BCM)
pwm_pin = 18  # Use GPIO 18 for PWM
GPIO.setup(pwm_pin, GPIO.OUT)

# Initialize PWM
pwm = GPIO.PWM(pwm_pin, 100000)  # Frequency = 100 Hz
pwm.start(0)  # Start PWM with 0% duty cycle
current_duty_cycle = 0

# Software Debouncing
debounce_time = 0.1
last_press_time = time.time()

try:
    while True:
        # Display duty cycle in the terminal
        print(f"Duty Cycle: {current_duty_cycle}%")

        # Wait for button press
        while True:
            if time.time() - last_press_time > debounce_time:
                key = input("Press 't' to increase duty cycle, 'f' to decrease: ")
                if key == 't':
                    current_duty_cycle = min(current_duty_cycle + 10, 100)
                elif key == 'f':
                    current_duty_cycle = max(current_duty_cycle - 10, 0)
                else:
                    continue
                last_press_time = time.time()
                break

        # Update PWM duty cycle
        pwm.ChangeDutyCycle(current_duty_cycle)

except KeyboardInterrupt:
    # Clean up GPIO on Ctrl+C
    pwm.stop()
    GPIO.cleanup()
