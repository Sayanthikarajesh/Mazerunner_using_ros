#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Motor driver pins for the two front wheels
IN1 = 17
IN2 = 18
IN3 = 22
IN4 = 23
ENA = 27
ENB = 24

# Set up GPIO pins for the motor driver
GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)

GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)

pwm_a = GPIO.PWM(ENA, 1000)
pwm_b = GPIO.PWM(ENB, 1000) 

def move_wheels(right_wheel_fwd, left_wheel_fwd, right_speed=50, left_speed=50):
    pwm_a.ChangeDutyCycle(right_speed)
    pwm_b.ChangeDutyCycle(left_speed)
    GPIO.output(IN1, right_wheel_fwd)
    GPIO.output(IN2, not right_wheel_fwd)
    GPIO.output(IN3, left_wheel_fwd)
    GPIO.output(IN4, not left_wheel_fwd)

def move_forward(speed):
    move_wheels(True, True, speed, speed)
    print('Moving forward')

def move_backward(speed):
    move_wheels(False, False, speed, speed)
    print('Moving backward')

def turn_right(speed):
    move_wheels(False, True, speed, speed)
    print('Turning right')

def turn_left(speed):
    move_wheels(True, False, speed, speed)
    print('Turning left')

def stop():
    move_wheels(False, False)
    print('Stopped')

def callback(data):
    pub_data = data.data
    sensors_diatances = pub_data.split(' ')
    rospy.loginfo("Received Distance: {}".format(pub_data))

    front_distance = float(sensors_diatances[0])
    right_distance = float(sensors_diatances[1])
    left_distance = float(sensors_diatances[2])
    
    # Algorithm
    if front_distance > 20.0:
        move_forward(50) 
    elif right_distance > 28.0: 
        turn_right(80)
        time.sleep(0.85)
        stop()
    else: 
        turn_left(90)
        time.sleep(1)
        stop()

def motor_subscriber():
    # Initialize ROS node
    rospy.init_node('motor_subscriber', anonymous=True)

    # Create a subscriber with topic name "distances" and message type Float32
    rospy.Subscriber('distances', String, callback)

    # Set the loop rate for the subscriber
    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        rate.sleep()

if __name__ == '__main__':
    try:
        # Start the motor subscriber node
        motor_subscriber()
    except rospy.ROSInterruptException:
        pass