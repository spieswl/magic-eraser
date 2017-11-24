import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt
from random import randint
'''
cap = cv2.VideoCapture('/home/rikako/Documents/git_directories/classes/Computer Vision/project/Original.avi')

framnum=0
while(cap.isOpened()):
    ret, frame = cap.read()
    if ret==True:
    	framnum+=1
    	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    	if framnum<100:
    		cv2.circle( gray,( 200, 200 ), 32, ( 0, 0, 255 ), -1, 8 )
    	cv2.imshow('frame',gray)
  		#imshow("Image",image);
    	if cv2.waitKey(25) & 0xFF == ord('q'):
       		break
    else:
    	break

cap.release()
cv2.destroyAllWindows()'''



im=cv2.imread('frame.png')
image_size=im.size
#orig=Image.open('moon.bmp').convert('L')

#will put a balack box over the words
#					x      y
cv2.rectangle( im,( 1300, 300 ), (200,600), ( 255, 255, 255 ), -1, 8 )

framewidth=im.shape[0]
frameheight=im.shape[1]
tilesize=100
overlapwidth=50

#finds the coordinates where the black box is 
imgy,i2x,i3= np.where(im==(255,255,255))
#print im.shape[1]
#creates a matrix of the same size as the blacked out area
img = np.zeros((tilesize,tilesize,3), np.uint8)
#chooses a random number for the position in which the tile is coming from 
randompatchheight=randint(0,frameheight-tilesize)
randompatchwidth=  randint(0,framewidth-tilesize) 
check=True

#will generate the random tile if there are any pixels that are within the banked out box then it will re
#re generate the patch
while check==True:

	for i in range(tilesize):
	    for j in range(tilesize):
	        img[i, j] = im[ randompatchwidth+ i, randompatchheight+ j] 

	i4,i5,i6= np.where(img==(255,255,255)) 
	if len(i4) >0:
		check=True
		randompatchheight=randint(0,frameheight-tilesize)
		randompatchwidth=  randint(0,framewidth-tilesize) 
	else:
		check=False

#creating th ssd
th=0
ar=[]
ov=[]
q=0
diffcolor=np.zeros((3))
print framewidth
print frameheight
for i in range(framewidth):
	for j in range(frameheight):
		#ovrow.append(im[ i, j])
		if  im[ i, j][0] == 255 and th==0:
			th=1
			

			for x in range(i-(i-tilesize)):
				row=[]
				ovrow=[]
				for y in range((j+overlapwidth)-j):
					
					t= (im[ i-x, j+y]-img[x,y])
					diffcolor[0]= (im[ i-x, j+y][0]-img[x,y])[0]
					diffcolor[1]= (im[ i-x, j+y][1]-img[x,y])[1]
					diffcolor[2]= (im[ i-x, j+y][2]-img[x,y])[2]
					q+=(diffcolor[0]**2+diffcolor[1]**2+diffcolor[2]**2)**0.5
					print img[x,y],im[ i-x, j+y],t,q

					
					row.append((diffcolor[0]**2,diffcolor[1]**2,diffcolor[2]**2)) 
					ovrow.append(t)
				ar.append(row)
				ov.append(ovrow)
			
			if q<1000000:
				for x in range(tilesize):
					row=[]
					ovrow=[]
					for y in range(tilesize):
						im[ i+x, j+y]=img[x,y]

plt.imshow(im)
#plt.imshow(ov)
plt.show()

plt.imshow(ov) #overlap area
plt.show()

plt.imshow(img) #sample
plt.show()
'''		
print len(ov), len(ov[0])
print len(img), len(img[0])
#plt.imshow(ar)
plt.imshow(ov)
plt.show()
plt.imshow(img)
plt.show()


plt.imshow(ar)
plt.gray()
plt.show()





#cv2.imshow('frame',img)
cv2.imshow('dst_rt', im)
cv2.waitKey(1000)
cv2.destroyAllWindows()
'''

#cv2.imshow('frame',im)