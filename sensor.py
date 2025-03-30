from gpiozero import DistanceSensor
import time

TRIG1 = 4
TRIG2 = 27
ECHO1 = 17
ECHO2 = 24

ultrasonic1 = DistanceSensor(echo=ECHO1, trigger=TRIG1, max_distance = 5)
ultrasonic2 = DistanceSensor(echo=ECHO2, trigger=TRIG2, max_distance = 5)

def get_distance1():
    return ultrasonic1.distance*1000

def get_distance2():
    return ultrasonic1.distance*1000