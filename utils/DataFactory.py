import numpy as np
import pandas as pd
import cv2
import os
from utils.general import neighbor

TIME_OFFSET_MS = 70500 #ms 1:11min offset

## @defgroup group1 DataFactory
#  Several methods for reading and processing the input data from
#  a video and its corresponding sensor data output
#  @{

## @brief Imports mp4 from path for further processing
# @param path to mp4 file
# @returns video as cv2VideoCapture - None on error
def loadInputVideoFromPath(path):
    vid_input = cv2.VideoCapture(path)
    if (vid_input.isOpened() == False):
        print("Error opening the video file")
        return None
    else:
        fps = int(vid_input.get(5))
        print("Frame Rate : ", fps, "frames per second")

        frame_count = vid_input.get(7)
        print("Frame count : ", frame_count)
    return vid_input


## @brief Imports csv from path for further processing
# @param path to csv file
# @param fields to be importet from csv, default:['ts in ms', 'mapped id', 'x in m', 'y in m', 'direction of movement in deg']
# @returns input csv as list
def loadInputCsvFromPath(path, fields=['ts in ms', 'mapped id', 'x in m', 'y in m', 'direction of movement in deg']):
    df = pd.read_csv(path, 
                     sep=';', 
                     header=0,
                     skipinitialspace=True, 
                     usecols=fields, 
                     engine='c', 
                     quoting=3,
                     on_bad_lines='skip',
                     encoding='utf-8')
    return df


## @brief Converts the original csv to one with the specified collumns
# @param path to csv file
# @param fields to be importet from csv, default:['ts in ms', 'mapped id', 'x in m', 'y in m', 'direction of movement in deg']
def transformToSimpleCSV(path, fields=['ts in ms', 'mapped id', 'x in m', 'y in m', 'direction of movement in deg']):
    useful_columns = fields

    # Reading the entire file will cause out of memory,
    # create chunk to deal with it.

    chunksize = 1000000
    df = pd.DataFrame()
    for chunk in (pd.read_csv(path,
                            sep=';',
                            header=0,
                            skipinitialspace=True, 
                            usecols=fields,
                            engine='c',
                            quoting=3,
                            chunksize=chunksize)):
        df = pd.concat([df, chunk], ignore_index=True)

    file_name = os.path.basename(path) 
    newfile_name = 'simple_' + file_name
    dir_name = os.path.dirname(path)
    path = os.path.join(dir_name, newfile_name)
    print(path)

    df.loc[:, useful_columns].to_csv(path)


## @brief Creates small stack of array from input video
#
# This function takes the video cap as input reads several frames
# downsamples and rescales the frames if applied and converts 
# the frame to grayscale. The output of this function is a stack of np.arrays
# which contnains the read frames as well as the corresponding times beginning
# from the start of the video.
#
# @param cap input video capture.
# @param start_frame frame number of cap to start with.
# @param in_fps fps of input cap.
# @param out_fps target fps of array.
# @param num_frames target frame number of array.
# @param rescale rescale dimensio (x,y) if needed.
# @returns times, video - times of frames within stack, video stack of np arrays.
def videoCaptureToNpArray(cap, start_frame, in_fps, out_fps, num_frames, rescale):
    frames = []
    frame_times = []
    ret = True
    frame_number = start_frame
    end_frame = start_frame + num_frames * int(in_fps/out_fps)

    while ret and frame_number < end_frame:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number-1)
        ret, frame = cap.read()
        # read one frame from the 'capture' object; img is (H, W, C)
        if ret:
            if rescale is not None:
                frame = cv2.resize(frame, rescale)
            
            frame  = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)     
            frames.append(frame)
            # Only even values to avoid time drift
            frame_time = cap.get(cv2.CAP_PROP_POS_MSEC) + \
                (cap.get(cv2.CAP_PROP_POS_MSEC) % 2)
            frame_times.append(frame_time)
        frame_number += int(in_fps/out_fps)
    video = np.stack(frames, axis=0)  # dimensions (T, H, W, C)
    times = np.array(frame_times)
    return video, times


