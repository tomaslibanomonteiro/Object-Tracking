# input a series of video and output the background 

from turtle import back, width
import cv2
import os
from skimage.metrics import structural_similarity
import numpy as np
import random
import tqdm

# return block from a 2d-matrix with index
def block(matrix,column_index,row_index,m,n,width,height):
    # get width and height for blocks except the blocks on the boundary
    if width is None or height is None:
        width = matrix.shape[0]
        height = matrix.shape[1]
    width_block = width // n
    height_block = height // m

    row_index_left = row_index
    column_index_top = column_index


    if column_index == n-1 and row_index == m-1:
        block = matrix[row_index:, column_index:]
        row_index_right = -1
        column_index_down = -1
    elif column_index == n-1:
        block = matrix[row_index:(row_index + width_block), column_index:]
        row_index_right = row_index + width_block
        column_index_down = -1
    elif row_index == m-1:
        block = matrix[row_index:, column_index:(column_index + height_block)]  
        row_index_right = -1  
        column_index_down = column_index + height_block
    else: 
        block = matrix[row_index:(row_index + width_block), column_index:(column_index + height_block)]
        row_index_right = row_index + width_block
        column_index_down = column_index + height_block


    return(block, row_index_left, row_index_right, column_index_top,column_index_down)





# return background without persons given the video series
def background_detect(cap):
    # get width, height, fps from videos
    height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    fps = cap.get(cv2.CAP_PROP_FPS)
    height = int(height)
    width = int(width)
    fps = int(fps)
    
    # split image into 20*20. e.g. block0_0 means matrix[0:width//20, 0:height//20 ]
    # split image into 20*20 blocks and find every block's background
    split = [20,20] # blocks_by_rows, blocks_by_cloumns
    m = split[0]
    n = split[1]

    # creat a 10*width*height numpy array filled zeros.
    background = np.zeros([height, width,10],dtype=int)
    repeat_table = np.zeros([m,n,10]) # record the number of repitions high similarity blocks
    status_table = np.zeros([m,n]) 


    count = 0
    while True:
        ret, frame = cap.read()
        if count % (fps*10) == 0:
            if not ret:
                print("Cannot get frame from videos")
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            total_num = 0
            for i in range(m):
                for j in range(n):
                    #print(repeat_table[i][j][:].max())
                    status_table[i,j] = repeat_table[i][j][:].max()
                    total_num += status_table[i,j]
            print(total_num/(m*n*10))

            
            #print(status_table.min())
            if status_table.min() >= 10:
                output_background = np.zeros([height, width],dtype=int)
                for i in range(m):
                    for j in range(n):
                        max_index = np.argmax(repeat_table[i][j][:])
                        #block_background,l,r,t,d = block(background[:][:][max_index],i*n+j,m,n,height,width)
                        output_background[i*(height//m):(i+1)*(height//m), j*(width//n):(j+1)*(width//n)] = background[i*(height//m):(i+1)*(height//m), j*(width//n):(j+1)*(width//n),max_index]
                #display_image(output_background)
                #print(output_background.shape)
                #print(type(output_background))
                cv2.imwrite('background.jpg',output_background)
                print("Get background successfully !!! generate backgound.jpg in the project root dir.")
                exit()

            for i in range(m):
                    for j in range(n):
                        for k in range(10):
                            if repeat_table[i][j][k] >= 10:
                                break
                            block_gray = gray[i*(height//m):(i+1)*(height//m), j*(width//n):(j+1)*(width//n)]
                            block_background= background[i*(height//m):(i+1)*(height//m), j*(width//n):(j+1)*(width//n),k]
                            s = structural_similarity(block_gray,block_background)
                            #print(s)
                            if s >= 0.95:
                                repeat_table[i][j][k] += 1
                                #print(repeat_table[i][j][k])
                                background[i*(height//m):(i+1)*(height//m), j*(width//n):(j+1)*(width//n),k] = block_gray[:][:]
                            else:
                                index = np.argmin(repeat_table[i][j][:])
                                if repeat_table[i][j][:].max() <= 2:
                                    random_num = random.randrange(0, 10, 1)
                                    background[i*(height//m):(i+1)*(height//m), j*(width//n):(j+1)*(width//n),random_num] == block_gray[:,:]
                                    repeat_table[i][j][random_num] = 0
                                background[i*(height//m):(i+1)*(height//m), j*(width//n):(j+1)*(width//n),index] = block_gray[:,:]
        count +=1
    cap.release()
    return(output_background)