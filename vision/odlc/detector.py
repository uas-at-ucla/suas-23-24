"""
Stateful representation of vision system
"""

import math
import json
import redis

from vision.odlc import shape_color_detection

r = redis.Redis(host='redis', port=6379, db=0)


def get_detection_diff(d_1, d_2):
    """
    Determine if two detections are different
    Currently considers detection type and whether the distance between
    coordinates is within our allowed tolerance
    """
    if d_1['type'] != d_2['type']:
        return float('inf')

    # Calculate difference using Haversine formula
    # Difference returned in feet
    la1, lo1 = d_1['coords']
    la2, lo2 = d_2['coords']
    dla = math.radians(abs(la1 - la2))
    dlo = math.radians(abs(lo1 - lo2))

    a = math.sin(dla / 2.0)**2 + math.cos(math.radians(la1)) * \
        math.radians(la2) * math.sin(dlo / 2.0) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1.0 - a))

    return c * 2.093e7


def update_targets(targets):
    """
    Update list of targets
    """
    target_json = json.dumps(targets)
    r.set('detector/targets', target_json)

    # Initialize detections
    detection_json = json.dumps([])
    r.set('detector/detections', detection_json)


def get_top_detections():
    """
    Returns the top N detections we are most confident in
    """

    # detections = json.loads(r.get('detector/detections'))
    # targets = json.loads(r.get('detector/targets'))

    # TODO: Use matching algarithm on detections and targets and return
    # the best matches
    return []


def process_queued_image(img_data, telemetry):
    """
    Main routine for image processing
    """

    detections = json.loads(r.get("detector/detections"))

    # TODO: Get emergent detectins
    # TODO: Get alphanumric detections
    # TODO: If alphanumeric detection found, run odlc

    # TODO: Append these detections to the detections variable
    shape_color_detection.detect_shape_color(img_data)
    json_detections = json.dumps(detections)
    r.set("detector/detections", json_detections)
