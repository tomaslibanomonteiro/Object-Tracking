import numpy as np
import pandas as pd

import cv2 


## @brief imports mp4 from path for further processing
# @param path to mp4 file
# @return video as cv2VideoCapture - None on error
def loadInputVideoFromPath(path):
    vid_input = cv2.VideoCapture(path)
    if (vid_input.isOpened() == False):
        print("Error opening the video file")
        return None
    else:
        fps = int(vid_input.get(5))
        print("Frame Rate : ",fps,"frames per second") 
        
        frame_count = vid_input.get(7)
        print("Frame count : ", frame_count)
    return vid_input

## @brief import csv from path for further processing
# @param path to csv file
# @param fields to be importet from csv, default:['ts in ms', 'mapped id', 'x in m', 'y in m', 'direction of movement in deg']
# @return panda df 
def loadInputCsvFromPath(path, fields=['ts in ms', 'mapped id', 'x in m', 'y in m', 'direction of movement in deg']):
    df = pd.read_csv(path, sep=';', header=0, skipinitialspace=True, usecols=fields)
    print(df.columns)
    print("Rows in csv count : ", len(df))
    return df

def videoCaptureToNpArray(cap, start_frame, num_frames=100, out_fps=1):
    frames = []
    fps = int(cap.get(5))
    ret = True
    frame_number = start_frame
    end_frame = start_frame + num_frames * int(fps/out_fps)
    
    while ret and frame_number<=end_frame:
        cap.set(cv2.CAP_PROP_FRAME_COUNT, frame_number-1)
        ret, frame = cap.read() # read one frame from the 'capture' object; img is (H, W, C)
        if ret:
            frames.append(frame)
        frame_number += int(fps/out_fps)
    video = np.stack(frames, axis=0) # dimensions (T, H, W, C)
    return video

def downsampleInput(df_video, df_csv):
    pass

def decreaseDataframe(df_csv):
    pass

def createSnippet():
    pass