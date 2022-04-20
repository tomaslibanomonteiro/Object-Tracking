
# Object-Tracking by Agile Network Development Team C.
"""
Run inference on videos and csv datafiles.

Usage:
    $ python path/to/train.py --videos path/to/video.mp4 --datafiles path/to/datafile.csv --weights weights.pt --imgsz 1920
"""

import argparse
from utils.DataFactory import loadInputVideoFromPath, loadInputCsvFromPath, videoCaptureToNpArray, \
    downsampleInput, decreaseDataframe, createSnippet
from utils.background_detect import background_detect
from utils.general import print_args
from pathlib import Path
import sys


FILE = Path(__file__).resolve()
ROOT = FILE.parents[0]  # Project root directory
if str(ROOT) not in sys.path:
    sys.path.append(str(ROOT))  # add ROOT to PATH



def run(
        weights='object-tracking.pt',  # model.pt path(s)
        background = None, # background image from videos 
        videos='data/videos',  # file/dir/URL/glob, 0 for webcam
        datafiles='data/datafiles',  # file/dir/URL/glob, 0 for webcam
        imgsz=1920,  # inference size (pixels)
        device='',  # cuda device, i.e. 0 or 0,1,2,3 or cpu
        project='runs/detect',  # save results to project/name
        name='exp',  # save results to project/name
        ):

    cap = loadInputVideoFromPath(videos)
    datafile = loadInputCsvFromPath(datafiles)
    if background is None:
        background = background_detect(cap) # return a background image from videos
    """
    # Remove Background
    frame_without_background = background_remove(background, frame)
    You can use this function, this and this


    You have the image
    It tries to calculate the corrdinates
    We compare to the real coordinates
    And then it tries again



    # Transform from 3D to 2D (Optional)
    #  
    pass

    
    """

def parse_opt():
    parser = argparse.ArgumentParser()
    parser.add_argument('--weights', nargs='+', type=str, default='object-tracking.pt', help='model path(s)')
    parser.add_argument('--background', nargs='+', type=str, default=None, help='background image from videos')
    parser.add_argument('--videos', type=str, default='data/videos.mp4', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--datafiles', type=str, default='data/datafiles', help='file/dir/URL/glob, 0 for webcam')
    parser.add_argument('--imgsz', '--img', '--img-size', nargs='+', type=int, default=[1920], help='inference size h,w')
    parser.add_argument('--project', default='runs/detect', help='save results to project/name')
    parser.add_argument('--name', default='exp', help='save results to project/name')
    opt = parser.parse_args()
    opt.imgsz *= 2 if len(opt.imgsz) == 1 else 1  # expand
    print_args(FILE.stem, opt)
    return opt


def main(opt):
    #check_requirements(exclude=('tensorboard', 'thop'))
    run(**vars(opt))


if __name__ == "__main__":
    opt = parse_opt()
    main(opt)