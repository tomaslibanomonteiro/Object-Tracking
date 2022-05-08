from time import time
from utils.DataFactory import TIME_OFFSET_MS, loadInputVideoFromPath, loadInputCsvFromPath, getSensordataForFrame, getPositionsFromSensorData, generateImageFromSensorPositions, videoCaptureToNpArray
import cv2
import numpy as np

def main():

    print("Loading csv datafile")
    df = loadInputCsvFromPath("data/2022-03-07_14-07-22_positions-15.csv")
    print("Loading video datafile")
    vcap = loadInputVideoFromPath("data/20220307-1307-214.mp4")
    print("Loading finished!")
    
    # Time interval for each step, Unit: ms 
    # Because fps is 25,output video will show
    # 25s animation per second.
    time_interval = int(1000/25) #1000 ms == 1 s

    # Choose the size of output video
    H,W = (200,420)
    # Set the framerate of output video
    fps = 25
    # choose codex according to format nedded
    
    print("Downsample")
    start_frame = 2000 # Start frame 1775 of sensor data 
    
    print("Generate training stack from video")
    sub_vcap, times = videoCaptureToNpArray(vcap, 
                                            start_frame, 
                                            in_fps=fps, 
                                            out_fps=fps, 
                                            num_frames=100, 
                                            rescale=(W, H)) 
    
    
    # apply time ofset of sensor data
    csv_start_time = df.at[1, 'ts in ms']
    times += csv_start_time - TIME_OFFSET_MS
    print("Downsample Finished")
    
    start_time_stamp = int(df.iloc[-0]['ts in ms'])
    end_time_stamp = start_time_stamp + 60000
    #end_time_stamp = int(df.iloc[-1]['ts in ms'])
    print("Time stamp from %s to %s" % (str(start_time_stamp),str(end_time_stamp)))
    
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('Visualize_position.avi',fourcc,fps,(W,H),False)
    
    numFrame = 0

    #for i in range(start_time_stamp,end_time_stamp,time_interval):
    for i in times:
        # Get sensor_data from given dataframe and time_stamp
        sensor_data = getSensordataForFrame(df,i)

        # Skip NAN data
        if sensor_data.empty:
            print("sensor_data is empty")
            numFrame +=1
            continue
        if np.isnan(sensor_data.iloc[0]['x in m']) == False:
            
            position = getPositionsFromSensorData(sensor_data, (W,H))
            field = generateImageFromSensorPositions(position, (W,H))
           
            #Masking posittions onto frames
            frame = sub_vcap[numFrame]
            frame[field == 255] = 255
            
            out.write(frame)
            
        numFrame +=1

    out.release()
    cv2.destroyAllWindows()


main()