import math
from PIL import Image
import pyexif as exif

def calculate_object_gps(image_path: str, detections: list) -> list:
    """
    Calculates the GPS coordinates of detected objects in an image.

    Args:
        image_path (str): The path to the input image.
        detections (list): A list of dictionaries containing the x and y positions of the detected objects.

    Returns:
        list: A list of tuples containing the GPS coordinates of the detected objects.
    """

    # Open the image and get its dimensions
    with Image.open(image_path) as image:
        image_width = image.size[0]
        image_height = image.size[1]

    # Get the image metadata
    image_metadata = exif.ImageMetadata(image)
    image_metadata.read()

    # Get the image metadata
    location = [image_metadata.gps_latitude, image_metadata.gps_longitude]
    true_heading = image_metadata.gps_img_direction
    altitude = image_metadata.gps_altitude
    focal_length = image_metadata.focal_length
    sensor_width = image_metadata.sensor_width

    # Calculate the center pixel of the image
    center_pixel_x = image_width / 2
    center_pixel_y = image_height / 2

    # Calculate the ground sample distance
    GSD = (altitude * sensor_width) / (focal_length * image_width)
    
    # Calculate the GPS coordinates of the detected objects
    detections_coords = []
    
    for detection in detections:
        x_pos = detection['x_pos']
        y_pos = detection['y_pos']

        #  Calculate the delta x and y of the detected object in inches
        delta_x = (x_pos - center_pixel_x) * GSD
        delta_y = (y_pos - center_pixel_y) * GSD

        # Calculate the true x and y of the detected object in inches
        true_x = delta_x * math.cos(true_heading) - delta_y * math.sin(true_heading)
        true_y = delta_x * math.sin(true_heading) + delta_y * math.cos(true_heading)

        # Convert the true x and y to GPS coordinates
        delta_gps_x = true_x / 111111
        delta_gps_y = true_y / 111111

        # Add the GPS coordinates to the list of detections
        detections_coords = [(location[0] + delta_gps_x, location[1] + delta_gps_y)]

    # Return the GPS coordinates of the detected objects
    return detections_coords