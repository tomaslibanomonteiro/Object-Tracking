"""
run this file to remove the background: 

python background_removal.py --input FILE_PATH_TO_VIDEO --algo ALGORITHM_NAME

FILE_PATH_TO_VIDEO: usually, this is the video that we want to remove background: data/videos/20220307-1307-214.mp4
ALGORITHM_NAME: 'KNN' or 'MOG2'  

- It will output an mp4 video with no background
- To see the options you can change to remove the background in different ways, read the comments on
    "ARGUMENTS THAT CAN BE CHANGED BELOW" section of the code

"""

import numpy as np
import cv2 as cv
import time as time
import argparse

#
# ARGUMENTS THAT CAN BE CHANGED BELOW
#

## Debug Flag: Set to "1" to see how long a frame takes to be processed and results frame by frame in "live" mode (can slow down the process)
DEBUG_INFO = 0     


## Name of output video
OUT_VIDEO_NAME = "foreground.mp4"    
## Frames per second in output video (10-30? -> see size)
FPS = 30
# Filter settings
## Number of times to erode frame (remove solo pixels)
FIRST_ERODE_NUM = 0
## Number of times to dilate frame (make players "fatter")
DILATE_NUM = 0
## Number of times to erode frame after dilate (remove solo pixels)
SECOND_ERODE_NUM = 0
## Erode filter size (if it is bigger, will remove more ungrouped pixels)
kernel = np.ones((3, 3),np.uint8) 

#
# REST OF THE CODE
#

## @brief Get Foreground of the frame given as input to the function
#
# This function takes the frame as input and applys the background subtractor to it.
# After, applys erode, dilation and another erode according to the numbers given as arguments.
# @param frame one frame from the video
# @param backSub background subtraction method (KNN or MOG2)
# @param first_erode number of iterations to erode foreground frame
# @param dilate number of iterations to dilate foreground frame
# @param second_erode number of iterations to erode foreground frame after dilation
# @returns fgmask foreground frame where algorithm was apllied
def GetForeground(frame, backSub, first_erode, dilate, second_erode):
    fgmask = backSub.apply(frame) #apply background subtractor

    #apply erosion, dilation and erosion again (can change with variables in the beggining)
    if first_erode:
        fgmask = cv.erode(fgmask, kernel, iterations = first_erode)
    if dilate:
        fgmask = cv.dilate(fgmask, kernel, iterations = dilate) 
    if second_erode:
        fgmask = cv.erode(fgmask, kernel, iterations = second_erode)
    
    return fgmask

## @brief Capture input video and create output video
#
# @param args get the name of the input video
# @returns cap, out - input video captured and output video object to be written on
def GetIOVideos(args):
    #create object to capture video
    cap = cv.VideoCapture(cv.samples.findFileOrKeep(args.input))
    if not cap.isOpened():
        print('Unable to open: ' + args.input)
        exit(0)

    #read the first frame from video
    ret, frame = cap.read()
    if ret is False:
        print("Cannot read video stream")
        exit()

    #create object where foreground is written on
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    out = cv.VideoWriter(OUT_VIDEO_NAME, fourcc, FPS, (int(frame.shape[1]),int(frame.shape[0])))

    return cap, out

## @brief See how long a frame takes to be processed and results frame by frame in "live" mode (can slow down the process)
#
# 3 windows will appear showing the background, foreground, and the background subtractor results 
#
def DebugInfo(fg, fgmask, frame):
    cv.imshow('fgmask',fgmask)
    cv.imshow('Foreground',fg)
    cv.imshow('Background',cv.copyTo(frame,cv.bitwise_not(fgmask)))
    cv.waitKey(1) 

    end_frame = time.time()
    seconds = end_frame - start_frame
    fps  = round((1 / seconds), 1)
    start_frame = time.time()
    print (format(fps))


## @brief Remove the background of the input video
#
# The output video will be written on the device 
def main():
    #Get arguments from terminal 
    parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by OpenCV. You can process both videos and images.')

    parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='data/videos/20220301-1638-214.mp4')
    parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')

    args = parser.parse_args()

    #create background subtractor
    if args.algo == 'MOG2':
        backSub = cv.createBackgroundSubtractorMOG2()
    else:
        backSub = cv.createBackgroundSubtractorKNN()

    #capture input video and create output video
    cap, out = GetIOVideos(args)

    start = time.time()
    start_frame = time.time()
    i = 0
    while(1):
        i = i + 1
        ret, frame = cap.read()
        if ret is False:
            break
        
        fgmask = GetForeground(frame, backSub, FIRST_ERODE_NUM, DILATE_NUM, SECOND_ERODE_NUM)

        #write foreground frame in new video
        fg = cv.copyTo(frame,fgmask)
        out.write(fg)  

        #display process in screen
        if DEBUG_INFO:
            DebugInfo(fgmask, fg, frame)

    end = time.time()
    print("time to remove background: ", end-start)
    cap.release()
    out.release()
    cv.destroyAllWindows()

main()