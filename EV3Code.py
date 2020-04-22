#!/usr/bin/env pybricks-micropython

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import (Port, Stop, Direction, Button, Color,
                                 SoundFile, ImageFile, Align)
from pybricks.tools import print, wait, StopWatch
from pybricks.robotics import DriveBase
from pybricks.iodevices import UARTDevice
from pybricks.media.ev3dev import SoundFile, ImageFile
import math
import ubinascii, ujson, urequests, utime
import socket

ev3 = EV3Brick()

MayaKey = 'LMw29uQunUQcAT4U-0cEFPQykBHZZwaZF11WHdkI-W'
ChrisKey = 'bvd8X9LweQY9o2eP1NYL-p8mLL9wMAk6YYOnYSiIo0'
IP = '192.168.1.100'
PORT = 1234

X_Motor = Motor(Port.A, Direction.COUNTERCLOCKWISE)
Y1_Motor = Motor(Port.B, Direction.COUNTERCLOCKWISE)
Y2_Motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
previous_direction = 'Class 4'

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

def SetupSocket(IP, PORT):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((IP, PORT))
	return s

def UnpackSocket(s):
	msg = s.recv(256)
	print(msg)
	msg = msg.decode('utf-8')
	msg = msg.split('\n')[0]
	CoorDict = ujson.loads(msg)
	currentX = CoorDict['current'][0]
	currentY = CoorDict['current'][1]
	return currentX, currentY

def moveMotors(direction, previous_direction):
	if direction != previous_direction:
		if direction == "Class 1":
			X_Motor.run_angle(200, 35, wait = True, stop_type = Stop.BRAKE)
		if direction == "Class 2":
			X_Motor.run_angle(-200, 35, wait = True, stop_type = Stop.BRAKE)
		if direction == "Class 3":
			Y1_Motor.run_angle(200, 35, wait = False, stop_type = Stop.BRAKE)
			Y2_Motor.run_angle(200, 35, wait = True, stop_type = Stop.BRAKE)
		if direction == "Class 4":
			Y1_Motor.run_angle(-200, 35, wait = False, stop_type = Stop.BRAKE)
			Y2_Motor.run_angle(-200, 35, wait = True, stop_type = Stop.BRAKE)
	previous_direction = direction
	return previous_direction,

#Put_SL('Start06', 'BOOLEAN', 'true', ChrisKey)
# Write your program here
ev3.speaker.say('Start')

StartCode = Get_SL('Start06', ChrisKey)

while StartCode != 'true':
    StartCode = Get_SL('Start06', ChrisKey)

s = SetupSocket(IP, PORT)
while StartCode == 'true': 
	direction = Get_SL('PoseNetKeypoints', MayaKey)
	direction = ujson.loads(direction)
	print(direction)
	previous_direction = moveMotors(direction, previous_direction)
	currentX, currentY = UnpackSocket(s)
	print(currentX, currentY)
	if (currentX < 195 and currentY < 70):
		Put_SL('Start07', 'BOOLEAN', 'true', ChrisKey)
		StartCode = 'false'

ev3.speaker.say('done')
