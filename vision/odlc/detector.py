"""
Stateful representation of vision system
"""

import json
import redis
import pyexif as exif
import math


r = redis.Redis(host='redis', port=6379, db=0)


def update_targets(targets):
    """
    Update list of targets
    """
    target_json = json.dumps(targets)
    r.set('detector/targets', target_json)


def get_top_detections():
    """
    Returns the top N detections we are most confident in
    """

    # detections = json.loads(r.get('detector/detections'))
    # targets = json.lads(r.get('detector/targets'))

    # TODO: Use matching algarithm on detections and targets and return
    # the best matches
    return []


def process_queued_image(img):
    """
    Main routine for image processing
    """

    detections = json.loads(r.get('detector/detections'))

    # TODO: Get telemetry data from image metadata

    # TODO: Get emergent detectins
    # TODO: Get alphanumric detections

    # TODO: Add these detections to the detections variable

    json_detections = json.dumps(detections)
    r.set('detector/detections', json_detections)

def calculate_object_gps(image, detections):
    image_width = image.size[0]
    image_height = image.size[1]

    image_metadata = exif.ImageMetadata(image)
    image_metadata.read()

    location = [image_metadata.gps_latitude, image_metadata.gps_longitude]
    true_heading = image_metadata.gps_img_direction
    altitude = image_metadata.gps_altitude
    focal_length = image_metadata.focal_length
    sensor_width = image_metadata.sensor_width

    center_pixel_x = image_width / 2
    center_pixel_y = image_height / 2

    GSD = (altitude * sensor_width) / (focal_length * image_width)

    detections_coords = []
    
    for detection in detections:
        x_pos = detection['x_pos']
        y_pos = detection['y_pos']

        delta_x = (x_pos - center_pixel_x) * GSD
        delta_y = (y_pos - center_pixel_y) * GSD

        true_x = delta_x * math.cos(true_heading) - delta_y * math.sin(true_heading)
        true_y = delta_x * math.sin(true_heading) + delta_y * math.cos(true_heading)

        delta_gps_x = true_x / 111111
        delta_gps_y = true_y / 111111

        detections_coords = [location[0] + delta_gps_x, location[1] + delta_gps_y]



        

        


