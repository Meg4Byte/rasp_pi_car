import RPi.GPIO as GPIO
import time
import keyboard


# Setup GPIO
GPIO.setmode(GPIO.BOARD)

in1_pin = 16  # Use physical pin 3 for IN1
in2_pin = 18  # Use physical pin 5 for IN2
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

global current_duty_cycle_1 , current_duty_cycle_2

current_duty_cycle_1 = 50           #dutry cycle for motor 1
current_duty_cycle_2 = 50           #dutry cycle for motor 2
direction = "f"

# Initialize PWM
pwm_1 = GPIO.PWM(pwm_pin_1, 10)     # do check out optimal ??
pwm_1.start(current_duty_cycle_1)                     # Start PWM with 0% duty cycle

pwm_2 = GPIO.PWM(pwm_pin_2, 10)  # do check out optimal ??
pwm_2.start(current_duty_cycle_2)  # Start PWM with 0% duty cycle


reduce_speed_left_motor = 10
reduce_speed_right_motor = 10

increase_speed_left_motor = 20
increase_speed_right_motor = 20

debounce_time = 0.05
last_press_time = time.time()

def set_motor_speed(speed):

    global current_duty_cycle_1 , current_duty_cycle_2

    if speed == "q":

        current_duty_cycle_1 += increase_speed_left_motor
        current_duty_cycle_2 += increase_speed_right_motor

        pwm_1.ChangeDutyCycle(min(current_duty_cycle_1 , 100))
        pwm_2.ChangeDutyCycle(min(current_duty_cycle_2 , 100))

        #pwm_1.start(current_duty_cycle_1 + increase_speed_left_motor)
        #pwm_2.start(current_duty_cycle_2 + increase_speed_right_motor)

        print("duty clycle 1 : {}%".format(current_duty_cycle_1 ))

        print("duty clycle 2 : {}%".format(current_duty_cycle_2 ))



    elif speed == "e":
        
        current_duty_cycle_1 -= reduce_speed_left_motor
        current_duty_cycle_2 -= reduce_speed_right_motor

        pwm_1.ChangeDutyCycle(max(current_duty_cycle_1 , 0))
        pwm_2.ChangeDutyCycle(max(current_duty_cycle_2 , 0))

        #pwm_1.start(current_duty_cycle_1 - reduce_left_motor)
        #pwm_2.start(current_duty_cycle_2 - reduce_right_motor)

        print("duty clycle 1 : {}%".format(current_duty_cycle_1 ))

        print("duty clycle 2 : {}%".format(current_duty_cycle_2 ))
        


def ignite_motor(contact):

    return True if contact == "t" else False

# Motor direction
def set_motor_direction(direction):

    global current_duty_cycle_1 , current_duty_cycle_2

    if direction == "w":

        GPIO.output(in1_pin, GPIO.HIGH)
        GPIO.output(in2_pin, GPIO.LOW)
        GPIO.output(in3_pin, GPIO.HIGH)
        GPIO.output(in4_pin, GPIO.LOW)

        print("direction : {}".format(direction))


    elif direction == "s":

        GPIO.output(in1_pin, GPIO.LOW)
        GPIO.output(in2_pin, GPIO.HIGH)
        GPIO.output(in3_pin, GPIO.LOW)
        GPIO.output(in4_pin, GPIO.HIGH)

        print("direction : {}".format(direction))


    elif direction == "a":

        ##this should change speed a bit 
        pwm_1.ChangeDutyCycle(current_duty_cycle_1 - reduce_speed_left_motor-20)
        ##pwm_2.ChangeDutyCycle(current_duty_cycle_2 + reduce_right_motor)
        
        print("direction : {}".format(direction))

        print("duty cycle 1 : {}%".format(current_duty_cycle_1-reduce_speed_left_motor))

        print("duty cycle 2 : {}%".format(current_duty_cycle_2))

    elif direction == "d":

        pwm_2.ChangeDutyCycle(current_duty_cycle_2 - reduce_speed_right_motor-30)

        print("direction : {}".format(direction))

        print("duty cycle 1 :{}%".format(current_duty_cycle_1))

        print("duty cycle 2 :{}%".format(current_duty_cycle_2-reduce_speed_right_motor))

    else:

        GPIO.output(in1_pin, GPIO.LOW)
        GPIO.output(in2_pin, GPIO.LOW)
        GPIO.output(in3_pin, GPIO.LOW)
        GPIO.output(in4_pin, GPIO.LOW)


try:
    while True:
        
          # Display duty cycle in the terminal
        #print(f"Duty Cycle Motor 1 : {current_duty_cycle_1}%")
        #print(f"Duty Cycle Motor 2 : {current_duty_cycle_2}%")
        #print("direction : {}".format(direction))


        # Wait for button press
        while True:

            if time.time() - last_press_time > debounce_time:

                key = input("Press 'q' to increase duty cycle, 'e' to decrease: ")

                if key == 'q':

                    speed = "q"
                    set_motor_speed(speed)

                elif key == 'e':

                    speed = "e"
                    set_motor_speed(speed)

                elif key == 'w':

                    direction = "w"
                    set_motor_direction(direction)

                elif key == 's':

                    direction = "s"
                    set_motor_direction(direction)

                elif key == 'a':

                    direction = "a"
                    set_motor_direction(direction)

                elif key == 'd':

                    direction = "d"
                    set_motor_direction(direction)

                else:

                    continue

                last_press_time = time.time()

                break



        """if current_duty_cycle_1 or current_duty_cycle_2 >= 0 and direction == "f":

            current_duty_cycle += 1
        # Set motor direction
        #direction = input("Enter 'forward' or 'backward': ")
            set_motor_direction(direction)

        # Set PWM duty cycle
        #current_duty_cycle = int(input("Enter duty cycle (0 to 100): "))
        #current_duty_cycle = max(0, min(100, current_duty_cycle))
            pwm_1.ChangeDutyCycle(current_duty_cycle_1)
            pwm_2.ChangeDutyCycle(current_duty_cycle_2)
            time.sleep(1)

            if current_duty_cycle_1 or current_duty_cycle_2 == 100 :
                current_duty_cycle_1 , current_duty_cycle_2 = 0 , 0 
                direction = "b"

        elif current_duty_cycle >=0 and direction == "b":

            current_duty_cycle +=1
            set_motor_direction(direction)
            pwm.ChangeDutyCycle(current_duty_cycle)

            time.sleep(1)

            if current_duty_cycle == 100:
                current_duty_cycle = 0
                direction = "f
                
            """
        


except KeyboardInterrupt:

    # Clean up GPIO on Ctrl+C
    pwm_1.stop()
    pwm_2.stop()
    GPIO.cleanup()
