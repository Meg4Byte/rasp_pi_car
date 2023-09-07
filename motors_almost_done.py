import RPi.GPIO as GPIO
import time
import keyboard
import multiprocessing
import socket


# Setup GPIO

GPIO.setmode(GPIO.BOARD)

        #use physical pin numbering

in1_pin = 16  
in2_pin = 18  
pwm_pin_1 = 12  ## EnA (PWM)

in3_pin = 11
in4_pin = 13
pwm_pin_2 = 35  ##EnB (PWM)

motor_freq = 500  # ne vristi motor

GPIO.setup(in1_pin, GPIO.OUT)
GPIO.setup(in2_pin, GPIO.OUT)
GPIO.setup(pwm_pin_1, GPIO.OUT)
GPIO.setup(in3_pin, GPIO.OUT)
GPIO.setup(in4_pin, GPIO.OUT)
GPIO.setup(pwm_pin_2, GPIO.OUT)

lower_speed_limit = 35                   #min duty cycle
upper_speed_limit = 97                   #max duty cycle

current_duty_cycle_1 = lower_speed_limit           # Duty cycle for motor 1
current_duty_cycle_2 = lower_speed_limit           # Duty cycle for motor 2
   
debounce_time = 0.2
turning_time = 0.75                         #decrease speed while turning

last_key = None
key_press_count = 0
key_press_start_time = None

#start pwm 
pwm_1 = GPIO.PWM(pwm_pin_1, motor_freq)   
pwm_2 = GPIO.PWM(pwm_pin_2, motor_freq)   

pwm_1.start(current_duty_cycle_1)  
pwm_2.start(current_duty_cycle_2)  

        #settiing up server conncetion 

# Set up socket server
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.1.15', 8001))  # Use the Pi's IP address
server_socket.listen(1)

conn, addr = server_socket.accept()

#this is the more realsitic acceleration profile , based on various acceleration profiles of varius motors 
def quadratic_acceleration_profile(time_difference , coefficient_1 , coefficient_2 , coefficient_3):

    #give me back duty cycle   
    return coefficient_1 * time_difference + coefficient_2 * time_difference ** 2 + coefficient_3

#this is simple linear slowing down profile 
def linear_slow_down_profile(time_difference):

    deceleration_rate = 15.0
    desired_duty_cycle_1 = current_duty_cycle_1 - deceleration_rate * time_difference
    desired_duty_cycle_2 = current_duty_cycle_2 - deceleration_rate * time_difference

    return max(lower_speed_limit, desired_duty_cycle_1 ) , max(lower_speed_limit, desired_duty_cycle_2 ) 

#control of acceleration and deceleration
def set_motor_speed(speed):

    global current_duty_cycle_1, current_duty_cycle_2

    #speed up   
    if speed == "3":
        
            #implement gears
            if lower_speed_limit <= (current_duty_cycle_1 and current_duty_cycle_2) < 50:

                desired_duty_cycle_1 = round(current_duty_cycle_1 + quadratic_acceleration_profile(1 , 0.4 , 8 , 0) , 2)
                desired_duty_cycle_2 = round(current_duty_cycle_2 + quadratic_acceleration_profile(1 , 0.4 , 8 , 0) , 2) 

                current_duty_cycle_1 = min(desired_duty_cycle_1, 50)
                current_duty_cycle_2 = min(desired_duty_cycle_2, 50)

                print("first gear")
                
            elif  50 <= (current_duty_cycle_1 and current_duty_cycle_2) < 75:

                desired_duty_cycle_1 = round(current_duty_cycle_1 + quadratic_acceleration_profile(0.5 , 1.5 , 20 , 2) , 2)
                desired_duty_cycle_2 = round(current_duty_cycle_2 + quadratic_acceleration_profile(0.5 , 1.5 , 20 , 2) , 2) 

                current_duty_cycle_1 = min(desired_duty_cycle_1, 75)
                current_duty_cycle_2 = min(desired_duty_cycle_2, 75)

                print("second gear")
                
            elif 75 <= (current_duty_cycle_1 and current_duty_cycle_2) <= upper_speed_limit:

                desired_duty_cycle_1 = round(current_duty_cycle_1 + quadratic_acceleration_profile(0.2 , 10 , 31 , 4.5) , 2)
                desired_duty_cycle_2 = round(current_duty_cycle_2 + quadratic_acceleration_profile(0.2 , 10 , 31 , 4.5) , 2) 

                current_duty_cycle_1 = min(desired_duty_cycle_1, upper_speed_limit)
                current_duty_cycle_2 = min(desired_duty_cycle_2, upper_speed_limit)

                print("third gear")
                
            
            pwm_1.ChangeDutyCycle(current_duty_cycle_1)
            pwm_2.ChangeDutyCycle(current_duty_cycle_2)

            #display the result 
            print(f"Duty Cycle: {current_duty_cycle_1}%")
            print(f"Duty Cycle: {current_duty_cycle_2}%")

            time.sleep(0.01)

    #slow down
    elif speed == "e":

        desired_duty_cycle_1 = linear_slow_down_profile(0.1)[0]
        desired_duty_cycle_2 = linear_slow_down_profile(0.1)[1]

        desired_duty_cycle_1 = max(lower_speed_limit, desired_duty_cycle_1)
        desired_duty_cycle_2 = max(lower_speed_limit, desired_duty_cycle_2)

        current_duty_cycle_1 = max(desired_duty_cycle_1, lower_speed_limit)
        current_duty_cycle_2 = max(desired_duty_cycle_2, lower_speed_limit)

        pwm_1.ChangeDutyCycle(current_duty_cycle_1)
        pwm_2.ChangeDutyCycle(current_duty_cycle_2)

        #display the result 
        print(f"Duty Cycle: {current_duty_cycle_1}%")
        print(f"Duty Cycle: {current_duty_cycle_2}%")

        time.sleep(0.01)

