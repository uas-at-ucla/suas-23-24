import numpy as np
import cv2


def get_shape_text_colors(image_path):
    image = cv2.imread(image_path)
    filtered_image = cv2.medianBlur(image, ksize=11)

    hsv_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2HSV)
    # Apply blur to v channel of image
    v_channel = hsv_image[:, :, 2]
    v_blurred = cv2.GaussianBlur(v_channel, (3, 3), 0)

    # Perform edge detection using Sobel
    sobel_x = cv2.Sobel(v_blurred, cv2.CV_64F, 1, 0, ksize=3)
    sobel_y = cv2.Sobel(v_blurred, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
    # Threshold the gradient magnitude to obtain edges
    edge_threshold = 20
    edges = np.uint8(gradient_magnitude > edge_threshold)

    # Find the largest contour and make the background pure gray
    normalized_gradient = cv2.normalize(edges, None, 0, 255,
                                        cv2.NORM_MINMAX, cv2.CV_8UC1)
    _, binary_image = cv2.threshold(normalized_gradient, 0, 255,
                                    cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL,
                                   cv2.CHAIN_APPROX_SIMPLE)
    largest_contour = max(contours, key=cv2.contourArea)
    contour_image = np.zeros_like(binary_image)
    cv2.drawContours(contour_image, [largest_contour], -1, 255,
                     thickness=cv2.FILLED)

    kernel = np.ones((9, 9), np.uint8)
    eroded_mask = cv2.erode(contour_image, kernel, iterations=1)
    eroded_mask = eroded_mask.astype(np.uint8)
    result_image = cv2.bitwise_and(contour_image, contour_image,
                                   mask=eroded_mask)

    final_image = cv2.bitwise_and(image, image, mask=result_image)
    final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
    gray_color = [128, 128, 128]
    black_mask = np.all(final_image == [0, 0, 0], axis=-1)
    final_image[black_mask] = gray_color

    # Check if the edge detection actually found a shape
    # Try edge detection on saturation otherwise
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
        normalized_gradient = cv2.normalize(edges, None, 0, 255,
                                            cv2.NORM_MINMAX, cv2.CV_8UC1)
        _, binary_image = cv2.threshold(normalized_gradient, 0, 255,
                                        cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL,
                                       cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = max(contours, key=cv2.contourArea)
        contour_image = np.zeros_like(binary_image)
        cv2.drawContours(contour_image, [largest_contour], -1, 255,
                         thickness=cv2.FILLED)

        kernel = np.ones((9, 9), np.uint8)
        eroded_mask = cv2.erode(contour_image, kernel, iterations=1)
        eroded_mask = eroded_mask.astype(np.uint8)
        result_image = cv2.bitwise_and(contour_image, contour_image,
                                       mask=eroded_mask)

        final_image = cv2.bitwise_and(image, image, mask=result_image)
        final_image = cv2.cvtColor(final_image, cv2.COLOR_BGR2RGB)
        gray_color = [128, 128, 128]
        black_mask = np.all(final_image == [0, 0, 0], axis=-1)
        final_image[black_mask] = gray_color
        non_gray_count = np.sum(np.any(final_image != gray_color, axis=-1) > 0)
        percent = non_gray_count/image.shape[0]/image.shape[1]

    sum_rgb = np.sum(final_image, axis=-1)

    # Remove white, black, and brown pixels from the image first
    white_threshold = 600
    black_threshold = 400
    range_rgb = np.max(final_image, axis=-1) - np.min(final_image, axis=-1)
    color_range_threshold = 0.5

    hsv = cv2.cvtColor(final_image, cv2.COLOR_RGB2HSV)
    brown_mask = (cv2.inRange(hsv, (0, 10, 0), (180, 70, 160)) > 0)
    brown_mask = (
        (cv2.inRange(final_image, (145, 115, 130), (175, 135, 150)) > 0) |
        (cv2.inRange(final_image, (115, 180, 145), (130, 190, 170)) > 0)
    )

    # Create masks for white and black pixels based on the thresholds
    white_mask = sum_rgb > white_threshold
    black_mask = (
        (sum_rgb < black_threshold) &
        (range_rgb <= (color_range_threshold * np.max(final_image, axis=-1))) &
        (sum_rgb != 384)
    )

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

    # Apply masks for various colors that are not white, black, or brown
    hsv = cv2.cvtColor(final_image, cv2.COLOR_RGB2HSV)
    red_mask = cv2.inRange(hsv, (165, 10, 0), (180, 255, 255))
    blue_mask = cv2.inRange(hsv, (100, 1, 0), (125, 255, 255))
    purple_mask = cv2.inRange(hsv, (125, 10, 0), (165, 255, 255))
    green_mask = cv2.inRange(hsv, (50, 10, 0), (100, 255, 255))
    yellow_mask = cv2.inRange(hsv, (25, 10, 0), (40, 255, 255))
    orange_mask = cv2.inRange(hsv, (0, 10, 0), (20, 255, 255))

    mask_sums = [
        ('red', np.sum(red_mask > 0)),
        ('black', np.sum(black_mask > 0)),
        ('white', np.sum(white_mask > 0)),
        ('brown', np.sum(brown_mask > 0)),
        ('blue', np.sum(blue_mask > 0)),
        ('purple', np.sum(purple_mask > 0)),
        ('green', np.sum(green_mask > 0)),
        ('yellow', np.sum(yellow_mask > 0)),
        ('orange', np.sum(orange_mask > 0))
    ]

    sorted_mask_sums = sorted(mask_sums, key=lambda x: x[1], reverse=True)

    shape_dict = {
        'red': 0,
        'black': 0,
        'white': 0,
        'brown': 0,
        'blue': 0,
        'purple': 0,
        'green': 0,
        'orange': 0,
        'yellow': 0
    }

    text_dict = {
        'red': 0,
        'black': 0,
        'white': 0,
        'brown': 0,
        'blue': 0,
        'purple': 0,
        'green': 0,
        'orange': 0,
        'yellow': 0
    }

    for idx, (color, count) in enumerate(sorted_mask_sums[:2], start=1):
        if idx == 1:
            if (color == 'black' or color == 'white' or color == 'green' or
                    color == 'orange' or color == 'yellow'):
                shape_dict[color] = 100
            if (color == 'red'):
                shape_dict['red'] = 90
                shape_dict['brown'] = 5
                shape_dict['purple'] = 5
            if (color == 'brown'):
                shape_dict['red'] = 5
                shape_dict['brown'] = 90
                shape_dict['purple'] = 5
            if (color == 'blue'):
                shape_dict['blue'] = 90
                shape_dict['purple'] = 10
            if (color == 'purple'):
                shape_dict['blue'] = 80
                shape_dict['purple'] = 10
                shape_dict['red'] = 10
        else:
            if (color == 'white' or color == 'green' or
                    color == 'orange' or color == 'yellow'):
                text_dict[color] = 100
            if (color == 'red'):
                text_dict['red'] = 75
                text_dict['brown'] = 5
                text_dict['purple'] = 15
                text_dict['black'] = 5
            if (color == 'black'):
                text_dict['red'] = 5
                text_dict['blue'] = 5
                text_dict['brown'] = 5
                text_dict['purple'] = 5
                text_dict['black'] = 80
            if (color == 'brown'):
                text_dict['red'] = 5
                text_dict['brown'] = 80
                text_dict['purple'] = 10
                text_dict['black'] = 5
            if (color == 'blue'):
                text_dict['blue'] = 85
                text_dict['purple'] = 10
                text_dict['black'] = 5
            if (color == 'purple'):
                text_dict['red'] = 15
                text_dict['brown'] = 5
                text_dict['purple'] = 70
                text_dict['black'] = 5
                text_dict['blue'] = 5
        if idx == 1:
            if (color == 'white'):
                text_dict['red'] = 12.5
                text_dict['black'] = 12.5
                text_dict['brown'] = 12.5
                text_dict['blue'] = 12.5
                text_dict['purple'] = 12.5
                text_dict['green'] = 12.5
                text_dict['orange'] = 12.5
                text_dict['yellow'] = 12.5

    return shape_dict, text_dict
