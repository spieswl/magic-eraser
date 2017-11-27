import numpy as np
import cv2
from PIL import Image
from matplotlib import pyplot as plt
from random import randint


def createpatch (im,tilesize,framewidth,frameheight):
	
	#creates a matrix of the same size as the blacked out area
	img=np.zeros((tilesize,tilesize,3), np.uint8)
	#chooses a random number for the position in which the tile is coming from 
	randompatchheight=randint(0,frameheight-tilesize)
	randompatchwidth=randint(0,framewidth-tilesize)

	check=True
	#will generate the random tile if there are any pixels that are within the banked out box then it will re
	#re generate the patch
	while check==True:

		for i in range(tilesize):
			for j in range(tilesize):
				img[i,j]=im[randompatchwidth+i,randompatchheight+j]

		i4,i5,i6=np.where(img==(255,255,255))
		i9,i8,i7=np.where(img==(0,0,255))

		if len(i4)>0 or len(i7)>0:
			check=True
			randompatchheight=randint(0,frameheight-tilesize)
			randompatchwidth=randint(0,framewidth-tilesize) 
		else:
			check=False
	return img


def createssd (th,im,img,framewidth,frameheight,overlapwidth,tilesize):

	#creating the ssd	
	ar=[]
	ov=[]
	q=0
	q2=0
	
	diffcolory=np.zeros((3))
	diffcolorx=np.zeros((3))

	#will check the ssd of the pixels on the right edge of the space to fill in
	for i in range(framewidth):
		for j in range(frameheight):
			
			if im[i,j][0] == 255 and im[i,j][1] == 255 and im[i,j][2] == 255 :
				
				

				for x in range(i-(i-tilesize)):
				
					for y in range((j+overlapwidth)-j):
						
						
						diffcolory[0]=(im[i-x,j+y][0]-img[x,y])[0]
						diffcolory[1]=(im[i-x,j+y][1]-img[x,y])[1]
						diffcolory[2]=(im[i-x,j+y][2]-img[x,y])[2]
						q+=(diffcolory[0]**2+diffcolory[1]**2+diffcolory[2]**2)**0.5
						
						t= (im[ i-x, j+y]-img[x,y])
					
				
				#will check the ssd of the pixels on the upper edge of the space to fill in

				for x in range((j+overlapwidth)-j):
				
					for y in range(i-(i-tilesize)):
						diffcolorx[0]=(im[i+x,j-y][0]-img[x,y])[0]
						diffcolorx[1]=(im[i+x,j-y][1]-img[x,y])[1]
						diffcolorx[2]=(im[i+x,j-y][2]-img[x,y])[2]

						tr=(im[i-x,j+y]-img[x,y])
						q2+=(diffcolorx[0]**2+diffcolorx[1]**2+diffcolorx[2]**2)**0.5
						
					
				
				#if the ssd is in the appropriate range then the tile will be added

				#choose q and q2 values between 1M to .9M these are the threshholds
				#the lower threashhold will make the prgram run slower because it becomes more selective
				#higher threashhold will make the program run faster because it is less selective

				if q<900000 and q2<900000 :
					tile (im,img,tilesize,i,j)
					
				else:
					#print 0
					img=createpatch (im,tilesize,framewidth,frameheight)
					createssd (th,im,img,framewidth,frameheight,overlapwidth,tilesize)


def tile (im,img,tilesize,i,j):
	
	for x in range(tilesize):
		row=[]
		ovrow=[]
		for y in range(tilesize):
			im[i+x,j+y]=img[x,y]

'''
#im = the frame gotten from the video
	- the area that you want to be tiled over needs to be of color (255,255,255)
	- the pen and the graphical error at the bottom of the frames should be overlayed with the color 
	(0,0,255) otherwise tile samples with portions of these can be used to fill in the blank area

#framewidth= the width in pixels of the frame

#frameheight=the height in the pixels of the frame

#tilesize= the size of the tile added to the empty space
	- i suggest a size of 100
	-if the size is too large then when tiling happens there is a chance that the tile will exceede
	the frame size
	- if the size is too small then it will take a long time to run
#overlapwidth= the amount of overlap between the frame and the tile when checking the similarity between the 
neighboring frames
'''

def processimage (im,framewidth,frameheight,tilesize,overlapwidth):
	img=createpatch (im,tilesize,framewidth,frameheight)
	createssd (0,im,img,framewidth,frameheight,overlapwidth,tilesize)
	return im
	#plt.imshow(im)
	#plt.show()
