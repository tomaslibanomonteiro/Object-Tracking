import numpy as np
import pandas as pd

# import cv2


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
# @return panda df


class PersonTime:
    def __init__(self, time_id, person_id, x_coord, y_coord):
        self.time_id = time_id
        self.person_id = person_id
        self.x_coord = x_coord
        self.y_coord = y_coord


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


def transformToSimpleCSV(path, fields=['ts in ms', 'mapped id', 'x in m', 'y in m', 'direction of movement in deg'], file_name='simple_2022-03-01_17-38_positions'):
    df = pd.read_csv(path, sep=';', header=0,
                     skipinitialspace=True, usecols=fields)
    useful_columns = fields
    df.loc[:, useful_columns].to_csv('../data/datafiles/new.csv')


def videoCaptureToNpArray(cap, start_frame, num_frames=100, out_fps=1):
    frames = []
    fps = int(cap.get(5))
    ret = True
    frame_number = start_frame
    end_frame = start_frame + num_frames * int(fps/out_fps)

    while ret and frame_number <= end_frame:
        cap.set(cv2.CAP_PROP_FRAME_COUNT, frame_number-1)
        ret, frame = cap.read()  # read one frame from the 'capture' object; img is (H, W, C)
        if ret:
            frames.append(frame)
        frame_number += int(fps/out_fps)
    video = np.stack(frames, axis=0)  # dimensions (T, H, W, C)
    return video


def downsampleInput(df_video, df_csv):
    pass


def decreaseDataframe(df_csv):
    pass


def createSnippet():
    pass


transformToSimpleCSV('../data/datafiles/2022-03-01_17-38_positions.csv')
