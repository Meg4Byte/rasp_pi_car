import time
import keyboard

duty_cycle_1 = 100
duty_cycle_2 = 40


def slow_down(time_elapsed):

    duty_cycle_limit = 20
    coef = 15           #adjust if needed

    temp_1 = duty_cycle_1  - coef*time_elapsed
    temp_2 = duty_cycle_2  - coef*time_elapsed

    new_duty_cycle_1 = max(temp_1 , duty_cycle_limit)
    new_duty_cycle_2 = max(temp_2 , duty_cycle_limit)

    return new_duty_cycle_1 , new_duty_cycle_2


def pressing(speed):

    if speed == "q":

        start_time = time.time()

        while keyboard.is_pressed('q'):


            time_difference = time.time() - start_time          #measure time interval between key press and release

            #desired_duty_cycle = quadratic_acceleration_profile(time_difference)
            #desired_duty_cycle = min(upper_speed_limit, desired_duty_cycle)
            #current_duty_cycle_1 = min(desired_duty_cycle, 100)
            #current_duty_cycle_2 = min(desired_duty_cycle, 100)
            #pwm_1.ChangeDutyCycle(current_duty_cycle_1)
            #pwm_2.ChangeDutyCycle(current_duty_cycle_2)
            time.sleep(0.01)

            print("q pressed")
            print("time difference : {}".format(time_difference))
    """
    elif speed == "e":
        start_time = time.time()
        while keyboard.is_pressed('e'):
            time_difference = time.time() - start_time
            desired_duty_cycle = linear_slow_down_profile(time_difference)
            desired_duty_cycle = max(lower_speed_limit, desired_duty_cycle)
            current_duty_cycle_1 = min(desired_duty_cycle, 100)
            current_duty_cycle_2 = min(desired_duty_cycle, 100)
            pwm_1.ChangeDutyCycle(current_duty_cycle_1)
            pwm_2.ChangeDutyCycle(current_duty_cycle_2)
            time.sleep(0.01)
    """


if __name__ == "__main__":

    #slow_down(50 , 60 , 3)
    print(slow_down(3))
    pressing("q")