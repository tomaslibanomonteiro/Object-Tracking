import unittest
from Object-Tracking.utils import DataFactory
import cv2
import os
import numpy as np
import pandas as pd
import pickle

class TestingDataFactory(unittest.TestCase):

    def test_loadInputVideoFromPath(self):
        
        # read frame after 5 ms of input video
        vid_input = DataFactory.loadInputVideoFromPath('test_vid.mp4')
        vid_input.set(cv2.CAP_PROP_POS_MSEC, 5)
        successFrameRead, frame = vid_input.read()
        
        # check that frame is i read
        self.assertTrue(successFrameRead, 'Frame could not be read')
        
        # write frame as jpg
        cv2.imwrite('testing_frame.jpg', frame)
        
        # read a premade "correct frame"
        correctFrame = cv2.imread('test_frame.jpg')
        
        testing_frame = cv2.imread('testing_frame.jpg')

        # check that the frames are exactly the same 
        self.assertTrue(frame.shape == frame.shape and not(np.bitwise_xor(frame,frame).any()), 'Video not equal to testvideo')
        

        false_vid_input = DataFactory.loadInputVideoFromPath('fake_path')
        self.assertIsNone(false_vid_input)
    
    def test_loadInputCsvFromPath(self):
        
        csv_as_list = DataFactory.loadInputCsvFromPath('test_csv.csv')
        
        correct_csv = pd.read_pickle('test_csv.pkl')

        self.assertTrue(csv_as_list.equals(correct_csv), 'Something wrong with CSV file')


    def test_transformToSimpleCSV(self):
        DataFactory.transformToSimpleCSV('test_csv.csv')
        
        # simple test
        self.assertEqual(os.path.getsize('simple_test_csv.csv'), os.path.getsize('correct_simple_csv.csv'))
        


    def test_videoCaptureToNpArray(self):
        vidcap = cv2.VideoCapture('test_vid.mp4')   
        video, times = DataFactory.videoCaptureToNpArray(vidcap, 10, 10, 10, 100, (200,200))    
        
        correct_vid_file = open('correct_vid.pkl', 'rb')
        correct_times_file = open('correct_times.pkl', 'rb')
        
        correct_vid = pickle.load(correct_vid_file)
        correct_times = pickle.load(correct_times_file)

        correct_vid_file.close()
        correct_times_file.close()

        self.assertTrue(np.array_equal(video, correct_vid))
        self.assertTrue(np.array_equal(times, correct_times))




if __name__ == '__main__':
    unittest.main()


