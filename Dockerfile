FROM ultralytics/ultralytics:8.1.0

RUN apt-get update --allow-releaseinfo-change --fix-missing && \
    DEBIAN_FRONTEND=noninteractive apt-get install ffmpeg libsm6 libxext6 -y
COPY vision/requirements.txt /vision/
RUN pip3 install -r /vision/requirements.txt

COPY . /app
WORKDIR /app
CMD ["bash", "./vision/start_gunicorn.sh"]
