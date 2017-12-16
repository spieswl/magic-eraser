#!/usr/bin/env python

'''
"Magic Eraser" Computer Vision Project - Main function
Author: William Spies
Date: December 16th, 2017 (2017/12/16)
Revision 3
'''

import cv2
import imageTiling
import numpy as np
import os
import sys


def magicEraser(videoFile):

    # Define the working path for the target video file
    vid_path = os.path.dirname(os.path.abspath(__file__)) + "/" + videoFile
    vid_capture = cv2.VideoCapture(vid_path)

    # Read first frame from the video feed and convert to HSV space
    frame_firstImage = vid_capture.read()[1]
    frame_firstHSVImage = cv2.cvtColor(frame_firstImage, cv2.COLOR_BGR2HSV)

    # Define frame height and width boundaries
    frame_height = frame_firstImage.shape[0]  # Nominally 240
    frame_width = frame_firstImage.shape[1]   # Nominally 320

    # Develop mask (and inverse mask) of red text based on first video frame
    mask_Text = developTextMask(frame_firstHSVImage)

    # Pass masked image with occluded areas to imageTiling function
    frame_preTiledImage = tilingMaskSetup(frame_firstImage, mask_Text)
    frame_postTiledImage = imageTiling.process_image(frame_preTiledImage.copy(), frame_height, frame_width, tile_size=22, overlap_width=5)

    # Extract the post-tiled image only in the area defined by the text mask
    frame_TileMask = cv2.bitwise_and(frame_postTiledImage, frame_postTiledImage, mask=mask_Text)

    # ////////////////////  Main image processing loop  ////////////////////
    while vid_capture.isOpened():

        # Read all successive frames from the video feed
        vid_frameInBuffer, frame_baseImage = vid_capture.read()

        if vid_frameInBuffer == True:

            ## Change video frame to HSV color space
            frame_HSVImage = cv2.cvtColor(frame_baseImage, cv2.COLOR_BGR2HSV)

            # Find the "x" coordinate of the marker tip
            # Replace the red text based on marker tip position with the tiled replacement mask
            frame_erasedImage = eraseTextWithMask(frame_baseImage.copy(), frame_HSVImage, mask_Text, frame_TileMask)

            # Display source image, blanked image, and HSV-Space image in horizontal stack
            imageArray = np.hstack((frame_baseImage, frame_erasedImage))
            cv2.imshow("Images", imageArray)
            cv2.waitKey(1)

        else:
            break
    # //////////////////////////////////////////////////////////////////////

    # Close the video feed
    vid_capture.release()

    # Safely terminate any CV2 windows still operating
    cv2.destroyAllWindows()

    return


def developTextMask(frame_HSVImage):

    # Define frame height boundaries
    frame_height = frame_HSVImage.shape[0]  # Nominally 240

    # Initialize kernel for morphological operations
    kernel = np.ones((3,3), np.uint8)

    # HSV boundary ranges for "Red" (NOTE: Slightly different than marker tip boundary values)
    mask_redLowerBound = np.array([0,0,0])
    mask_redUpperBound = np.array([25,255,255])

    # Use OpenCV function to generate red image mask
    mask_base = cv2.inRange(frame_HSVImage, mask_redLowerBound, mask_redUpperBound)

    # Erode and dilate the text mask until general enough to cover the marker text
    mask_eroded = cv2.erode(mask_base, kernel, iterations=1)
    mask_dilated = cv2.dilate(mask_eroded, kernel, iterations=5)

    # Zero out mask values for all row coordinates less than 64 and greater than 220 (isolate the text)
    for x in range(0, 64, 1):
        mask_dilated[x] = np.zeros(mask_dilated[x].shape[0])

    for y in range(220, frame_height, 1):
        mask_dilated[y] = np.zeros(mask_dilated[y].shape[0])

    return mask_dilated


def eraseTextWithMask(frame_BGR, frame_HSV, mask, replacementTexture):

    # Define frame height and width boundaries
    frame_height = frame_BGR.shape[0]  # Nominally 240
    frame_width = frame_BGR.shape[1]   # Nominally 320

    # Initialize important mask variables
    frame_wandXCoord = 0
    kernel = np.ones((3,3), np.uint8)

    # HSV boundary ranges for "Red" (NOTE: Slightly different than original mask boundary values)
    mask_redLowerBound = np.array([0,0,0])
    mask_redUpperBound = np.array([20,255,255])

    # Use OpenCV function to generate red image mask
    frame_redMask = cv2.inRange(frame_HSV, mask_redLowerBound, mask_redUpperBound)

    # Erode and dilate the text mask until general enough to cover the marker text
    frame_erodedMask = cv2.erode(frame_redMask, kernel, iterations=1)
    frame_dilatedMask = cv2.dilate(frame_erodedMask, kernel, iterations=5)

    # Identify the location of the magic wand based on the value of the tip
    # The "break" statements are required to eject from the nested "for" loops when finding the first non-zero value
    for j in range(frame_height):
        for k in range(frame_width):
            if frame_dilatedMask[j][k] == 255:
                frame_wandXCoord = k

            if frame_wandXCoord != 0:
                break
            else:
                continue

        if frame_wandXCoord != 0:
            break
        else:
            continue

    # Set up occlusion masks for important areas to ignore as part of the texture tiling setup
    for m in range(frame_height):
        for n in range(frame_width):

            # Replace all text to the right of the marker tip with the white "screen"
            if n >= frame_wandXCoord and mask[m][n] == 255:
                frame_BGR[m][n] = replacementTexture[m][n]

    return frame_BGR


def tilingMaskSetup(frame_BGR, mask):

    # Define frame height and width boundaries
    frame_height = frame_BGR.shape[0]  # Nominally 240
    frame_width = frame_BGR.shape[1]   # Nominally 320

    # Set up occlusion masks for important areas to ignore as part of the texture tiling setup
    for m in range(frame_height):
        for n in range(frame_width):

            # Obscure the body of the marker
            if 0 <= m <= 60 and (255 <= n <= 295):
                frame_BGR[m][n] = [255, 0, 0]

            # Obscure the heavily scrambled region at the bottom of the video
            if m >= 220:
                frame_BGR[m][n] = [255, 0, 0]

            # Obscure the sides (blank margins) of the image
            if n < 14 or n > 310:
                frame_BGR[m][n] = [255, 0, 0]

            # Replace all masked text with the white "screen"
            if mask[m][n] == 255:
                frame_BGR[m][n] = [255, 255, 255]

    return frame_BGR


################################################################################

def main():

    print "Welcome to the 'Magic' Eraser program!" + "\n"

    while (True):
        # Get path to the video file to be parsed
        if (sys.version_info[0] > 2):
            filePath = input("Please enter the filename (local folder only, please) for the video to be parsed, or type 'quit' to exit: ")
        else:
            filePath = raw_input("Please enter the filename (local folder only, please) for the video to be parsed, or type 'quit' to exit: ")

        # If the file path is "quit", immediately return from the main function; else, continue with parsing the file
        if (filePath == "quit"):
            print "\n" + "Goodbye!"
            return 0
        else:
            magicEraser(filePath)
            print "\n" + "Video modification complete." + "\n"


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print "\n" + "Program terminated by user." + "\n"
        sys.exit(0)
