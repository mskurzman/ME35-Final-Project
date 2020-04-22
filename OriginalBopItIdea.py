#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile
import math
import ubinascii, ujson, urequests, utime
import random

# Initialize motors and variables
ev3 = EV3Brick()
MayaKey = 'LMw29uQunUQcAT4U-0cEFPQykBHZZwaZF11WHdkI-W'
ChrisKey = 'bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0'

X_Motor = Motor(Port.A)
Y1_Motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
Y2_Motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
Switch = TouchSensor(Port.S4)

#Define Functions
def SL_setup(Key):
     urlBase = "https://api.systemlinkcloud.com/nitag/v2/tags/"
     headers = {"Accept":"application/json","x-ni-api-key":Key} #passwords.NI
     return urlBase, headers

def Put_SL(Tag, Type, Value, Key):
     urlBase, headers = SL_setup(Key)
     urlValue = urlBase + Tag + "/values/current"
     propValue = {"value":{"type":Type,"value":Value}}
     try:
          reply = urequests.put(urlValue,headers=headers,json=propValue).text
     except Exception as e:
          print(e)         
          reply = 'failed'
     return reply

def Get_SL(Tag, Key):
     urlBase, headers = SL_setup(Key)
     urlValue = urlBase + Tag + "/values/current"
     try:
          value = urequests.get(urlValue,headers=headers).text
          data = ujson.loads(value)
          result = data.get("value").get("value")
     except Exception as e:
          print(e)
          result = 'failed'
     return result

def Get_RandomAPI(urlValue):
     #headers = {"Accept":"application/json"}
     try:
          value = urequests.get(urlValue).text
          #data = ujson.loads(value)
          print(value)
          #result = data.get("value")
          #print(result)
     except Exception as e:
          print(e)         
          value = 'failed'
     return value

def Twist(NumTries): # Twist is Yellow
    X_Motor.run_angle(150, -25, stop_type=Stop.BRAKE, wait=True)
    Y1_Motor.run_angle(150, -25, stop_type=Stop.BRAKE, wait=False)
    Y2_Motor.run_angle(150, -25, stop_type=Stop.BRAKE, wait=True)
    NumTries, Command = Reset(NumTries)
    return NumTries, Command

def Pull(NumTries): # Pull is Blue
    X_Motor.run_angle(150, 25, stop_type=Stop.BRAKE, wait=True)
    Y1_Motor.run_angle(150, -25, stop_type=Stop.BRAKE, wait=False)
    Y2_Motor.run_angle(150, -25, stop_type=Stop.BRAKE, wait=True)
    NumTries, Command = Reset(NumTries)
    return NumTries, Command

def Flick(NumTries): # Flick is Green
    X_Motor.run_angle(150, -25, stop_type=Stop.BRAKE, wait=True)
    Y1_Motor.run_angle(150, 25, stop_type=Stop.BRAKE, wait=False)
    Y2_Motor.run_angle(150, 25, stop_type=Stop.BRAKE, wait=True)
    NumTries, Command = Reset(NumTries)
    return NumTries, Command

def Spin(NumTries): # Spin is Red
    X_Motor.run_angle(150, 25, stop_type=Stop.BRAKE, wait=True)
    Y1_Motor.run_angle(150, 25, stop_type=Stop.BRAKE, wait=False)
    Y2_Motor.run_angle(150, 25, stop_type=Stop.BRAKE, wait=True)
    NumTries, Command = Reset(NumTries)
    return NumTries, Command

def Reset(NumTries):
    XAngle = X_Motor.angle()
    Y1Angle = Y1_Motor.angle()
    Y2Angle = Y2_Motor.angle()
    X_Motor.run_angle(-150, XAngle, stop_type=Stop.BRAKE, wait=True)
    Y1_Motor.run_angle(-150, Y1Angle, stop_type=Stop.BRAKE, wait=False)
    Y2_Motor.run_angle(-150, Y2Angle, stop_type=Stop.BRAKE, wait=True)
    NumTries = NumTries - 1
    Command = random.randint(1, 4)
    return NumTries, Command


# Write your program here
ev3.speaker.say('Bop it')

StartCode = Get_SL('Start06', ChrisKey)
NumTries = random.randint(1, 10)
Put_SL('Start06', 'BOOLEAN', 'true', ChrisKey)

while StartCode != 'true':
    StartCode = Get_SL('Start06', ChrisKey)

while StartCode == 'true':
    Command = random.randint(1, 4)
    if Command == 1:
        NumTries, Command = Twist(NumTries)
        urlvalue = 'http://numbersapi.com/1/trivia?fragment'
        Get_RandomAPI(urlValue)

    if Command == 2:
        NumTries, Command = Pull(NumTries)
        urlValue = 'http://numbersapi.com/2/trivia?fragment'
        Get_RandomAPI(urlValue)

    if Command == 3:
        NumTries, Command = Spin(NumTries)
        urlValue = 'http://numbersapi.com/3/trivia?fragment'
        Get_RandomAPI(urlValue)

    if Command == 4:
        NumTries, Command = Flick(NumTries)
        urlValue = 'http://numbersapi.com/4/trivia?fragment'
        Get_RandomAPI(urlValue)

    if NumTries == 0:
        Y1_Motor.run_angle(150, -25, stop_type=Stop.BRAKE, wait=False)
        Y2_Motor.run_angle(150, -25, stop_type=Stop.BRAKE, wait=True)
        Put_SL('Start06', 'BOOLEAN', 'false', ChrisKey)
        StartCode = 'false'
