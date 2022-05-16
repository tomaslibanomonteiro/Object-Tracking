# Object Tracking

Find each player's x&y postion in the playground from given videos.

## Installation and Execution
  
### Clone Repository

Python3 is required with all requirements.txt installed including Pytorch>=1.7:

```bash
$ git clone https://github.com/tomaslibanomonteiro/Object-Tracking.git
$ cd Object-Tracking
```

### Download Datasets

Click links to download [videos files](https://drive.google.com/file/d/1OrTUqcDlupKqz20r5teMnfLvFnvhVqgP/view?usp=sharing) and [object position csv files](https://drive.google.com/file/d/1onGxXwf2NFWHsZsSpvAMHjWAlqfKKUKJ/view?usp=sharing) from google drive.
[Here](https://drive.google.com/file/d/152wThRrr2ujar-yxuPtvFmnr6C8P5Y0V/view?usp=sharing) is the input video already with no background

### Install and Run with Docker

To install Docker run the following commands:

```bash
$ chmod +x install_docker.sh
$ ./install_docker.sh
```

In order to run the project:

```bash
$ chmod +x run.sh # Only one time
$ ./run.sh
```

### Install and Run with Conda

To install conda environment run following commands:

```bash
$ conda create -n object-tracking python=3.8
$ conda activate object-tracking
$ conda install pip
$ pip install -r requirements.txt
$ mkdir data/videos/ data/datafiles/ # create data dirs.
```

Put the video files and datafiles into data/videos/ and data/datafiles/ respectively firstly.


### Generate Training Data

Go to the file "save_image_and_labels.ipynb" to generate training data.

Dataset will be saved in data/dataset/

Copy dataset dir into Pytorch-UNet/dataset/


### Training the Model
Run following example for training:


default device: CPU

```bash
$ python train.py --epochs 1 --batch-size 1
```

## Documentation

The Doxygen documentation can be found in the following link: [Documentation](https://tomaslibanomonteiro.github.io/Object-Tracking/index.html)


## Steps Taken 

In order to accomplish our objectives, the project was divided in the following tasks:

### Background Removal

In order to identify the players, there was a necessity to remove the background, namely the field. This way, we obtain frames which only contain the blobs of players.

In folder "background_removal", run:

```bash
$ python background_removal.py --input FILE_PATH_TO_VIDEO --algo ALGORITHM_NAME
```

**FILE_PATH_TO_VIDEO**: usually, this is the video that we want to remove background: data/videos/20220307-1307-214.mp4
ALGORITHM_NAME: 'KNN' or 'MOG2'

**Output**: video with the foreground of the one given as input

<!-- In the code, you can change some options regarding the background removal process -->


### Sync Frames

The coordinates of the players present on the excel, had an associated time offset with the video. There was a need to correct this offset.
 

### Binary Frame

Since the number of the players present in the video is not always the same, we decided to convert the excel into a binary matrix, containing zeros in the pixels which there are no players, and ones, in case there are.
In order to give some tolerance, the closest four points to the central point of the player were also converted to one.

**Running**:

```bash
$ python visualize_csv_position.py
```

## Future work
### Model Training

Finally, the last step of the project is to train the model.
The Neural Network will receive the video as an input, and output the coordinates of the players. 
In order to train it, the video and the excel will be separated in training and testing data.
The training data will compare the output of the network with the excel containing the real coordinates and learn from it.
The objective is for the network to be able to accurately calculate the coordinates of the testing video.
  

