import RPi.GPIO as GPIO
import time


# Set GPIO mode
GPIO.setmode(GPIO.BCM)
0.3
# Ultrasonic sensor pins
front_sensor_trigger = 16
front_sensor_echo = 20

right_sensor_trigger = 26
right_sensor_echo = 19

left_sensor_trigger = 5
left_sensor_echo = 15

# Motor driver pins
IN1 = 17
IN2 = 18
IN3 = 22
IN4 = 23
ENA = 27
ENB = 24

# Set up GPIO pins
GPIO.setup(front_sensor_trigger, GPIO.OUT)
GPIO.setup(front_sensor_echo, GPIO.IN)
GPIO.setup(left_sensor_trigger, GPIO.OUT)
GPIO.setup(left_sensor_echo, GPIO.IN)
GPIO.setup(right_sensor_trigger, GPIO.OUT)
GPIO.setup(right_sensor_echo, GPIO.IN)

GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)

# Create PWM objects for the enable pins
motor_a_pwm = GPIO.PWM(ENA, 1000)
motor_b_pwm = GPIO.PWM(ENB, 1000)

# Motor control functions
def stop_motors():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def move_forward(speed):
    motor_a_pwm.start(speed)
    motor_b_pwm.start(speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print('fwd')

def move_backward(speed):
    motor_a_pwm.start(speed)
    motor_b_pwm.start(speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

def move_left(speed):
    motor_a_pwm.start(speed)
    motor_b_pwm.start(speed)
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    print('left')

def move_right(speed):
    motor_a_pwm.start(speed)
    motor_b_pwm.start(speed)
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    print('right')
    

# Ultrasonic sensor functions
def send_trigger_pulse(pin):
    GPIO.output(pin, True)
    time.sleep(0.0001)
    GPIO.output(pin, False)

def wait_for_echo(value, pin, timeout):
    count = timeout
    while GPIO.input(pin) != value and count > 0:
        count -= 1

def get_pulse_time(pin, timeout):
    wait_for_echo(True, pin, timeout)
    start_time = time.time()
    wait_for_echo(False, pin, timeout)
    end_time = time.time()
    return end_time - start_time

def get_distance(trigger_pin, echo_pin):
    GPIO.output(trigger_pin, True)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, False)

    pulse_duration = get_pulse_time(echo_pin, 10000)
    distance = pulse_duration * 17150  # Speed of sound: 343 m/s (17150 cm/s)

    return distance

try:
    motor_a_pwm.start(0)
    motor_b_pwm.start(0)
    
    while True:
        front_distance = get_distance(front_sensor_trigger, front_sensor_echo)
        left_distance = get_distance(left_sensor_trigger, left_sensor_echo)
        right_distance = get_distance(right_sensor_trigger, right_sensor_echo)

        print(f"Front: {front_distance:.2f} cm, Left: {left_distance:.2f} cm, Right: {right_distance:.2f} cm")

        # Add a short gap between sensor readings
        time.sleep(0.1)
         
    # while front_dist > max_dist and right_dist > max_dist and left_dist > max_dist:
        
        if front_distance > 20:
            move_forward(50) 
            #collision
        elif right_distance > 28: 
            move_right(80)
            time.sleep(0.85)
            stop_motors()
        else: 
            move_left(90)
            time.sleep(1)
            stop_motors()

 

except KeyboardInterrupt:
    print("Stopping the robot...")
    stop_motors()
    motor_a_pwm.stop()
    motor_b_pwm.stop()
    GPIO.cleanup()

