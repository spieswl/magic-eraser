#!/usr/bin/env python

'''
EECS432 - Introduction to Computer Vision
Author: Lauren Hutson & William Spies
Date: November 28th, 2017 (2017/11/28)
Revision 1
'''

import cv2
import imageTiling
import numpy as np
import os


def magicEraser(videoFile):

    # Define the working path for the target video file
    vid_path = os.path.dirname(os.path.abspath(__file__)) + "/" + videoFile
    vid_capture = cv2.VideoCapture(vid_path)

    # Read all successive frames from the video feed
    vid_frameInBuffer, frame_Image = vid_capture.read()

    # Define frame height and width boundaries
    frame_height = frame_Image.shape[0]
    frame_width = frame_Image.shape[1]

    while vid_capture.isOpened():

        # Read all successive frames from the video feed
        vid_frameInBuffer, frame_origImage = vid_capture.read()

        if vid_frameInBuffer == True:

            ## Change video frame to HSV color space
            frame_HSVImage = cv2.cvtColor(frame_origImage, cv2.COLOR_BGR2HSV)

            # Generate occlusion mask for marker text for each frame of the source video frame
            # Find the "x" coordinate of the marker tip
            frame_blankedImage = eraseTextWithMask(frame_origImage, frame_HSVImage)

            # For the blanked image, call imageTiling in order to fill in the blank spaces
            frame_erasedImage = imageTiling.processimage(frame_blankedImage,  frame_height, frame_width,tilesize=20, overlapwidth=10)

            # DEBUG
            # Display source image, blanked image, and HSV-Space image in horizontal stack
            imageArray = np.hstack((frame_origImage, frame_blankedImage, frame_erasedImage))

            cv2.imshow("Images", imageArray)

            # Kill image viewer when reading a "q" keypress
            if cv2.waitKey(0) & 0xFF == ord('q'):
                continue
            # END DEBUG

        else:
            break

    vid_capture.release()

    cv2.destroyAllWindows()

    return


def eraseTextWithMask(frame_source, frame_HSVImage):

    # Local copy of source image
    frame_Image = frame_source.copy()

    # Define frame height and width boundaries
    frame_height = frame_Image.shape[0]
    frame_width = frame_Image.shape[1]

    # Initialize important mask variables
    frame_wandXCoord = 0
    kernel = np.ones((3,3), np.uint8)

    # HSV boundary ranges for "Red"
    mask_redLowerBound = np.array([0,0,0])
    mask_redUpperBound = np.array([26,255,255])

    # Use OpenCV function to generate red image mask
    frame_redMask = cv2.inRange(frame_HSVImage, mask_redLowerBound, mask_redUpperBound)

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

    # Zero out mask values for all row coordinates less than 64 and greater than 220 (isolate the text)
    for x in range(0, 64, 1):
        frame_dilatedMask[x] = np.zeros(frame_dilatedMask[x].shape[0])

    for y in range(220, frame_height, 1):
        frame_dilatedMask[y] = np.zeros(frame_dilatedMask[y].shape[0])

    # Set up occlusion masks for important areas to ignore as part of the texture tiling setup
    for m in range(frame_height):
        for n in range(frame_width):

            # Obscure the body of the marker
            if 0 <= m <= 60 and (frame_wandXCoord - 10) <= n <= (frame_wandXCoord + 30):
                frame_Image[m][n] = [255, 0, 0]

            # Obscure the heavily scrambled region at the bottom of the video
            if m >= 220:
                frame_Image[m][n] = [255, 0, 0]

            # Replace all text to the right of the marker tip with the white "screen"
            if n >= frame_wandXCoord and frame_dilatedMask[m][n] == 255:
                frame_Image[m][n] = [255, 255, 255]

    return frame_Image
