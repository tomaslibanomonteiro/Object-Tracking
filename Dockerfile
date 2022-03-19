FROM python:3
RUN  mkdir src
RUN  cd  src
WORKDIR  /src
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
ADD main.py .
CMD ["python", "-u", "main.py"]