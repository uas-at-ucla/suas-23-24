"""
Requests for vision subsystem server
"""

from queue import Queue
from threading import Thread

import os
import time
import traceback

from flask import Flask, Response, request, jsonify
from prometheus_flask_exporter import PrometheusMetrics
from prometheus_client import Counter
from prometheus_client import Gauge

import odlc.detector as detector

app = Flask(__name__)
image_queue = Queue()

metrics = PrometheusMetrics(app)
images_processed = Counter('vision_images_processed_total',
                           'Total Images Processed')
queue_size = Gauge('vision_queue_size', 'Current Images Queued')
active_time = Counter('vision_active_time_seconds', 'Active Processing Time')

FILE_PATH = './images/odlc'


@app.route('/')
def index():
    return 'Hello world!\n'


@app.route('/odlc', methods=['GET'])
def get_best_object_detections():
    """
    Get most certain object detections
    """
    top_detections = detector.get_top_detections()
    json_detections = jsonify(top_detections)
    print(top_detections)
    return json_detections


@app.route('/odlc', methods=['POST'])
def queue_image_for_odlc():
    """
    Queue image POST request

    Get image path from request and queue it.
    TODO: Also extract telemetry data either here,
    once it is popped from the queue, or in detector.py.
    """
    img_path = request.get_data()
    image_queue.put({"img_path": img_path})
    queue_size.inc()
    return Response(status=200)


@app.route('/targets', methods=['POST'])
def update_targets():
    """
    Update target POST request
    """

    # Push updates to drone targets
    # If any info is missing, throw an error
    try:
        data_list = request.get_json()

        for data in data_list:
            if data['type'] == 'emergent':
                assert len(data.keys()) == 1
            elif data['type'] == 'alphanumeric':
                assert len(data.keys()) == 2
                data_class = data['class']
                assert len(data_class) == 4
                assert type(data_class['shape-color']) is str
                assert type(data_class['text-color']) is str
                assert type(data_class['text']) is str
                assert type(data_class['shape']) is str
            else:
                raise Exception('Type not recognized')

        detector.update_targets(data_list)
    except Exception as exc:
        print(repr(exc))
        return 'Badly formed target update', 400

    return Response(status=200)


def process_image_queue(queue):
    while True:
        task = queue.get()
        img_path = task['img_path']
        print('Processing queued image')
        start_time = time.time()

        # Process image
        try:
            detector.process_queued_image(img_path)
        except Exception:
            traceback.print_exc()

        # Delete file and return
        os.remove(img_path)
        queue.task_done()
        print('Queued image processed')
        images_processed.inc()
        queue_size.dec()
        active_time.inc(time.time() - start_time)


@app.route('/process', methods=['POST'])
def simulate_process_img():
    images_processed.inc()
    queue_size.dec()
    active_time.inc(2)
    return Response(status=200)


worker = Thread(target=process_image_queue, args=(image_queue, ))
worker.setDaemon(True)
worker.start()
