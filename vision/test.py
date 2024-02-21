import unittest
from vision.odlc import shape_color_detection
from vision.odlc import matching
from vision.odlc import color


class ShapeColorDetectionTests(unittest.TestCase):
    image_path_1 = "vision/images/test/shape_color_detection_1.jpg"
    image_path_2 = "vision/images/test/shape_color_detection_2.jpg"

    def test_shape_color_detection(self):
        results = sorted(shape_color_detection.detect_shape_color
                         (self.image_path_1))
        self.assertEqual(results[0], "blue triangle")
        self.assertEqual(results[1], "orange pentagon")

    def test_shape_color_detection_false_positive(self):
        results = shape_color_detection.detect_shape_color(self.image_path_2)
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

class ColorDetectionTests(unittest.TestCase):
    image_path_1 = "vision/images/test/nimg_1.jpg"
    image_path_2 = "vision/images/test/nimg_2.jpg"
    image_path_3 = "vision/images/test/nimg_3.jpg"
    image_path_4 = "vision/images/test/nimg_4.jpg"
    image_path_5 = "vision/images/test/nimg_5.jpg"
    image_path_6 = "vision/images/test/nimg_6.jpg"

    def test__color_detection(self):
        shape_color_1, text_color_1 = color.get_shape_text_colors(self.image_path_1)
        self.assertEqual(shape_color_1, "Orange")
        self.assertEqual(text_color_1, "Black")
        shape_color_2, text_color_2 = color.get_shape_text_colors(self.image_path_2)
        self.assertEqual(shape_color_2, "Red")
        self.assertEqual(text_color_2, "Orange")
        shape_color_3, text_color_3 = color.get_shape_text_colors(self.image_path_3)
        self.assertEqual(shape_color_3, "Blue")
        self.assertEqual(text_color_3, "Green")
        shape_color_4, text_color_4 = color.get_shape_text_colors(self.image_path_4)
        self.assertEqual(shape_color_4, "Purple")
        self.assertEqual(text_color_4, "White")
        shape_color_5, text_color_5 = color.get_shape_text_colors(self.image_path_5)
        self.assertEqual(shape_color_5, "Red")
        self.assertEqual(text_color_5, "Blue")
        shape_color_6, text_color_6 = color.get_shape_text_colors(self.image_path_6)
        self.assertEqual(shape_color_6, "Black")
        self.assertEqual(text_color_6, "Red")


if __name__ == "__main__":
    unittest.main()
