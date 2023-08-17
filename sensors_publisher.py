#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import RPi.GPIO as GPIO
import time
import math

GPIO.setwarnings(False)
# Set GPIO mode
GPIO.setmode(GPIO.BCM)

# Ultrasonic sensor pins
front_sensor_trigger = 16
front_sensor_echo = 20
right_sensor_trigger = 26
right_sensor_echo = 19
left_sensor_trigger = 5
left_sensor_echo = 15

# Set up GPIO pins for the ultrasonic sensor
GPIO.setup(front_sensor_trigger, GPIO.OUT)
GPIO.setup(front_sensor_echo, GPIO.IN)
GPIO.setup(left_sensor_trigger, GPIO.OUT)
GPIO.setup(left_sensor_echo, GPIO.IN)
GPIO.setup(right_sensor_trigger, GPIO.OUT)
GPIO.setup(right_sensor_echo, GPIO.IN)

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
    send_trigger_pulse(trigger_pin)
    pulse_duration = get_pulse_time(echo_pin, 10000)
    distance = pulse_duration * 17150  # Speed of sound: 343 m/s (17150 cm/s)
    return distance

def distance_publisher():
    # Initialize ROS node
    rospy.init_node('distance_publisher', anonymous=True)

    # Create a publisher with topic name "distances" and message type String
    distance_pub = rospy.Publisher('distances', String, queue_size=10)

    # Set the loop rate for the publisher (adjust this based on your requirements)
    rate = rospy.Rate(10)  # 10 Hz

    while not rospy.is_shutdown():
        # Measure distance from the obstacle
        front_distance = get_distance(front_sensor_trigger, front_sensor_echo)
        right_distance = get_distance(right_sensor_trigger, right_sensor_echo)
        left_distance = get_distance(left_sensor_trigger, left_sensor_echo)

        distances_list = [str(front_distance), str(right_distance), str(left_distance)]
        distances = ' '.join(distances_list)

        # Publish the distance data
        distance_pub.publish(distances)

        rate.sleep()

if __name__ == '__main__':
    try:
        # Start the distance publisher node
        distance_publisher()
    except rospy.ROSInterruptException:
        pass