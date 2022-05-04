"""
run this file to remove the background: 

python remove_background.py

- Change "FILE_PATH" argument to the name of the video which background will be removed (put the video in this folder)
- It will output an mp4 video with no background

"""

import numpy as np
import cv2 as cv
import time as time

#
# ARGUMENTS THAT CAN BE CHANGED BELOW
#

SHOW_FPS_DATA = 0               #if 1: see how long a frame takes to be processed (can slow down the process)
SHOW_PROCESS = 0                #if 1: see the results frame by frame in "live" mode (can slow down the process)
FILE_PATH = "video_cut.mp4"     #path to video to remove background

#output video
OUT_VIDEO_NAME = "out.mp4"      #name
FPS = 30                        #frames per second in new video (10-30? -> see size)

#filter settings
FIRST_ERODE_NUM = 0     #number of times to erode frame (remove solo pixels)
DILATE_NUM = 0          #number of times to dilate frame (make players "fatter")
SECOND_ERODE_NUM = 0    #number of times to erode frame after dilate (remove solo pixels)
kernel = np.ones((3, 3),np.uint8) #erode filter size (if it is bigger, will remove more ungrouped pixels)

#
# REST OF THE CODE
#


#read the first frame from video
cap = cv.VideoCapture(FILE_PATH)
ret, frame = cap.read()
if ret is False:
    print("Cannot read video stream")
    exit()

#create object where new video is written on
fourcc = cv.VideoWriter_fourcc(*'mp4v')
out = cv.VideoWriter(OUT_VIDEO_NAME, fourcc, FPS, (int(frame.shape[1]),int(frame.shape[0])))

#create background subtractor
fgbg = cv.createBackgroundSubtractorMOG2()

start = time.time()
start_frame = time.time()
i = 0
while(1):
    i = i + 1
    ret, frame = cap.read()
    if ret is False:
        break

    fgmask = fgbg.apply(frame) #apply background subtractor

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