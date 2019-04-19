#Nasa-bot drive code written in pygame using UDP
import time
import socket
import pygame

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


def main():
    print("main")
    #Control upadate frequency
    CLOCK = pygame.time.Clock()
    clock_speed = 20

    #vars for if joystick is connected and program is running
    joystick_connect = True
    running = True

    #Create UDP socket connection
    #HOST = '192.168.1.153'
    HOST = 'localhost'
    #HOST = '192.168.1.73'
    PORT = 5005
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    receiveSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    #receiveSocket.bind((HOST, PORT))
    
    #initialize pygame to handle the xbox controller
    pygame.init()
    #use first joystick connected since only
    #one xbox remote is used
    joystick = pygame.joystick.Joystick(0)
    #initailize joystick
    joystick.init()
    print(joystick.get_name())
    print("Axes", (joystick.get_numaxes()))
    print("Balls", joystick.get_numballs())
    print("Buttons", joystick.get_numbuttons())
    print("Hats", joystick.get_numhats())
    if joystick.get_init() == True: print("Initialized properly")
    
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
    while(running):
        for event in pygame.event.get():
            if event.type == pygame.JOYBUTTONDOWN or event.type == pygame.JOYAXISMOTION:
                Str = ""
                #Left side tank drive
                if (joystick.get_axis(1) > .1 or joystick.get_axis(1) < -.1) and (commandLF != 900 and commandLF != -900):
                    previousCommand = commandLF
                    commandLF = joystick.get_axis(1)*1000
                    commandLF = int(commandLF)
                    if commandLF > 500: 
                        commandLF = 500
                    elif commandLF < -500:
                        commandLF = -500
                    Str="LF"
                    if(previousCommand != commandLF):
                        Send(commandLF,s,Str)
                
                elif joystick.get_axis(1) < .1 and joystick.get_axis(1) > -.1 and commandLF != 0:
                    commandLF = 0
                    Str="LF"
                    Send(commandLF,s,Str)
                    
                #Right side tank drive
                if joystick.get_axis(3) > .1 or joystick.get_axis(3) < -.1 and (commandRI != 900 and commandRI != -900):
                    previousCommand = commandRI
                    commandRI = joystick.get_axis(3)*1000
                    commandRI = int(commandRI)
                    if commandRI > 500: 
                        commandRI = 500
                    elif commandRI < -500:
                        commandRI = -500
                    Str="RI"
                    if(previousCommand != commandRI):
                        Send(commandRI,s,Str)
                elif joystick.get_axis(3) < .1 and joystick.get_axis(3) > -.1 and commandRI != 0:
                    commandRI = 0
                    Str="RI"
                    Send(commandRI,s,Str)
                    

                #Conveyor Belt control using the X button
                #**Note: this will also stop motion when the limit switch is hit
                if joystick.get_button(2) != 0:
                    Str = "CO"
                    ConUp = True
                    Send(750,s,Str)
##                    if(toggleCO %2 != 0):
##                        Send(-999,s,Str)
##                    else:
##                        Send(0,s,Str)
##                    toggleCO=toggleCO+1
                    
                #Conveyor Belt Reverse using the Y button
                if joystick.get_button(3) != 0:
                    Str = "CO"
                    ConDown = True
                    Send(-750,s,Str)
##                    if(toggleCO %2 != 0):
##                        Send(999,s,Str)
##                    else:
##                        Send(0,s,Str)
##                    toggleCO=toggleCO+1

               #Auger control using the A button (Drill direction)
                if joystick.get_button(0) != 0:
                    Str = "AU"
                    Send(-999,s,Str)
                    AuForward = True
##                    if toggleAU % 2 != 0 and toggleAU>0: #odd number
##                        Send(999,s,Str)
##                    else:
##                        Send(0,s,Str)
##                    toggleAU = toggleAU + 1
                                        

                #Auger control using B button (Reverse direction)
                if joystick.get_button(1) != 0:
                    Str = "AU"
                    Send(999,s,Str)
                    AuReverse = True
