import socket
import time
import json
import cv2
import imutils
import numpy

# Define Functions
def createSocket(IP, Port):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind((IP,PORT))
	s.listen(5)
	clientsocket, address = s.accept()
	return clientsocket

def CameraSetup():
	# Open VideoCapture
	cap = cv2.VideoCapture(0)
	# Lower resolution of Video
	ret = cap.set(3, 320)
	ret = cap.set(4, 240)
	return cap

def SetupBlobs():
	params = cv2.SimpleBlobDetector_Params()
	params.minThreshold = 1
	params.maxThreshold = 256
	params.filterByArea = True
	params.minArea = 50
	params.minConvexity = 0.1
	params.minInertiaRatio = 0.1
	detector = cv2.SimpleBlobDetector_create(params)
	return detector

def ImgProcess(cap, detector):
	ret, frame = cap.read()
	frame = imutils.resize(frame, width = 500, inter = cv2.INTER_LINEAR)
	array = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	ThreshArray = cv2.inRange(array, lowerthresh, upperthresh)
	ret, ThreshArray = cv2.threshold(ThreshArray, 200, 255, cv2.THRESH_BINARY_INV)

	keypoints = detector.detect(ThreshArray)
	im_with_keypoints = cv2.drawKeypoints(ThreshArray, keypoints, numpy.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
	cv2.imshow("Keypoints", im_with_keypoints)
	ballLoc = keypoints[-1].pt
	print(ballLoc)
	return ballLoc

def sendSocket(Xref, Yref, currX, currY, clientsocket):
	m = {}
	m['reference'] = [Xref, Yref]
	m['current'] = [currX, currY]
	msg = json.dumps(m)
	msg = msg + '\n'
	clientsocket.send(bytes(msg, 'utf-8'))
#	print('sent dictionary')

# Define Global Variables
# Define IP and Port
IP = "192.168.1.104"
PORT = 1234

# Define Thresholds
lowerthresh = numpy.array([0, 0, 200])
upperthresh = numpy.array([150, 150, 255])

# Define Reference X and Y Coordinates:
Xref = 246
Yref = 172

# Program Starts Here:
cap = CameraSetup()
detector = SetupBlobs()
clientsocket = createSocket(IP, PORT)
print("Socket created")

while cap.isOpened():
	ballLoc = ImgProcess(cap, detector)
	currX = ballLoc[0]
	currY = ballLoc[1]
	sendSocket(Xref, Yref, currX, currY, clientsocket)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
