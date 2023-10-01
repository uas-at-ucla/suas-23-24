"""
Requests for vision subsystem server
"""

from flask import Flask, Response


app = Flask(__name__)


@app.route('/')
def index():
    """
    Test request
    """
    return 'Hello world!\n'


@app.route('/odlc', methods=['GET'])
def get_best_object_detections():
    """
    Get target detection info
    """
    return []


@app.route('/odlc', methods=['POST'])
def queue_image_for_odlc():
    """
    Queue image POST request
    """
    return Response(status=200)


@app.route('/telemetry', methods=['POST'])
def update_telemetry():
    """
    Update telementry POST request
    """
    return Response(status=200)


@app.route('/targets', methods=['POST'])
def update_targets():
    """
    Update target POST request
    """
    return Response(status=200)
