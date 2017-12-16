#!/usr/bin/env python

'''
"Magic Eraser" Computer Vision Project - Texture synthesis function
Authors: Lauren Hutson & William Spies
Date: December 16th, 2017 (2017/12/16)
Revision 2
'''

import numpy as np
from random import randint


def process_image(sourceImg, frame_width, frame_height, tile_size, overlap_width):
    '''
    Main texture synthesis loop - at the moment, this only samples one area and returns a new image using that
    texture 'tile' over the entire blanked area.
    '''

    # Creates a new textured 'tile'
    tile = create_patch(sourceImg, tile_size, frame_width, frame_height)

    # Checks the ssd values for the sample; if good, replaces the blanked space with the synthesized tile.
    create_ssd(sourceImg, tile, frame_width, frame_height, overlap_width, tile_size)

    return sourceImg


def create_patch(sourceImg, tile_size, frame_width, frame_height):
    '''
    This function creates a random texture from the combination of an input tile_size and an input source_image
    '''

    # Creates a matrix of the same dimensions as the input replacement tile size
    texTile = np.zeros((tile_size, tile_size, 3), np.uint8)

    # Chooses a random location to source the tile from
    rnd_patchheight = randint(0, frame_height-tile_size)
    rnd_patchwidth = randint(0, frame_width-tile_size)

    mCheck = True

    # Generates a random tile at the chosen position
    # If there are any pixels that are within the blanked-out region then it will regenerate the tile
    while (mCheck == True):

        # Copy all the pixels inside the selected area to the replacement tile
        for i in range(tile_size):
            for j in range(tile_size):
                texTile[i,j] = sourceImg[rnd_patchwidth+i,rnd_patchheight+j]

        wCount_B, wCount_G, wCount_R = np.where(texTile == (255, 255, 255))
        bCount_B, bCount_G, bCount_R = np.where(texTile == (255, 0, 0))

        # If any pixel values 'trigger' the detection case below, the entire tile will be regenerated
        if (len(wCount_B) > 0 or len(bCount_B) > 0):
            mCheck = True
            rnd_patchheight = randint(0, frame_height-tile_size)
            rnd_patchwidth = randint(0, frame_width-tile_size)
        else:
            mCheck = False

    return texTile


def create_ssd(sourceImg, texTile, frame_width, frame_height, overlap_width, tile_size):
    '''
    This function compares the ssd values for a number of points along the synthesized texture block
    '''

    # Variable instantiation for ssd calculation
    q1 = 0
    q2 = 0
    diff_colorY = np.zeros((3))
    diff_colorX = np.zeros((3))

    for i in range(frame_width):
        for j in range(frame_height):

            if sourceImg[i,j][0] == 255 and sourceImg[i,j][1] == 255 and sourceImg[i,j][2] == 255:

                # Check the ssd of the pixels on the right edge of the space to fill
                for r in range(i-(i-tile_size)):
                    for s in range((j+overlap_width)-j):
                        diff_colorY[0] = (sourceImg[i-r,j+s][0] - texTile[r,s])[0]
                        diff_colorY[1] = (sourceImg[i-r,j+s][1] - texTile[r,s])[1]
                        diff_colorY[2] = (sourceImg[i-r,j+s][2] - texTile[r,s])[2]

                        q1 += (diff_colorY[0]**2 + diff_colorY[1]* 2 + diff_colorY[2]**2)**0.5

                # Check the ssd of the pixels on the top edge of the space to fill
                for u in range((j+overlap_width)-j):
                    for v in range(i-(i-tile_size)):
                        diff_colorX[0] = (sourceImg[i+u,j-v][0] - texTile[u,v])[0]
                        diff_colorX[1] = (sourceImg[i+u,j-v][1] - texTile[u,v])[1]
                        diff_colorX[2] = (sourceImg[i+u,j-v][2] - texTile[u,v])[2]

                        q2 += (diff_colorX[0]**2 + diff_colorX[1]**2 + diff_colorX[2]**2)**0.5

                # If the ssd is in the appropriate range then the tile will be added

                # Choose q1 and q2 values between 900k to 1M; these values are the lower and upper thresholds
                # The lower threshold will make the program run slower as it becomes more selective
                # The higher threshold will make the program run faster as it is less selective

                if (q1 < 900000 and q2 < 900000):

                    # This copies the textured tile pixel onto the source image
                    for x in range(tile_size):
                        for y in range(tile_size):
                            sourceImg[i+x,j+y] = texTile[x,y]

                else:
                    texTile = create_patch(sourceImg, tile_size, frame_width, frame_height)
                    create_ssd(sourceImg, texTile, frame_width, frame_height, overlap_width, tile_size)

    return