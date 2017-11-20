import numpy as np
import cv2

cap = cv2.VideoCapture('/home/rikako/Documents/git_directories/classes/Computer Vision/project/Original.avi')

framnum=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
    	framnum+=1
    	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    	if framnum<100:
    		cv2.circle( gray,( 200, 200 ), 32, ( 0, 0, 255 ), 1, 8 )
    	cv2.imshow('frame',gray)
  		#imshow("Image",image);
    	if cv2.waitKey(25) & 0xFF == ord('q'):
       		break
    else:
    	break

cap.release()
cv2.destroyAllWindows()