#direction control
def set_motor_direction(direction):

    global current_duty_cycle_1 , current_duty_cycle_2

    if direction == "w":

        GPIO.output(in1_pin, GPIO.HIGH)
        GPIO.output(in2_pin, GPIO.LOW)
        GPIO.output(in3_pin, GPIO.HIGH)
        GPIO.output(in4_pin, GPIO.LOW)

    elif direction == "s":

        GPIO.output(in1_pin, GPIO.LOW)
        GPIO.output(in2_pin, GPIO.HIGH)
        GPIO.output(in3_pin, GPIO.LOW)
        GPIO.output(in4_pin, GPIO.HIGH)

    elif direction == "a":

        ##need adjustement
        #pwm_1.ChangeDutyCycle(max(round(current_duty_cycle_1 - linear_slow_down_profile(turning_time)[0] , 2) , lower_speed_limit))
       
        pwm_1.ChangeDutyCycle(max(round(current_duty_cycle_1 - linear_slow_down_profile(turning_time)[0] , 2) , lower_speed_limit))
        pwm_2.ChangeDutyCycle(current_duty_cycle_2)

        print("direction : {}".format(direction))
        print("duty cycle 1 : {}%".format(max(round(current_duty_cycle_1 - linear_slow_down_profile(turning_time)[0] , 2) , lower_speed_limit)))
        print("duty cycle 2 : {}%".format(current_duty_cycle_2))

    elif direction == "d":

        ##need adjustement
        #pwm_2.ChangeDutyCycle(max(round(current_duty_cycle_2 - linear_slow_down_profile(turning_time)[1] , 2) , lower_speed_limit))
        
        pwm_1.ChangeDutyCycle(current_duty_cycle_1)
        pwm_2.ChangeDutyCycle(max(round(current_duty_cycle_2 - linear_slow_down_profile(turning_time)[1] , 2) , lower_speed_limit))

        print("direction : {}".format(direction))
        print("duty cycle 1 : {}%".format(current_duty_cycle_1))
        print("duty cycle 2 : {}%".format(max(round(current_duty_cycle_2 - linear_slow_down_profile(turning_time)[1] , 2) , lower_speed_limit)))

    else:

        GPIO.output(in1_pin, GPIO.LOW)
        GPIO.output(in2_pin, GPIO.LOW)
        GPIO.output(in3_pin, GPIO.LOW)
        GPIO.output(in4_pin, GPIO.LOW)

def turn_on_motor():
    
    current_duty_cycle_1  = lower_speed_limit
    current_duty_cycle_2  = lower_speed_limit
    #time.sleep(0.1*(1/motor_freq))  # Delay of 1 msec
    pwm_1.start(current_duty_cycle_1)  
    pwm_2.start(current_duty_cycle_2)  

    time.sleep(0.001)   # Delay of 1 msec


if __name__ == "__main__":

    temp_flag = False
   
    """
    while motor_on == False:

        print("inside motor")
        #_ = input("press t to turn on the motor:")

        _ = conn.recv(1024).decode()

        if not _ : 
            break

        if _ != 't':

            print("FAILED TO TURN ON MOTOR")

        else:

            motor_on = True
            turn_on_motor()
            break

    print("motor is on now")

    """
    try:

        while True :
  

            while True:
                data = conn.recv(1024).decode()

                if data == "t":
                    print("motor is now on, start driving")
                    temp_flag = True

                if temp_flag:
                    if data in ['w', 's', 'a', 'd']:

                        # Apply software filtering
                        if data == last_key:
                            current_time = time.time()
                            time_elapsed = current_time - key_press_start_time

                            if time_elapsed >= debounce_time:  # Minimum time between presses
                                key_press_count += 1
                                key_press_start_time = current_time
                                
                        else:
                            last_key = data
                            key_press_count = 1
                            key_press_start_time = time.time()

                        set_motor_direction(data)
                        #print(f"Button {data} pressed {key_press_count} times")
                        

                    elif data in ['3', 'e']:
                        # Directly handle '3' and 'e' without software filtering
                        if data == '3':
                            set_motor_speed("3")
                            print("Speeding up")
                        elif data == 'e':
                            set_motor_speed("e")
                            print("Slowing down")

                    else:
                        continue

   
    except KeyboardInterrupt:

        temp_flag = False
        conn.close()
        pwm_1.stop()
        pwm_2.stop()
        GPIO.cleanup()

"""
def on_key_press(event):

    ##global speed, direction, last_press_time
    global last_press_time

    if time.time() - last_press_time > debounce_time:
        
        if event.name == 'q':
            speed = "q"
            set_motor_speed(speed)
        elif event.name == 'e':
            speed = "e"
            set_motor_speed(speed)
        elif event.name == 'w':
            direction = "w"
            set_motor_direction(direction)
        elif event.name == 's':
            direction = "s"
            set_motor_direction(direction)
        elif event.name == 'a':
            direction = "a"
            set_motor_direction(direction)
        elif event.name == 'd':
            direction = "d"
            set_motor_direction(direction)
        else:
            return

        last_press_time = time.time()


while True:
    # Your main program logic goes here
    try:

        on_key_press(keyboard.read_key())
        #keyboard.on_press(on_key_press)
        time.sleep(0.01)

    except KeyboardInterrupt:
    
        pwm_1.stop()
        pwm_2.stop()
        GPIO.cleanup()
"""