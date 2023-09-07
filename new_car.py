# import curses and GPIO
import curses
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

#set GPIO numbering mode and define output pins
GPIO.setmode(GPIO.BOARD)

global lower_speed_limit
global upper_speed_limit
global servo_duty_cycle

lower_speed_limit = 35                   #min duty cycle
upper_speed_limit = 100                  #max duty cycle
servo_duty_cycle = 7.5                  #needs to be changed

motor1a = 7
motor1b = 11
pwm_pin_2 = 22

motor2a = 13
motor2b = 16
pwm_pin_1 = 15

servo_pin = 37

left_turn_diode  = 29       #orange diodes
right_turn_diode = 31       
slow_down_diode  = 33       #red diode
motor_on_diode   =35

motor_freq = 2000
servo_freq = 50

GPIO.setup(left_turn_diode, GPIO.OUT)
GPIO.setup(right_turn_diode, GPIO.OUT)
GPIO.setup(slow_down_diode, GPIO.OUT)
GPIO.setup(motor_on_diode, GPIO.OUT)


GPIO.setup(motor1a,GPIO.OUT)
GPIO.setup(motor1b,GPIO.OUT)
GPIO.setup(pwm_pin_1, GPIO.OUT)
GPIO.setup(motor2a,GPIO.OUT)
GPIO.setup(motor2b,GPIO.OUT)
GPIO.setup(pwm_pin_2, GPIO.OUT)
GPIO.setup(servo_pin, GPIO.OUT)
#pwm_1 = GPIO.PWM(pwm_pin_1, motor_freq)   
#pwm_2 = GPIO.PWM(pwm_pin_2, motor_freq) 

pwm_servo = GPIO.PWM(servo_pin, servo_freq)
pwm_servo.start(servo_duty_cycle)



# Get the curses window, turn off echoing of keyboard to screen, turn on
# instant (no waiting) key response, and use special values for cursor keys
screen = curses.initscr()
curses.noecho()  
curses.cbreak()
curses.halfdelay(3)
screen.keypad(True)