## @brief Get corresponding sensor data of csv for input time
# @param df_csv dataframe csv with sensor output
# @param time time of frame 
# @returns sensor_data subset df of sensor data from frame at time
def getSensordataForFrame(df_csv, time):
    sensor_data = None
    for tolerance in range(-3, 4):
        sensor_data = df_csv[df_csv['ts in ms'] == (tolerance + time)]
        if not sensor_data.empty:
            return sensor_data  
    # Todo throw error
    return sensor_data


## @brief Calculates y and x positions from sensor data
#
# Precision is 0.1 m
# get y,x position for all players from sensor data
# sensor data is from function getSensordataForFrame
#
# @param sensor_data to extract player positions
# @param out_size desired size of output
# @returns list of y and x for all players from sensor data
def getPositionsFromSensorData(sensor_data, out_size):
    W, H = out_size
    position =[]
    for i in range(len(sensor_data)):
        x = sensor_data.iloc[i]['x in m']
        y = sensor_data.iloc[i]['y in m']
        if np.isnan(x) == False and np.isnan(y) == False:
            if x >= 21:
                x=21
            elif x<= -21:
                x=-21

            if y >=10:
                y=10
            elif y<= -10:
                y =-10
            
            x = int((round((x + 21),2) * 10))
            y = int((round((-(y-10)),2) * 10))

            # Aviod x and y out of boundary(index)
            if x == W:
                x -= 1
            if y == H:
                y -= 1
            position.append((y,x))

    return position


## @brief Creates image frame from positions
#
# @param positions list of calculated (y, x) player positions
# @param out_size desired size of output
# @returns frame with player position value 255
def generateImageFromSensorPositions(positions, out_size):
    W,H = out_size
    field = np.zeros((H,W),np.uint8)
    for j in range(len(positions)):

        # For a better visualization, also set neighbors are 255
        index = neighbor(positions[j][0],positions[j][1],H,W)
        for k in index:
            field[k] = 255
            field[positions[j]] = 255
    return field


## @brief Generates stack of frames and corresponding player map for training data
#
# This function takes the video cap as input reads several frames
# downsamples and rescales the frames if applied and converts 
# the frame to grayscale. The output of this function is a stack of np.arrays
# which contnains the read frames as well as the corresponding times beginning
# from the start of the video.
#
# @param cap input video capture.
# @param df dataframe of sensor data
# @param start_frame frame number to start with.
# @param out_fps target fps of stack.
# @param stack_size target size of output stack.
# @param data_size target size of data (W,H).
# @returns train_data, train_result - frame stack of video, frame stack of sensor maps.
def generateTrainingSamples(cap, df, start_frame, out_fps=25, stack_size=500, data_size=(420, 200)):
    fps = int(cap.get(5))
    train_data, times = videoCaptureToNpArray(cap, 
                                            start_frame, 
                                            in_fps=fps, 
                                            out_fps=out_fps, 
                                            num_frames=stack_size, 
                                            rescale=data_size) 
    
    
    # apply time ofset of sensor data
    csv_start_time = df.at[1, 'ts in ms']
    times += csv_start_time - TIME_OFFSET_MS
    
    print("Generate training stack from sensor data")
    fields = []
    for i in times:
        # Get sensor_data from given dataframe and time_stamp
        sensor_data = getSensordataForFrame(df,i)
        
        # Skip NAN data
        assert not sensor_data.empty, f"Frame choosen without corresponding sensor input"
        position = getPositionsFromSensorData(sensor_data, data_size)
        field = generateImageFromSensorPositions(position, data_size)
        fields.append(field)
    train_result = np.stack(fields, axis=0)  # dimensions (T, H, W)       
    
    assert train_data.size == train_result.size, f"Train data size missmatch"
    
    return train_data, train_result

## @} */ // end of Data Factory

# vcap = loadInputVideoFromPath("./data/20220301-1638-214.mp4")
# print("Read Csv")
# csv = loadInputCsvFromPath("./data/2022-03-07_14-07-22_positions-15.csv")
# print("Done")
# test = downsampleInput(vcap, csv, 0)

