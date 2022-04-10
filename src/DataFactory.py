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

def downsampleInput(df_video, df_csv):
    pass

def decreaseDataframe(df_csv):
    pass