def main(stdscr):

    global lower_speed_limit
    global upper_speed_limit
    global servo_duty_cycle

    motor_speed = 35

                     # Initialize curses

    curses.curs_set(0)  
    stdscr.clear() 
    stdscr.nodelay(1)               # Make getch() non-blocking
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    #curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

    key_is_pressed = False
    motor_is_on = False

    try:
        while True:   

            char = screen.getch()
            if char == ord('q'):

                curses.nocbreak()
                stdscr.keypad(False)
                curses.echo()
                curses.endwin()
                pwm_1.stop()
                pwm_2.stop()
                GPIO.cleanup()

                break

            elif char == ord('t') and motor_is_on == False:

                motor_is_on = True

                stdscr.addstr(0, 8, "  TURNING BATMOBILE ON " , curses.color_pair(2))
                time.sleep(1.4)
                stdscr.refresh()
                stdscr.addstr(1, 8, "  STARTING ENGINE" , curses.color_pair(2))
                time.sleep(1.4)
                stdscr.refresh()
                stdscr.addstr(2, 8, "  CALIBRATING CAMERA" , curses.color_pair(2))
                time.sleep(1.4)
                stdscr.refresh()
                stdscr.addstr(3, 8, "  CHECKING DRIVERS" , curses.color_pair(2))
                time.sleep(1.4)
                stdscr.refresh()
                stdscr.addstr(4, 8, "  UPDATING SOFTWARE" , curses.color_pair(2))
                time.sleep(1.4)
                stdscr.refresh()
                stdscr.addstr(5, 8, "  MAKING POPCORN" , curses.color_pair(2))
                time.sleep(1.4)
                stdscr.refresh()
                stdscr.addstr(6, 8, "  TURNING ON LIGHTS" , curses.color_pair(2))
                time.sleep(1.4)
                stdscr.refresh()
                stdscr.addstr(7, 8, "  TURNING ON MUSIC" , curses.color_pair(2))
                time.sleep(1.4)
                stdscr.refresh()
                stdscr.addstr(8, 8, "  BATMOBILE ON , WELCOME BACK MASTER BRUCE" , curses.color_pair(2))

                GPIO.output(motor_on_diode, GPIO.HIGH)
                pwm_1 = GPIO.PWM(pwm_pin_1, motor_freq)   
                pwm_2 = GPIO.PWM(pwm_pin_2, motor_freq) 
                pwm_1.start(motor_speed)
                pwm_2.start(motor_speed)

                time.sleep(0.1)

            elif char == curses.KEY_UP:

                GPIO.output(motor1a,GPIO.HIGH)
                GPIO.output(motor1b,GPIO.LOW)
                GPIO.output(motor2a,GPIO.HIGH)
                GPIO.output(motor2b,GPIO.LOW)

                pwm_1.ChangeDutyCycle(motor_speed)
                pwm_2.ChangeDutyCycle(motor_speed)           

                stdscr.clear()
                #stdscr.refresh()

                stdscr.addstr(0, 5, " FORWARD ")
                stdscr.addstr(1, 5, "   /\    ")
                stdscr.addstr(2, 5, "  /  \   ")
                stdscr.addstr(3, 5, " /    \  ")
                stdscr.addstr(4, 5, "         ")
                stdscr.addstr(5, 5, "         ")
                
                time.sleep(0.005)

            elif char == curses.KEY_DOWN:

                GPIO.output(motor1a,GPIO.LOW)
                GPIO.output(motor1b,GPIO.HIGH)
                GPIO.output(motor2a,GPIO.LOW)
                GPIO.output(motor2b,GPIO.HIGH)

                pwm_1.ChangeDutyCycle(motor_speed)
                pwm_2.ChangeDutyCycle(motor_speed)

                stdscr.clear()
                #stdscr.refresh()

                stdscr.addstr(0, 5, "  BACK   ")
                stdscr.addstr(1, 5, " \    /  ")
                stdscr.addstr(2, 5, "  \  /   ")
                stdscr.addstr(3, 5, "   \/    ")
                stdscr.addstr(4, 5, "         ")
                stdscr.addstr(5, 5, "         ")

                time.sleep(0.005)

            elif char == curses.KEY_RIGHT:

                GPIO.output(right_turn_diode,GPIO.HIGH)

                GPIO.output(motor1a,GPIO.HIGH)
                GPIO.output(motor1b,GPIO.LOW)
                GPIO.output(motor2a,GPIO.LOW)
                GPIO.output(motor2b,GPIO.HIGH)
                

                pwm_1.ChangeDutyCycle(0)
                pwm_2.ChangeDutyCycle(motor_speed)

                stdscr.clear()
                #stdscr.refresh()

                stdscr.addstr(0, 5, "  RIGHT  ")
                stdscr.addstr(1, 5, "   \\    ")
                stdscr.addstr(2, 5, "    \\   ")
                stdscr.addstr(3, 5, "    //   ")
                stdscr.addstr(4, 5, "   //    ")
                stdscr.addstr(5, 5, "         ")

                time.sleep(0.005)
                
            elif char == curses.KEY_LEFT:

                GPIO.output(left_turn_diode,GPIO.HIGH)

                GPIO.output(motor1a,GPIO.LOW)
                GPIO.output(motor1b,GPIO.HIGH)
                GPIO.output(motor2a,GPIO.HIGH)
                GPIO.output(motor2b,GPIO.LOW)

                pwm_1.ChangeDutyCycle(motor_speed)
                pwm_2.ChangeDutyCycle(0)

                stdscr.clear()
                #stdscr.refresh()

                stdscr.addstr(0, 5, "  LEFT   ")
                stdscr.addstr(1, 5, "  //    ")
                stdscr.addstr(2, 5, " //     ")
                stdscr.addstr(3, 5, " \\     ")
                stdscr.addstr(4, 5, "  \\    ")
                stdscr.addstr(5, 5, "         ")


                time.sleep(0.005)

            elif char == ord('f'):

                servo_duty_cycle += 0.5
                if servo_duty_cycle >= 12.5:  # Adjust this value based on your servo's range
                     servo_duty_cycle = 12.5

                pwm_servo.ChangeDutyCycle(servo_duty_cycle)

                stdscr.clear()
                #stdscr.refresh()

                stdscr.addstr(0, 5, " CAMERA TURNED RIGHT  ")
                stdscr.addstr(1, 5, "        [       ]---->>    ")
                stdscr.addstr(2, 5, "        [       ]---->>    ")
                stdscr.addstr(3, 5, "           |||             ")
                stdscr.addstr(4, 5, "           |||             ")
                stdscr.addstr(5, 5, "           |||             ")

                time.sleep(0.005)

            elif char == ord('g'):
        
                servo_duty_cycle -= 0.5

                if servo_duty_cycle <= 2.5:  # Adjust this value based on your servo's range
                    servo_duty_cycle = 2.5

                pwm_servo.ChangeDutyCycle(servo_duty_cycle)

                stdscr.clear()
                #stdscr.refresh()

                stdscr.addstr(0, 5, " CAMERA TURNED LEFT  ")
                stdscr.addstr(1, 5, " <<---- [       ]    ")
                stdscr.addstr(2, 5, " <<---- [       ]    ")
                stdscr.addstr(3, 5, "           |||       ")
                stdscr.addstr(4, 5, "           |||       ")
                stdscr.addstr(5, 5, "           |||       ")
                       
                time.sleep(0.005)

            elif char == ord('w'):
           
                if not key_is_pressed:

                    key_is_pressed = True
                    motor_speed += 20

                    if motor_speed >= upper_speed_limit:
                        motor_speed = upper_speed_limit

                #pwm_1.start(upper_speed_limit)
                    pwm_2.ChangeDutyCycle(motor_speed)
                    pwm_2.ChangeDutyCycle(motor_speed)

                    #time.sleep(0.01)
                    stdscr.clear()

                    stdscr.addstr(0, 5, " SPEEDING UP ")
                    stdscr.addstr(1, 5, "        ____  ")
                    stdscr.addstr(2, 5, "       /      ")
                    stdscr.addstr(3, 5, "      /       ")
                    stdscr.addstr(4, 5, "     /        ")
                    stdscr.addstr(5, 5, " ___/         ")



                    stdscr.addstr(8, 0, f"Motor speed: {motor_speed}% ") if motor_speed <= upper_speed_limit else stdscr(8 , 0 , "SPEED LIMMIT REACHED")
                    #stdscr.refresh()
                    time.sleep(0.005)
            
            elif char == ord('s'):
                

                if not key_is_pressed:

                    key_is_pressed = True
                    motor_speed -= 20

                    if motor_speed <= lower_speed_limit:
                        motor_speed = lower_speed_limit
                
                    pwm_1.ChangeDutyCycle(motor_speed)
                    pwm_2.ChangeDutyCycle(motor_speed)

                    stdscr.clear()

                    stdscr.addstr(0, 5, " SLOWING DOWN ")
                    stdscr.addstr(1, 5, " \            ")
                    stdscr.addstr(2, 5, "  \           ")
                    stdscr.addstr(3, 5, "   \          ")
                    stdscr.addstr(4, 5, "    \         ")
                    stdscr.addstr(5, 5, "     \_______ ")

                    stdscr.addstr(8, 0, f"Motor speed: {motor_speed}% ") if motor_speed <= lower_speed_limit else stdscr(8 , 0 , "LOWER SPEED LIMIT REACHED")
                    #stdscr.refresh()
                    time.sleep(0.005)

            else:

                key_is_pressed = False
                #stdscr.referesh()
                """
                GPIO.output(motor1a, GPIO.LOW)
                GPIO.output(motor1b, GPIO.LOW)
                GPIO.output(motor1b, GPIO.LOW)
                GPIO.output(motor2b, GPIO.LOW) 
                """
    finally:

        #Close down curses properly, inc turn echo back on!
        curses.nocbreak()
        stdscr.keypad(False)
        curses.echo()
        curses.endwin()
        GPIO.cleanup()


# Run the curses application
curses.wrapper(main)

"""
def move_forward():

    GPIO.output(motor1a,GPIO.HIGH)
    GPIO.output(motor1b,GPIO.LOW)
    GPIO.output(motor2a,GPIO.HIGH)
    GPIO.output(motor2b,GPLOW)

    pwm_1.ChangeDutyCycle(motor_speed)
    pwm_2.ChangeDutyCycle(motor_speed)

def move_backward():

    pass

def turn_left():

    pass

def turn_right():

    pass

def speed_up():

    pass

def slow_down():
    
    pass

def turn_on_motor():

    pass

def turn_off_motor():

    pass

def turn_camera_left():

    pass

def turn_camera_right():
    
    pass

"""