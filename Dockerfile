#FROM python:3.10-slim
FROM dustynv/l4t-pytorch:r36.2.0
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6 gcc -y

RUN python3 -m pip install --upgrade pip
COPY vision/requirements.txt /vision/
RUN pip3 install -r /vision/requirements.txt --ignore-installed blinker

# install ultralytics without torch so we don't override the
# version of pytorch in the base image
COPY vision/ultralytics-reqs.txt /vision/
RUN pip3 install -r /vision/ultralytics-reqs.txt --ignore-installed blinker --no-deps

COPY . /app
WORKDIR /app
CMD ["bash","./vision/start_gunicorn.sh"]
