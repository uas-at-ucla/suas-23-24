"""
Requests for vision subsystem server
"""

from queue import Queue
from threading import Thread

import time
import traceback
import mmap
import io
import numpy as np
import cv2
import os

from flask import Flask, Response, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from prometheus_client import Gauge

import vision.util as util
import vision.odlc.detector as detector

app = Flask(__name__)
image_queue = Queue()

metrics = PrometheusMetrics(app)
images_processed = Counter(
    "vision_images_processed_total", "Total Images Processed")
queue_size = Gauge("vision_queue_size", "Current Images Queued")
active_time = Counter("vision_active_time_seconds", "Active Processing Time")

IMG_FOLDER = "/app/vision/images/odlc"


@app.route("/")
def index():
    return "Hello world!\n"


@app.route("/odlc", methods=["GET"])
def get_best_object_detections():
    """
    Get most certain object detections
    """
    top_detections = detector.get_top_detections()
    json_detections = jsonify(top_detections)

    util.info(f'{top_detections=}')
    return json_detections


@app.route("/odlc", methods=["POST"])
def queue_image_for_odlc():
    """
    Queue image POST request
    """

    # Push updates to image queue
    # If any info is missing, throw an error
    try:
        req = request.json
        assert "img_name" in req, "field 'img_name' is missing"
        assert "altitude" in req, "field 'altitude' is missing"
        assert "latitude" in req, "field 'latitude' is missing"
        assert "longitude" in req, "field 'longitude' is missing"
        assert "heading" in req, "field 'heading' is missing"

        img_name = req.pop("img_name")

        # Try to read from shared memory object
        with open(f"/dev/shm/{img_name}", "r+b") as f:
            # Access file and its data from shared memory using a memory map
            mapped_file = mmap.mmap(f.fileno(), 0)
            data = mapped_file.read()

            # Convert the data into a numpy binary array into a cv2 image
            binary_data = io.BytesIO(data)
            image_array = np.asarray(
                bytearray(binary_data.read()), dtype=np.uint8)
            image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

            # Queue the image then delete the shared memory object
            image_queue.put(
                {"img_name": img_name, "img_data": image, "telemetry": req})
            util.info(f"Image queued: {img_name}")
            os.remove(f"/dev/shm/{img_name}")
            util.info(f"Image removed from shared memory: {img_name}")

    except Exception as exc:
        print(repr(exc))
        return "Badly formed image update", 400

    queue_size.inc()
    return Response(status=200)


@app.route("/targets", methods=["POST"])
def update_targets():
    """
    Update target POST request
    """

    # Push updates to drone targets
    # If any info is missing, throw an error
    try:
        data_list = request.get_json()

        for data in data_list:
            if data["type"] == "emergent":
                assert len(data.keys()) == 1
            elif data["type"] == "alphanumeric":
                assert len(data.keys()) == 2
                data_class = data["class"]
                assert len(data_class) == 4
                assert type(data_class["shape-color"]) is str
                assert type(data_class["text-color"]) is str
                assert type(data_class["text"]) is str
                assert type(data_class["shape"]) is str
            else:
                raise Exception("Type not recognized")

        detector.update_targets(data_list)
    except Exception as exc:
        util.error(repr(exc))
        return 'Badly formed target update', 400

    return Response(status=200)


def process_image_queue(queue):
    while True:
        task = queue.get()
        img_name = task["img_name"]
        img_data = task["img_data"]
        telemetry = task["telemetry"]
        util.info(f"Processing queued image: {img_name}")
        start_time = time.time()

        # Process image
        try:
            detector.process_queued_image(img_data, telemetry)
        except Exception:
            traceback.print_exc()
        # Delete file and return
        queue.task_done()
        util.info("Queued image processed")
        images_processed.inc()
        queue_size.dec()
        active_time.inc(time.time() - start_time)


worker = Thread(target=process_image_queue, args=(image_queue, ))
worker.setDaemon(True)
worker.start()
