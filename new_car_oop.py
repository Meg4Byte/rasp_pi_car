import curses
import RPi.GPIO as GPIO
import time

class CarControl:
    def __init__(self):

        # Initialize GPIO and set initial parameters
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)

        self.initialize_pins()
        self.initialize_variables()

    # Define GPIO pins
    def initialize_pins(self):

        
        self.motor1a = 7
        self.motor1b = 11
        self.pwm_pin_2 = 22

        self.motor2a = 13
        self.motor2b = 16
        self.pwm_pin_1 = 15

        #servo pin
        self.servo_pin = 37

        #i2c pins
        self.tof_sensor_pin_1 = 3       
        self.tof_sensor_pin_2 = 5

        #diodes
        self.left_turn_diode = 29
        self.right_turn_diode = 31
        self.slow_down_diode = 33
        self.motor_on_diode = 35


    # Initialize global variables
    def initialize_variables(self):

        self.lower_speed_limit = 35
        self.upper_speed_limit = 100
        self.servo_duty_cycle = 7.5
        self.motor_speed = 35
        self.motor_is_on = False
        self.motor_freq = 2000
        self.servo_freq = 50
        self.key_is_pressed = False


    def setup_gpio(self):

        # Set up GPIO pins
        GPIO.setup(self.left_turn_diode, GPIO.OUT)
        GPIO.setup(self.right_turn_diode, GPIO.OUT)
        GPIO.setup(self.slow_down_diode, GPIO.OUT)
        GPIO.setup(self.motor_on_diode, GPIO.OUT)

        # Set up motor and servo PWM
        GPIO.setup(self.motor1a, GPIO.OUT)
        GPIO.setup(self.motor1b, GPIO.OUT)
        GPIO.setup(self.pwm_pin_1, GPIO.OUT)
        GPIO.setup(self.motor2a, GPIO.OUT)
        GPIO.setup(self.motor2b, GPIO.OUT)
        GPIO.setup(self.pwm_pin_2, GPIO.OUT)
        GPIO.setup(self.servo_pin, GPIO.OUT)

        self.pwm_servo = GPIO.PWM(self.servo_pin, self.servo_freq)
        self.pwm_servo.start(self.servo_duty_cycle)

    def start(self):

        try:
            self.setup_gpio()
            self.run_car_control()

        finally:
            self.cleanup()

    def cleanup(self):

        self.pwm_servo.stop()
        GPIO.cleanup()

    def run_car_control(self):

        screen = curses.initscr()
        curses.noecho()
        curses.cbreak()
        curses.halfdelay(3)
        screen.keypad(True)

        

        try:
            while True:

                char = screen.getch()
                if char == ord('q'):
                    break
                elif char == ord('t') and not self.key_is_pressed:
                    self.start_motor(key_is_pressed)
                elif char == curses.KEY_UP:
                    self.move_forward(screen)
                elif char == curses.KEY_DOWN:
                    self.move_backward(screen)
                elif char == curses.KEY_RIGHT:
                    self.turn_right(screen)
                elif char == curses.KEY_LEFT:
                    self.turn_left(screen)
                elif char == ord('f'):
                    self.turn_camera_right(screen)
                elif char == ord('g'):
                    self.turn_camera_left(screen)
                elif char == ord('w'):
                    self.speed_up(screen)
                elif char == ord('s'):
                    self.speed_down(screen)
                else:
                    self.key_is_pressed = False
        finally:

            curses.nocbreak()
            screen.keypad(False)
            curses.echo()
            curses.endwin()

    #tbd???
    def start_motor(self ):

        #self.motor_is_on = True

        self.key_is_pressed = True

        GPIO.output(self.motor_on_diode, GPIO.HIGH)

        pwm_1 = GPIO.PWM(self.pwm_pin_1, self.motor_freq)
        pwm_2 = GPIO.PWM(self.pwm_pin_2, self.motor_freq)

        pwm_1.start(self.motor_speed)
        pwm_2.start(self.motor_speed)

        time.sleep(0.005)

    def move_forward(self, screen):





        self.clear_screen(screen)
        stdscr.addstr(0, 5, "   /\    ")
        stdscr.addstr(1, 5, "  /  \   ")
        stdscr.addstr(2, 5, " /    \  ")
        stdscr.addstr(3, 5, " FORWARD ")
        stdscr.addstr(4, 5, "         ")
        stdscr.addstr(5, 5, "         ")

        time.sleep(0.005)

    def move_backward(self, screen):
        self.clear_screen(screen)
        # Implement backward movement logic here
        pass

    def turn_right(self, screen):
        self.clear_screen(screen)
        # Implement turn right logic here
        pass

    def turn_left(self, screen):
        self.clear_screen(screen)
        # Implement turn left logic here
        pass

    def turn_camera_right(self, screen):
        self.servo_duty_cycle += 0.5
        if self.servo_duty_cycle >= 12.5:
            self.servo_duty_cycle = 12.5
        self.pwm_servo.ChangeDutyCycle(self.servo_duty_cycle)
        self.clear_screen(screen)
        # Implement camera turn right logic here
        pass

    def turn_camera_left(self, screen):
        self.servo_duty_cycle -= 0.5
        if self.servo_duty_cycle <= 2.5:
            self.servo_duty_cycle = 2.5
        self.pwm_servo.ChangeDutyCycle(self.servo_duty_cycle)
        self.clear_screen(screen)
        # Implement camera turn left logic here
        pass

    def speed_up(self, screen):
        if not key_is_pressed:
            key_is_pressed = True
            self.motor_speed += 20
            if self.motor_speed >= self.upper_speed_limit:
                self.motor_speed = self.upper_speed_limit

            # Implement speed up logic here
            pass

    def speed_down(self, screen):
        if not key_is_pressed:
            key_is_pressed = True
            self.motor_speed -= 20
            if self.motor_speed <= self.lower_speed_limit:
                self.motor_speed = self.lower_speed_limit
            # Implement speed down logic here
            pass

    def clear_screen(self, screen):
        screen.clear()

if __name__ == "__main__":
    car_control = CarControl()
    car_control.start()
