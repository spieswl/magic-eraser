# eecs432_magic-eraser
"Magic Eraser" final project, co-authored by Lauren Hutson and William Spies, MSR 2017-2018 Cohort at Northwestern University 

# Instructions on how to use tiling function
----------------
### Function call : 
processimage (im,framewidth,frameheight,tilesize,overlapwidth)
----------------
### Returns: 
im- processed Frame from the video 
----------------

1) im = the frame gotten from the video
	- the area that you want to be tiled over needs to be of color (255,255,255)
	- the pen and the graphical error at the bottom of the frames should be overlayed with the color 
	(125,0,0) otherwise tile samples with portions of these can be used to fill in the blank area

2) framewidth= the width in pixels of the frame

3) frameheight=the height in the pixels of the frame

4) tilesize= the size of the tile added to the empty space
	- i suggest a size of 100
	-if the size is too large then when tiling happens there is a chance that the tile will exceede
	the frame size
	- if the size is too small then it will take a long time to run
5) overlapwidth= the amount of overlap between the frame and the tile when checking the similarity between the neighboring fames
	- i use an overlap width between 25 and 50

unprocessed image: 

<img src="./unprocessed_image.png" width="640"
      style="margin-left:auto; margin-right:auto; display:block;"/>

processed image:

<img src="./example_frame_processes.png" width="640"
      style="margin-left:auto; margin-right:auto; display:block;"/>

original image:

<img src="./frame.png" width="640"
      style="margin-left:auto; margin-right:auto; display:block;"/>

