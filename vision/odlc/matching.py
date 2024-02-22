import numpy as np
from scipy.optimize import linear_sum_assignment


def get_detection_confidence_array(given_patterns, detection_list,
                                   n_detections, confidence_table):
    for i in range(0, n_detections):
        for j in range(0, n_detections):
            # sets color, shape, and letter based on pattern
            color = given_patterns[i]["color"]
            shape = given_patterns[i]["shape"]
            letter = given_patterns[i]["letter"]

            # goes to the drone detection dictionary, and matches pattern's
            # color, shape, and letter. Combines three individual percentages
            # into one complete detection percentage
            if color in detection_list[j]:
                confidence_table[i][j] += \
                    detection_list[j][given_patterns[i]["color"]]
            if shape in detection_list[j]:
                confidence_table[i][j] += \
                    detection_list[j][given_patterns[i]["shape"]]
            if letter in detection_list[j]:
                confidence_table[i][j] += \
                    detection_list[j][given_patterns[i]["letter"]]


def match_detections_and_patterns(n_detections, given_patterns,
                                  detection_list):
    confidence_table = np.zeros((n_detections, n_detections))
    get_detection_confidence_array(given_patterns, detection_list,
                                   n_detections, confidence_table)

    # Call linear_sum_assignment() function from scipy
    row_ind, col_ind = linear_sum_assignment(-confidence_table)

    # Print the matches
    ans = {}
    for x in range(n_detections):
        current_detection = "detection_" + str(col_ind[x])
        ans[current_detection] = {
            'color': str(given_patterns[x]['color']),
            'shape': str(given_patterns[x]['shape']),
            'letter': str(given_patterns[x]['letter'])
        }

    print(ans)
    return ans
