import numpy as np
import pandas as pd

# import cv2


class PersonTime:
    def __init__(self, time_id, person_id, x_coord, y_coord):
        self.time_id = time_id
        self.person_id = person_id
        self.x_coord = x_coord
        self.y_coord = y_coord


# @defgroup group1 DataFactory
 #  Methods of Data Factory
 #  @{

# @brief imports mp4 from path for further processing
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


# @brief import csv from path for further processing
# @param path to csv file
# @param fields to be importet from csv, default:['ts in ms', 'mapped id', 'x in m', 'y in m', 'direction of movement in deg']
# @return input csv as list
def loadInputCsvFromPath(path, fields=['ts in ms', 'mapped id', 'x in m', 'y in m', 'direction of movement in deg']):
    df = pd.read_csv(path, sep=';', header=0,
                     skipinitialspace=True, usecols=fields)
    people_times = []
    for row_idx in df.index:
        person_time = PersonTime(
            df['ts in ms'][row_idx],
            df['mapped id'][row_idx],
            df['x in m'][row_idx],
            df['y in m'][row_idx])
        people_times.append(person_time)

    return people_times


# @brief Converts the original csv to one with the specified collumns
# @param path to csv file
# @param fields to be importet from csv, default:['ts in ms', 'mapped id', 'x in m', 'y in m', 'direction of movement in deg']
def transformToSimpleCSV(path, fields=['ts in ms', 'mapped id', 'x in m', 'y in m', 'direction of movement in deg']):
    useful_columns = fields

    # Reading the entire file will cause out of memory,
    # create chunk to deal with it.
    chunksize = 1000000
    df = pd.DataFrame()
    for chunk in (pd.read_csv(path,sep=';',header=0,skipinitialspace=True, 
                            usecols=fields,engine='python',quoting=3,
                          chunksize=chunksize)):
        df = pd.concat([df, chunk], ignore_index=True)

    # find the index of '/' in the path 
    fraction = []
    for index,element in enumerate(path):
        if element == '/':
            fraction.append(index)
            
    # By separating '/' in the path, we can get dir path and file
    # Drop the '.csv' and get the filename
    filename = path[(fraction[-1]+1):-4] 
    suffix = '_simplified'
    newfile_path = path[:fraction[-1]+1] + filename + suffix + '.csv'
    df.loc[:, useful_columns].to_csv(newfile_path)


# @brief creates small stack of array from input video
# @param cap input video capture
# @param start_frame frame number of cap to start with
# @param in_fps fps of input cap
# @param out_fps target fps of array
# @param num_frames target frame number of array
# @param rescale rescale dimensio (x,y) if needed
# @return times of frames within stack
# @return video stack of np arrays
def videoCaptureToNpArray(cap, start_frame, in_fps, out_fps, num_frames, rescale):
    frames = []
    frame_times = []
    ret = True
    frame_number = start_frame
    end_frame = start_frame + num_frames * int(in_fps/out_fps)

    while ret and frame_number <= end_frame:
        cap.set(cv2.CAP_PROP_FRAME_COUNT, frame_number-1)
        ret, frame = cap.read()  # read one frame from the 'capture' object; img is (H, W, C)
        if rescale is not None:
            frame = cv2.resize(frame, rescale)
        if ret:
            frames.append(frame)
            # Only even values to avoid time drift
            frame_time = cap.get(cv2.CAP_PROP_POS_MSEC) + \
                (cap.get(cv2.CAP_PROP_POS_MSEC) % 2)
            frame_times.append(frame_time)
        frame_number += int(in_fps/out_fps)
    video = np.stack(frames, axis=0)  # dimensions (T, H, W, C)
    times = np.array(frame_times)
    return times, video


# @brief get corresponding data of input times
# @param df_csv dataframe csv with sensor output
# @param relevant_times times
# @return sub_csv subset of input frame only containing relevant times
def downsampleCSV(df_csv, relvant_times):
    # TODO: check problem missmatching times ? -> idea for better solution?
    tolerance_times = np.array([relvant_times + i for i in range(-1, 2)])
    sub_csv = df_csv[df_csv['ts in ms'].isin(tolerance_times)]
    set_ts = set(sub_csv['ts in ms'])
    print("Rows in sub df: ", len(sub_csv))
    return sub_csv


# @brief creates small stack of array from input video
# @param cap input video capture
# @param start_frame frame number of cap to start with
# @param out_fps target fps of array
# @param num_frames target frame number of array
# @param rescale rescale dimensio (x,y) if needed
def downsampleInput(cap, df_csv, start_frame, out_fps=1, num_frames=100, rescale=(480, 270)):
    in_fps = int(cap.get(5))
    csv_start_time = df_csv.at[1, 'ts in ms']
    times, cut_cap = videoCaptureToNpArray(
        cap, start_frame, in_fps, out_fps, num_frames, rescale)
    times += csv_start_time
    cut_csv = downsampleCSV(df_csv, times)

# @} */ // end of group1
