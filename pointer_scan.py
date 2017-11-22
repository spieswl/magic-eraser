#!/usr/bin/env python

'''
EECS432 - Introduction to Computer Vision
Author: Lauren Hutson & William Spies
Date: November 28th, 2017 (2017/11/28)
Revision 0
'''


import numpy as np
import os
import cv2

from inspect import getsourcefile


def captureVideo(videoFile):

    # Define the working path for the target video file.
    vid_path = os.path.dirname(os.path.abspath(__file__)) + "/" + videoFile
    vid_capture = cv2.VideoCapture(vid_path)

    # DEBUG
    print vid_path
    # END DEBUG

    # Reinitialize frame number to 0 on opening the target video file.
    vid_frameNum = 0

    while vid_capture.isOpened():

        # Read the next frame from the video file
        vid_frameInBuffer, vid_frameImage = vid_capture.read()

        if vid_frameInBuffer == True:

            # Increment frame counter
            vid_frameNum += 1

            # Change video frame to HSV color space
            vid_HSVImage = cv2.cvtColor(vid_frameImage, cv2.COLOR_BGR2HSV)

            # DEBUG
            # Display source image and HSV-Space image in horizontal stack
            imageArray = np.hstack((vid_frameImage, vid_HSVImage))

            cv2.imshow("Images", imageArray)
            # END DEBUG

            # Kill image viewer when reading a "q" keypress
            if cv2.waitKey(0) & 0xFF == ord('q'):
                continue
        else:
            break

    vid_capture.release()

    cv2.destroyAllWindows()

    return