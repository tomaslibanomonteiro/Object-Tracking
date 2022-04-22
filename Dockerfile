FROM python:3
RUN  mkdir src
RUN  cd  src
WORKDIR  /src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD main.py .
CMD ["python", "-u", "train.py", "--videos", "data/videos/20220301-1638-214.mp4", "--datafiles", "data/datafiles/2022-03-01_17-38_positions.csv"]

# python train.py --videos data/videos/20220301-1638-214.mp4 --datafiles data/datafiles/2022-03-01_17-38_positions.csv