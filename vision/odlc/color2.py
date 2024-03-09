import pandas as pd
import numpy as np
import cv2

def get_shape_text_colors(image_path):
    image = cv2.imread(image_path)
    filtered_image = cv2.medianBlur(image, ksize=11)

    hsv_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2HSV)
    #Apply blur to v channel of image
    v_channel = hsv_image[:, :, 2]
    v_blurred = cv2.GaussianBlur(v_channel, (3, 3), 0)

    # Perform edge detection using Sobel
    sobel_x = cv2.Sobel(v_blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(v_blurred, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    # Threshold the gradient magnitude to obtain edges
    edge_threshold = 20
    edges = np.uint8(gradient_magnitude > edge_threshold)

    #Find the largest contour and make all the pixels in the background pure gray
    normalized_gradient = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
    _, binary_image = cv2.threshold(normalized_gradient, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    contour_image = np.zeros_like(binary_image)
    cv2.drawContours(contour_image, [largest_contour], -1, 255, thickness=cv2.FILLED)

    kernel = np.ones((9, 9), np.uint8)
    eroded_mask = cv2.erode(contour_image, kernel, iterations=1)
    eroded_mask = eroded_mask.astype(np.uint8)
    result_image = cv2.bitwise_and(contour_image, contour_image, mask=eroded_mask)

    final_image = cv2.bitwise_and(image, image, mask=result_image)
    final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
    gray_color = [128, 128, 128]
    black_mask = np.all(final_image == [0, 0, 0], axis=-1)
    final_image[black_mask] = gray_color

    #Check if the edge detection actually found a shape, try edge detection on saturation otherwise
    non_gray_count = np.sum(np.any(final_image != gray_color, axis=-1) > 0)
    percent = non_gray_count/image.shape[0]/image.shape[1]

    if percent < 0.08:
        hsv_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2HSV)

        v_channel = hsv_image[:, :, 1]

        v_blurred = cv2.GaussianBlur(v_channel, (3, 3), 0)

        sobel_x = cv2.Sobel(v_blurred, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(v_blurred, cv2.CV_64F, 0, 1, ksize=3)

        # Compute the magnitude of gradients
        gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)

        # Threshold the gradient magnitude to obtain edges
        edge_threshold = 20
        edges = np.uint8(gradient_magnitude > edge_threshold)
        normalized_gradient = cv2.normalize(edges, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8UC1)
        _, binary_image = cv2.threshold(normalized_gradient, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)
        contour_image = np.zeros_like(binary_image)
        cv2.drawContours(contour_image, [largest_contour], -1, 255, thickness=cv2.FILLED)

        kernel = np.ones((9, 9), np.uint8) 
        eroded_mask = cv2.erode(contour_image, kernel, iterations=1)
        eroded_mask = eroded_mask.astype(np.uint8)
        result_image = cv2.bitwise_and(contour_image, contour_image, mask=eroded_mask)

        final_image = cv2.bitwise_and(image, image, mask=result_image)
        final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
        gray_color = [128, 128, 128]
        black_mask = np.all(final_image == [0, 0, 0], axis=-1)
        final_image[black_mask] = gray_color
        non_gray_count = np.sum(np.any(final_image != gray_color, axis=-1) > 0)
        percent = non_gray_count/image.shape[0]/image.shape[1]

    sum_rgb = np.sum(final_image, axis=-1)

    #Remove white, black, and brown pixels from the image first
    white_threshold = 600
    black_threshold = 400
    range_rgb = np.max(final_image, axis=-1) - np.min(final_image, axis=-1)
    color_range_threshold = 0.5

    hsv = cv2.cvtColor(final_image, cv2.COLOR_RGB2HSV)
    brown_mask = (cv2.inRange(hsv, (0, 10, 0), (180, 70, 160)) > 0)
    brown_mask = (cv2.inRange(final_image, (145, 115, 130), (175, 135, 150)) > 0) | (cv2.inRange(final_image, (115, 180, 145), (130, 190, 170)) > 0)

    # Create masks for white and black pixels based on the thresholds
    white_mask = sum_rgb > white_threshold
    black_mask = (sum_rgb < black_threshold) & (range_rgb <= (color_range_threshold * np.max(final_image, axis=-1))) * (sum_rgb != 384)

    # Apply the masks to the original image to visualize
    white_result = np.zeros_like(final_image)
    white_result[white_mask] = final_image[white_mask]

    black_result = np.zeros_like(final_image)
    black_result[black_mask] = final_image[black_mask]

    brown_result = np.zeros_like(final_image)
    brown_result[brown_mask] = final_image[brown_mask]

    white_count = np.sum(white_mask > 0)
    white_percent = white_count / non_gray_count

    black_count = np.sum(black_mask > 0)
    black_percent = black_count / non_gray_count

    brown_count = np.sum(brown_mask > 0)
    brown_percent = brown_count / non_gray_count

    if white_percent > 0.1:
        final_image[white_mask] = gray_color
    if black_percent > 0.1:
        final_image[black_mask] = gray_color
    if brown_percent > 0.1:
        final_image[brown_mask] = gray_color

    #Apply masks for various colors that are not white, black, or brown
    hsv = cv2.cvtColor(final_image, cv2.COLOR_RGB2HSV)
    red_mask = cv2.inRange(hsv, (165, 10, 0), (180, 255, 255)) #red
    blue_mask = cv2.inRange(hsv, (100, 1, 0), (125, 255, 255)) #blue
    purple_mask = cv2.inRange(hsv, (125, 10, 0), (165, 255, 255)) #purple
    green_mask = cv2.inRange(hsv, (50, 10, 0), (100, 255, 255)) #green
    yellow_mask = cv2.inRange(hsv, (25, 10, 0), (40, 255, 255)) #yellow
    orange_mask = cv2.inRange(hsv, (0, 10, 0), (20, 255, 255)) #orange

    mask_sums = [
    ('Red', np.sum(red_mask > 0)),
    ('Black', np.sum(black_mask > 0)),
    ('White', np.sum(white_mask > 0)),
    ('Brown', np.sum(brown_mask > 0)),
    ('Blue', np.sum(blue_mask > 0)),
    ('Purple', np.sum(purple_mask > 0)),
    ('Green', np.sum(green_mask > 0)),
    ('Yellow', np.sum(yellow_mask > 0)),
    ('Orange', np.sum(orange_mask > 0))
]

    sorted_mask_sums = sorted(mask_sums, key=lambda x: x[1], reverse=True)

    #Most frequent color is shape, next most frequent is text
    shape_color = sorted_mask_sums[0][0]
    text_color = sorted_mask_sums[1][0]

    return shape_color, text_color

#Example usage:
#shape_color, text_color = get_shape_text_colors('nimg_6.jpg')
#print(f"Shape color: {shape_color}")
#print(f"Text color: {text_color}")