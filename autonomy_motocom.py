import cv2
import numpy as np
import sys
import time
import pyzbar.pyzbar as pyzbar
import time
import socket
import pygame

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiveSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

"""Packet Meanings:
        DR = Drive
        ST = Steer(Actuator)
        AU = Auger
        TI = Tilt(Actuators)
        SL = BallScrew Slide
        CO = Conveyor
        """
def stop():
        pygame.joystick.quit()
        pygame.quit()
        print("Clean exit")

pointGreat = (0,0)
pointGreatest = (0,0)

cap = cv2.VideoCapture(1)
cv2.waitKey(1)
hasFrame,frame = cap.read()
vid_writer = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 10, (frame.shape[1],frame.shape[0]))
#Rectified linear unit reduction

# Display barcode and QR code location
def display(im, decodedObjects):
  for decodedObject in decodedObjects:
    points = decodedObject.polygon
    # If the points do not form a quad, find convex hull
    if len(points) > 4 :
      hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
      hull = list(map(tuple, np.squeeze(hull)))
    else :
      hull = points
    # Number of points in the convex hull
    n = len(hull)
    # Draw the convext hull
    pointsTop = saveTop(im, hull, n)
    print(points)
    print("Great:")
    print(pointsTop[1])
    print("Greatest:")
    print(pointsTop[0])
    cv2.line(im, pointsTop[0], (650,500), (0,255,0), 1)
    cv2.line(im, pointsTop[1], (0,0), (0,0,255), 2)  
    currentCenter = center(pointsTop[0], pointsTop[1])
    postion(currentCenter)
    for j in range(0,n):
      cv2.line(im, hull[j], hull[ (j+1) % n], (255,0,0), 3)

def showPos()  :
    t = time.time()
    print("main")
    #Control upadate frequency
    CLOCK = pygame.time.Clock()
    clock_speed = 20

    #vars for if joystick is connected and program is running
    joystick_connect = True
    running = True

    #Create UDP socket connection
    #HOST = '192.168.1.153'
    #HOST = 'localhost'
    HOST = '192.168.1.73'
    PORT = 5005
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiveSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #receiveSocket.bind((HOST, PORT))
    
    #initialize pygame to handle the xbox controller
    #pygame.init()
    #use first joystick connected since only
    #one xbox remote is used
    #joystick = pygame.joystick.Joystick(0)
    #initailize joystick
    #joystick.init()
    #print(joystick.get_name())
    #print("Axes", (joystick.get_numaxes()))
    #print("Balls", joystick.get_numballs())
    #print("Buttons", joystick.get_numbuttons())
    #print("Hats", joystick.get_numhats())
    #if joystick.get_init() == True: print("Initialized properly")
    
    #set initial values of the drive motors to off
    commandLF = 0
    commandRI = 0
    SLPower = 0
    counter = 0
    toggleAU = 2
    toggleCO = 2
    toggleTI = 2
    amps = ['Left Drive:','Right Drive:','Conveyor:','Tilt:','Auger1:','Auger2:','Auger3:','Ballscrew:','Auger1:','Auger2:','Auger3:','Ballscrew:',"Load1:","Load2:"]
    data = ""
    Str = ""
    dataString = ""
    #Bools for motion
    SlR = False
    SlL = False
    ConUp = False
    ConDown = False
    AuForward = False
    AuReverse = False
    tiltDown = False
    tiltUp = False
    #counter for pause message
    PACounter = 1

    while(1):
        hasFrame, inputImage = cap.read() 
        Send(500,s,"LF")
        Send(500,s,"RI")
        if not hasFrame:
            break
        decodedObjects = pyzbar.decode(inputImage)
        display(inputImage, decodedObjects)
        #cv2.line(inputImage, 0, 0, (255,0,0), 3)
        cv2.imshow("Result",inputImage)
        vid_writer.write(inputImage)
        if (cv2.waitKey(1) & 0xFF == ord('p')):
          Send(0,s,"LF")
          Send(0,s,"RI")
          cv2.destroyAllWindows()
          vid_writer.release()
          return

def saveTop(im, points, n ) :
  greatest = 1200
  great = 1200
  for j in range(0,n):
    hull = points[j]
    print(points[j])
    if(hull[1] < greatest) :
      if(greatest < 1200)  :
        pointGreat = pointGreatest
        great = pointGreat[1]
      greatest = hull[1]
      pointGreatest = points[j]

    elif(hull[1] <= great)  :
      great = hull[1]
      pointGreat = points[j]
  return (pointGreatest, pointGreat)

def center(pntGreatest, pntGreater)  :
  center = ((pntGreatest[0] + pntGreater[0])/2)
  return center

def postion(curpoint)   :
    if( (360 >= curpoint) & (curpoint >=  295) )    :
        Send(0,s,"LF")
        Send(0,s,"RI")
        toTheMine()
    elif(curpoint > 360)  :
        Send(0,s,"LF")
        Send(0,s,"RI")
        #time.sleep(.5)
        Send(-500,s,"LF")
        Send(-500,s,"RI")
#    elif(curpoint < 295)    :
#        Send(0,s,"LF")
#        Send(0,s,"RI")
#        #time.sleep(.5)
#        Send(500,s,"LF")
#        Send(500,s,"RI")

def toTheMine() :
    print("Off to the mines")
    time.sleep(1)
    Send(500,s,"LF")
    Send(-500,s,"RI")
    while(1)    :

        if (cv2.waitKey(1) & 0xFF == ord('p')):
            Send(0,s,"LF")
            Send(0,s,"LF")
            time.sleep(2)
            cv2.destroyAllWindows()
            vid_writer.release()
          

def Send(command,s,Str):
    #HOST = '192.168.1.80'
    HOST = '192.168.1.73'
    PORT = 5005
    command = command
    msg = Str + str(command)
    print(msg)
    lastmsg = msg
    send = msg.encode()
    s.sendto(send,(HOST,PORT))

showPos()

