from time import time
from utils.DataFactory import loadInputCsvFromPath,getSensordataForFrame
import cv2
import numpy as np
from utils.general import neighbor

#Precision is 0.1 m
# get y,x position for all players from sensor data
# sensor data is from function getSensordataForFrame
def get_position(sensor_data):
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
            if x == 420:
                x -= 1
            if y == 200:
                y -= 1
            position.append((y,x))

    return position

def main():

    print("Loading csv datafile")
    df = loadInputCsvFromPath("data/datafiles/2022-03-01_17-38_positions.csv")
    print("Loading finished!")

    start_time_stamp = int(df.iloc[-0]['ts in ms'])
    end_time_stamp = int(df.iloc[-1]['ts in ms'])
    print("Time stamp from %s to %s" % (str(start_time_stamp),str(end_time_stamp)))
    
    # Time interval for each step, Unit: ms 
    # Because fps is 25,output video will show
    # 25s animation per second.
    time_interval = int(1000/25) #1000 ms == 1 s

    # Choose the size of output video
    H,W = (200,420)
    # Set the framerate of output video
    fps = 25
    # choose codex according to format nedded
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('Visualize_position.avi',fourcc,fps,(420,200),False)

    for i in range(start_time_stamp,end_time_stamp,time_interval):
        # Get sensor_data from given dataframe and time_stamp
        sensor_data = getSensordataForFrame(df,i)


        # Skip NAN data
        if sensor_data.empty:
            print("sensor_data is empty")
            continue
        if np.isnan(sensor_data.iloc[0]['x in m']) == False:
            position = get_position(sensor_data)
            field = np.zeros((H,W),np.uint8)
            for j in range(len(position)):

                # For a better visualization, also set neighbors are 255
                index = neighbor(position[j][0],position[j][1],H,W)
                for k in index:
                    field[k] = 255
                    field[position[j]] = 255
            out.write(field)


    out.release()
    cv2.destroyAllWindows()


main()