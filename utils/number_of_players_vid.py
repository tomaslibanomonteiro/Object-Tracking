import cv2
import numpy as np
import matplotlib.pyplot as plt
import cvlib as cv
from cvlib.object_detection import draw_bbox
from numpy.lib.polynomial import poly
import random 


## @defgroup group2 Player Counter
#  Several methods to calculate the number ofo players within the images
#  @{


## @brief finds number of players in a frame 
# @param vidcap videofile
# @param milliSec desired frame in milliseconds from start of video 
# @return number of players in frame
def numberOfPlayersInFrame(vidcap, milliSec):
  vidcap.set(cv2.CAP_PROP_POS_MSEC, milliSec)
  success, image = vidcap.read()
  if success:
    box, label, count = cv.detect_common_objects(image, confidence=0.01)
    output = draw_bbox(image, box, label, count)
    plt.imshow(output)
    plt.show()
    
    print('Number of people in frame: ' + str(label.count('person')))

    return label.count('person')


## @brief find number of players in a video
# @param videofile 
# @return number of players in the video
def numberOfPlayersInVideo(vidcap):
  numbers = [0] * 30
  for i in range(30):
    numbers[i] = numberOfPlayersInFrame(vidcap, random.randint(1, 230000))
  numberOfPlayers = max(numbers)
  return numberOfPlayers

## @brief finds number of players in the video 
# @param video path to the videofile
# @return number of players in the video
def mainFunc(video):
    vidcap = cv2.VideoCapture(video)
    return numberOfPlayersInVideo(vidcap)

## @} */ // end of Data Factory
