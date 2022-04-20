## <div align="center">Object Tracking</div>
Find each player's x&y postion in the playground from given videos.
## <div align="center">Quick Start Examples</div>
<details open>
<summary>Install</summary>

Python3 is required with all requirements.txt installed including Pytorch>=1.7:
```bash
$ git clone https://github.com/tomaslibanomonteiro/Object-Tracking.git
$ cd Object-Tracking
```

<div align="center">Install and Run with Docker</div>

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
<div align="center">Install and Run with Conda </div>

To install conda environment run following commands:
```bash
$ conda create -n object-tracking python=3.8
$ conda activate object-tracking
$ conda install pip
$ pip install -r requirements.txt
$ mkdir data/videos/ data/datafiles/ # create data dirs.
```

Put the video files and datafiles into data/videos/ and data/datafiles/ respectively firstly.

Run following example for training:
```bash
$ python train.py --videos data/videos/20220301-1638-214.mp4 --datafiles data/datafiles/2022-03-01_17-38_positions.csv
```

</details>

<details open>
<summary>Interence with train.py</summary>

```bash
$ python train.py --videos data/videos/20220301-1638-214.mp4 --datafiles data/datafiles/2022-03-01_17-38_positions.csv
```


</details>
<details open>
<summary>Datasets</summary>

Click links to download [videos files](https://drive.google.com/file/d/1OrTUqcDlupKqz20r5teMnfLvFnvhVqgP/view?usp=sharing) and [object position csv files](https://drive.google.com/file/d/1onGxXwf2NFWHsZsSpvAMHjWAlqfKKUKJ/view?usp=sharing) from google drive.


</details>