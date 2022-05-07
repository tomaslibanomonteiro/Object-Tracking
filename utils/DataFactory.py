import numpy as np
import pandas as pd
import cv2
import os



## @defgroup group1 DataFactory
#  Several methods for reading and processing the input data from
#  a video and its corresponding sensor data output
#  @{

## @brief Imports mp4 from path for further processing
# @param path to mp4 file
# @return video as cv2VideoCapture - None on error
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
# @return input csv as list
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
# @param cap input video capture.
# @param start_frame frame number of cap to start with.
# @param in_fps fps of input cap.
# @param out_fps target fps of array.
# @param num_frames target frame number of array.
# @param rescale rescale dimensio (x,y) if needed.
# @return times, video - times of frames within stack, video stack of np arrays.
def videoCaptureToNpArray(cap, start_frame, in_fps, out_fps, num_frames, rescale):
    frames = []
    frame_times = []
    ret = True
    frame_number = start_frame
    end_frame = start_frame + num_frames * int(in_fps/out_fps)

    while ret and frame_number < end_frame:
        cap.set(cv2.CAP_PROP_FRAME_COUNT, frame_number-1)
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
    return times, video


## @brief Get corresponding data of input times 
# @param df_csv dataframe csv with sensor output.
# @param relevant_times times at which to extract sensor data.
# @return sub_csv subset of input frame only containing relevant times.
def downsampleCSV(df_csv, relvant_times):
    sub_csv = []
    for time in relvant_times:
        df_sensor = getSensordataForFrame(df_csv, time)
        sub_csv.append(df_sensor)
    sub_df = pd.concat(sub_csv, axis=0, ignore_index=True)
    set_ts = set(sub_df['ts in ms'])
    print("Rows in sub df: ", len(sub_df))
    return sub_df


## @brief Get corresponding sensor data of csv for input time
# @param df_csv dataframe csv with sensor output
# @param time time of frame 
# @return sensor_data subset df of sensor data from frame
def getSensordataForFrame(df_csv, time):
    sensor_data = None
    for tolerance in range(-3, 4):
        sensor_data = df_csv[df_csv['ts in ms'] == (tolerance + time)]
        if not sensor_data.empty:
            return sensor_data  
    # Todo throw error
    return sensor_data


## @brief Creates small stack of array from input video 
# @param cap input video capture
# @param start_frame frame number of cap to start with
# @param out_fps target fps of array
# @param num_frames target frame number of array
# @param rescale rescale dimensio (x,y) if needed
# @return cut_csv, cut_cap -  df of only relevant times, video stack of np arrays.
def downsampleInput(cap, df_csv, start_frame, out_fps=1, num_frames=100, rescale=(480, 270)):
    in_fps = int(cap.get(5))
    csv_start_time = df_csv.at[1, 'ts in ms']
    times, cut_cap = videoCaptureToNpArray(
        cap, start_frame, in_fps, out_fps, num_frames, rescale)
    times += csv_start_time
    cut_csv = downsampleCSV(df_csv, times)
    return cut_csv, cut_cap

## @} */ // end of Data Factory

# vcap = loadInputVideoFromPath("./data/20220301-1638-214.mp4")
# print("Read Csv")
# csv = loadInputCsvFromPath("./data/2022-03-07_14-07-22_positions-15.csv")
# print("Done")
# test = downsampleInput(vcap, csv, 0)

