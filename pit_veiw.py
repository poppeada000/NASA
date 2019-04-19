import cv2
import numpy as np

camera = cv2.VideoCapture(0)



##def make_bad():
##    camera.set(3,640)
##    camera.set(4,480)



def main():
    while True:
        ret, frame = camera.read()

    
        frame1 = cv2.GaussianBlur(frame, (15,15), 40)
        cv2.imshow('window',frame1)
    
        
        if cv2.waitKey(1) == ord('f') :
            kenny()
            
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def kenny():

    while True:
        ret, frame = camera.read()
        
        cv2.imshow('window',frame)
        frameRate = 10
        if cv2.waitKey(1) & 0xFF == ord('p'):
            main()
    
main()
camera.release()
cv2.destroyAllWindows()
