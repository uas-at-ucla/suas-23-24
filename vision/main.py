"""
Requests for vision subsystem server
"""

from queue import Queue
from threading import Thread

import os
import time
import redis
import traceback

from flask import Flask, Response, request, jsonify, send_from_directory
from prometheus_flask_exporter import PrometheusMetrics

import odlc.detector as detector


app = Flask(__name__)
metrics = PrometheusMetrics(app)
image_queue = Queue()

FILE_PATH = './images/odlc'

r = redis.Redis(host='redis', port=6379, db=0)


@app.route('/')
@app.route('/index')
def index():
    return send_from_directory('html', 'index.html')


@app.route('/status', methods=['GET'])
def get_status():
    """
    Get queue status

    TOOO: Get processing data
    """
    num_processed = int(r.get('vision/images_processed').decode('utf-8'))

    if num_processed > 0:
        tpi = float(r.get('vision/active_time').
                    decode('utf-8')) / num_processed
    else:
        tpi = 0.0

    status = {
        'processed_images': num_processed,
        'queued_images': image_queue.qsize(),
        'time_per_image': tpi
    }

    return jsonify(status)


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

        # Validate data, this will throw an error if anything is off
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

    # Return empty response for success (check status code for semantics)
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
        r.incr('vision/images_processed')
        r.incrbyfloat('vision/active_time', time.time() - start_time)


worker = Thread(target=process_image_queue, args=(image_queue, ))
worker.setDaemon(True)
worker.start()

r.set('vision/images_processed', 0)
r.set('vision/active_time', 0.0)
