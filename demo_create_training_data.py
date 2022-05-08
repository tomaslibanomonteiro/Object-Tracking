from utils.DataFactory import generateTrainingSamples, loadInputCsvFromPath, loadInputVideoFromPath
import cv2
import numpy as np

def main():
    # Choose the size of output video
    H,W = (200,420)
    
    # Set the framerate of output video
    fps = 25
    
    # Stack size for training data 
    stack_size = 500

    print("Loading csv datafile")
    df = loadInputCsvFromPath("data/2022-03-07_14-07-22_positions-15.csv")
    print("Loading video datafile")
    vcap = loadInputVideoFromPath("data/20220307-1307-214.mp4")
    print("Loading finished!")
    
    
    start_frame = 2000 # Start frame 1775 of sensor data 
    
    print("Generate training stack from video")
    train_data, train_results = generateTrainingSamples(vcap, 
                            df, 
                            start_frame, 
                            out_fps=25, 
                            stack_size=stack_size, 
                            data_size=(W, H))
    
    print("Training stack generated")   
    cv2.destroyAllWindows()


main()