##                    if toggleAU % 2 != 0: #odd number
##                        Send(-999,s,Str)
##                    else:
##                        Send(0,s,Str)
##                    toggleAU = toggleAU + 1

                #Ballscrew slide using right trigger
                if joystick.get_axis(2) > .1 and SLPower != 700 and SLPower != -700:
                    Str = "SL"
                    SLPower = 450
                    Send(SLPower,s,Str)
                    SlL = True
                elif joystick.get_axis(2) < .1 and SLPower != 0 and SLPower != -700 :
                    SlL = False
                    Str = "SL"
                    SLPower = 0
                    Send(0,s,Str)
                #Ballscrew slide using left trigger
                elif joystick.get_axis(2) < -.1 and SLPower != -700 and SLPower != 700:
                    Str = "SL"
                    SLPower = -450
                    Send(SLPower,s,Str)
                    SlR = True
                elif joystick.get_axis(2) > -.1 and SLPower != 0 and SLPower != 700:
                    Str = "SL"
                    SLPower = 0
                    SlL = False
                    Send(0,s,Str)

                #Tilt using left bumper
                if joystick.get_button(4) != 0:
                    Str = "TI"
                    Send(-600,s,Str)
                    tiltUp = True
##                    if(toggleTI %2 != 0):
##                        Send(-900,s,Str)
##                    else:
##                        Send(0,s,Str)
##                    toggleTI=toggleTI+1

                #Tilt using right bumper
                if joystick.get_button(5) != 0:
                    Str = "TI"
                    Send(600,s,Str)
                    tiltDown = True
##                    if(toggleTI %2 != 0):
##                        Send(900,s,Str)
##                    else:
##                        Send(0,s,Str)
##                    toggleTI=toggleTI+1

                #Send a command to only get data out
                if joystick.get_button(6):
                    Str = "SE"
                    Send(0,s,Str)
                #Filler command for whatever we want it to do
                if joystick.get_button(9):
                    Str = "SC" 
                    Send(0,s,Str)
                #Exit program if start button is pressed
                if joystick.get_button(7):
                    Str="QU"
                    commandRI = 0
                    Send(commandRI,s,Str)
                    print ("Stopping")
                if(Str == "TI" or Str == "AU" or Str == "CO" or (Str == "SL" and SLPower != 0) or Str == "SE"):
                    if s.timeout:
                        continue
                    else:
                        data, HOST = s.recvfrom(30)
                        commaIndex=0
                        num = 0
                        print(data)
                    
            if event.type == pygame.JOYBUTTONUP:
                #Turn off the motors when the button is released. This is a dumb hack I have to do
                #in order to get around the fact that Pygame kinda doesn't specify the button up.
                if joystick.get_button(2)==False and ConUp == True:
                    Str = "CO"
                    Send(0,s,Str)
                    ConUp = False
                if joystick.get_button(3)==False and ConDown == True:
                    Str = "CO"
                    Send(0,s,Str)
                    ConDown = False
                if joystick.get_button(0)==False and AuForward == True:
                    Str = "AU"
                    Send(0,s,Str)
                    AuForward = False
                if joystick.get_button(1)==False and AuReverse == True:
                    Str = "AU"
                    Send(0,s,Str)
                if joystick.get_button(5)==False and tiltDown == True:
                    Str = "TI"
                    Send(0,s,Str)
                    tiltDown = False
                if joystick.get_button(4)==False and tiltUp == True:
                    Str = "TI"
                    Send(0,s,Str)
                    tiltUp = False

    s.close()
    stop()
def Send(command,s,Str):
    #HOST = '192.168.1.80'
    HOST = '192.168.1.73'
    PORT = 5005
    command = command
    msg = Str + str(command)
    print(msg)
    send = msg.encode()
    s.sendto(send,(HOST,PORT))



main()
