import unittest
import cv2
from parameterized import parameterized

from vision.odlc import shape_color_detection
from vision.odlc import matching


class ShapeColorDetectionTests(unittest.TestCase):

    model = shape_color_detection.Model()

    @parameterized.expand([
        (
            "vision/images/test/shape_color_detection_1.jpg",
            ["blue triangle", "orange pentagon"]
        ),
        (
            "vision/images/test/shape_color_detection_2.jpg",
            []
        )
    ])
    def test_shape_color_detection(self, image_path, targets):
        results = sorted(self.model.detect_shape_color(cv2.imread(image_path)))
        self.assertEqual(results, targets)


class MatchingProblemTests(unittest.TestCase):

    def test_matching_problem(self):

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

        result = matching.match_detections_and_patterns(3, given_patterns,
                                                        detection_list)
        self.assertEqual(result['detection_2']['color'], 'purple')
        self.assertEqual(result['detection_1']['shape'], 'square')
        self.assertEqual(result['detection_0']['letter'], 'a')


if __name__ == "__main__":
    unittest.main()
