import unittest
import cv2

from vision.odlc import shape_color_detection
from vision.odlc import matching


class ShapeColorDetectionTests(unittest.TestCase):
    image_path_1 = "vision/images/test/shape_color_detection_1.jpg"
    image_path_2 = "vision/images/test/shape_color_detection_2.jpg"
    image_1 = cv2.imread(image_path_1)
    image_2 = cv2.imread(image_path_2)

    def test_shape_color_detection(self):
        results = sorted(
            shape_color_detection.detect_shape_color(self.image_1))

        self.assertEqual(results[0], "blue triangle")
        self.assertEqual(results[1], "orange pentagon")

    def test_shape_color_detection_false_positive(self):
        results = shape_color_detection.detect_shape_color(self.image_2)
        self.assertEqual(results, [])


class MatchingProblemTests(unittest.TestCase):
    pattern_1 = {'color': "purple", 'shape': "triangle", 'letter': 'd'}
    pattern_2 = {'color': "red", 'shape': "circle", 'letter': 'a'}
    pattern_3 = {'color': "orange", 'shape': "square", 'letter': 'c'}

    given_patterns = [pattern_1, pattern_2, pattern_3]

    detection_0 = {
        'purple': 1,
        'triangle': 1,
        'd': 0.3
    }

    detection_1 = {
        'red': 0,
        'circle': 0,
        'a': 0,
        'orange': 1,
        'square': 1,
        'c': 1
    }

    detection_2 = {
        'purple': 1,
        'triangle': 1,
        'd': 1
    }

    detection_list = [detection_0, detection_1, detection_2]

    def test_matching_problem(self):
        result = matching.match_detections_and_patterns(3, self.given_patterns,
                                                        self.detection_list)
        self.assertEqual(result['detection_2']['color'], 'purple')
        self.assertEqual(result['detection_1']['shape'], 'square')
        self.assertEqual(result['detection_0']['letter'], 'a')


if __name__ == "__main__":
    unittest.main()
