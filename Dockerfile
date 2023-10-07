FROM python:3.9-slim
RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

COPY vision/requirements.txt /vision/
RUN pip3 install -r /vision/requirements.txt

COPY . /app
WORKDIR /app
CMD ["./vision/start_gunicorn.sh"]
