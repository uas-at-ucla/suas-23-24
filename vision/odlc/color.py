import pandas as pd
import numpy as np
import cv2

def get_shape_text_colors(image_path):
    img = cv2.imread(image_path)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    mask_range1 = cv2.inRange(hsv, (0, 50, 20), (0, 255, 255))
    mask_range2 = cv2.inRange(hsv, (165, 50, 20), (180, 255, 255))
    red_mask = cv2.bitwise_or(mask_range1, mask_range2) #red
    black_mask = cv2.inRange(img, (0, 0, 0), (80, 80, 80)) #black
    white_mask = cv2.inRange(img, (210, 210, 210), (255, 255, 255)) #white
    blue_mask = cv2.inRange(hsv, (100, 80, 20), (120, 255, 255)) #blue
    purple_mask = cv2.inRange(hsv, (125, 70, 20), (165, 255, 255)) #purple
    green_mask = cv2.inRange(hsv, (40, 70, 20), (95, 255, 255)) #green
    orange_mask = cv2.inRange(hsv, (2, 80, 20), (22, 255, 255)) #orange

    ksize = 51  # Kernel size for median filter
    filtered_red_mask = cv2.medianBlur(red_mask, ksize)
    filtered_black_mask = cv2.medianBlur(black_mask, ksize)
    filtered_white_mask = cv2.medianBlur(white_mask, ksize)
    filtered_blue_mask = cv2.medianBlur(blue_mask, ksize)
    filtered_purple_mask = cv2.medianBlur(purple_mask, ksize)
    filtered_green_mask = cv2.medianBlur(green_mask, ksize)
    filtered_orange_mask = cv2.medianBlur(orange_mask, ksize)

    mask_sums = [
        ('Red', np.sum(filtered_red_mask)),
        ('Black', np.sum(filtered_black_mask)),
        ('White', np.sum(filtered_white_mask)),
        ('Blue', np.sum(filtered_blue_mask)),
        ('Purple', np.sum(filtered_purple_mask)),
        ('Green', np.sum(filtered_green_mask)),
        ('Orange', np.sum(filtered_orange_mask))
    ]

    # Sort the list based on sum of masks in descending order
    sorted_mask_sums = sorted(mask_sums, key=lambda x: x[1], reverse=True)

    # Get the shape and text colors
    shape_color = sorted_mask_sums[0][0]
    text_color = sorted_mask_sums[1][0]

    return shape_color, text_color

# Example usage:
#shape_color, text_color = get_shape_text_colors('nimg_6.jpg')
#print(f"Shape color: {shape_color}")
#print(f"Text color: {text_color}")