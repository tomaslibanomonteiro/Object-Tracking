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

SHOW_FPS_DATA = 0               #if 1: see how long a frame takes to be processed (can slow down the process)
SHOW_PROCESS = 0                #if 1: see the results frame by frame in "live" mode (can slow down the process)

#output video
OUT_VIDEO_NAME = "no_background.mp4"      #name
FPS = 30                        #frames per second in new video (10-30? -> see size)

#filter settings
FIRST_ERODE_NUM = 1     #number of times to erode frame (remove solo pixels)
DILATE_NUM = 1          #number of times to dilate frame (make players "fatter")
SECOND_ERODE_NUM = 0    #number of times to erode frame after dilate (remove solo pixels)
kernel = np.ones((3, 3),np.uint8) #erode filter size (if it is bigger, will remove more ungrouped pixels)

#
# REST OF THE CODE
#

#Get arguments from terminal 
parser = argparse.ArgumentParser(description='This program shows how to use background subtraction methods provided by \
                                              OpenCV. You can process both videos and images.')
parser.add_argument('--input', type=str, help='Path to a video or a sequence of image.', default='data/videos/20220301-1638-214.mp4')
parser.add_argument('--algo', type=str, help='Background subtraction method (KNN, MOG2).', default='MOG2')

args = parser.parse_args()

#create background subtractor
if args.algo == 'MOG2':
    backSub = cv.createBackgroundSubtractorMOG2()
else:
    backSub = cv.createBackgroundSubtractorKNN()

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

#create object where new video is written on
fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter(OUT_VIDEO_NAME, fourcc, FPS, (int(frame.shape[1]),int(frame.shape[0])))


start = time.time()
start_frame = time.time()
i = 0
while(1):
    i = i + 1
    ret, frame = cap.read()
    if ret is False:
        break

    fgmask = backSub.apply(frame) #apply background subtractor

    #apply erosion, dilation and erosion again (can change with variables in the beggining)
    if FIRST_ERODE_NUM:
        fgmask = cv.erode(fgmask, kernel, iterations = FIRST_ERODE_NUM)
    if DILATE_NUM:
        fgmask = cv.dilate(fgmask, kernel, iterations = DILATE_NUM) 
    if SECOND_ERODE_NUM:
        fgmask = cv.erode(fgmask, kernel, iterations = SECOND_ERODE_NUM)

    #write frame in new video
    fg = cv.copyTo(frame,fgmask)
    out.write(fg)  

    #display process in screen
    if SHOW_PROCESS:
        cv.imshow('fgmask',fgmask)
        cv.imshow('Foreground',fg)
        cv.imshow('Background',cv.copyTo(frame,cv.bitwise_not(fgmask)))
        
        k = cv.waitKey(1) & 0xff
        if k == 27:
            break

    #Show FPS Data
    if SHOW_FPS_DATA:
        end_frame = time.time()
        seconds = end_frame - start_frame
        fps  = round((1 / seconds), 1)
        start_frame = time.time()
        print (format(fps))

end = time.time()
print("time to remove background: ", end-start)
cap.release()
out.release()
cv.destroyAllWindows()