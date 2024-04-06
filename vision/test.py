import unittest
import cv2
from parameterized import parameterized

from vision.odlc import shape_color_detection
from vision.odlc import matching
from vision.odlc import color


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


class ColorDetectionTests(unittest.TestCase):
    image_path_1 = "vision/images/test/2-22-24-Images/cropped/t1.jpg"
    image_path_2 = "vision/images/test/2-22-24-Images/cropped/t2.jpg"
    image_path_3 = "vision/images/test/2-22-24-Images/cropped/t3.jpg"
    image_path_4 = "vision/images/test/2-22-24-Images/cropped/t4.jpg"
    image_path_5 = "vision/images/test/2-22-24-Images/cropped/t5.jpg"
    image_path_6 = "vision/images/test/2-22-24-Images/cropped/t6.jpg"
    image_path_7 = "vision/images/test/2-22-24-Images/cropped/t7.jpg"
    image_path_8 = "vision/images/test/2-22-24-Images/cropped/t8.jpg"
    image_path_9 = "vision/images/test/2-22-24-Images/cropped/t9.jpg"
    image_path_10 = "vision/images/test/2-22-24-Images/cropped/t10.jpg"
    image_path_11 = "vision/images/test/2-22-24-Images/cropped/t11.jpg"
    image_path_12 = "vision/images/test/2-22-24-Images/cropped/t12.jpg"
    image_path_13 = "vision/images/test/2-22-24-Images/cropped/t13.jpg"
    image_path_14 = "vision/images/test/2-22-24-Images/cropped/t14.jpg"
    image_path_15 = "vision/images/test/2-22-24-Images/cropped/t15.jpg"
    image_path_16 = "vision/images/test/2-22-24-Images/cropped/t16.jpg"
    image_path_17 = "vision/images/test/2-22-24-Images/cropped/t17.jpg"
    image_path_18 = "vision/images/test/2-22-24-Images/cropped/t18.jpg"
    image_path_19 = "vision/images/test/2-22-24-Images/cropped/t19.jpg"

    def test__color_detection(self):
        shape_color_1, text_color_1 = color.get_shape_text_colors(
            self.image_path_1)
        self.assertEqual(shape_color_1, "Black")
        self.assertEqual(text_color_1, "Blue")

        shape_color_2, text_color_2 = color.get_shape_text_colors(
            self.image_path_2)
        self.assertEqual(shape_color_2, "Orange")
        # self.assertEqual(text_color_2, "Black")

        shape_color_3, text_color_3 = color.get_shape_text_colors(
            self.image_path_3)
        self.assertEqual(shape_color_3, "Red")
        self.assertEqual(text_color_3, "Purple")

        shape_color_4, text_color_4 = color.get_shape_text_colors(
            self.image_path_4)
        self.assertEqual(shape_color_4, "Brown")
        self.assertEqual(text_color_4, "Purple")

        shape_color_5, text_color_5 = color.get_shape_text_colors(
            self.image_path_5)
        self.assertEqual(shape_color_5, "Blue")
        self.assertEqual(text_color_5, "Green")

        shape_color_6, text_color_6 = color.get_shape_text_colors(
            self.image_path_6)
        self.assertEqual(shape_color_6, "Blue")
        self.assertEqual(text_color_6, "Green")

        shape_color_7, text_color_7 = color.get_shape_text_colors(
            self.image_path_7)
        self.assertEqual(shape_color_7, "White")
        # self.assertEqual(text_color_7, "Orange")

        shape_color_8, text_color_8 = color.get_shape_text_colors(
            self.image_path_8)
        self.assertEqual(shape_color_8, "Black")
        self.assertEqual(text_color_8, "Red")

        shape_color_9, text_color_9 = color.get_shape_text_colors(
            self.image_path_9)
        self.assertEqual(shape_color_9, "Black")
        # self.assertEqual(text_color_9, "Red")

        shape_color_10, text_color_10 = color.get_shape_text_colors(
            self.image_path_10)
        self.assertEqual(shape_color_10, "Orange")
        self.assertEqual(text_color_10, "White")

        shape_color_11, text_color_11 = color.get_shape_text_colors(
            self.image_path_11)
        self.assertEqual(shape_color_11, "Green")
        # self.assertEqual(text_color_11, "Brown")

        shape_color_12, text_color_12 = color.get_shape_text_colors(
            self.image_path_12)
        # self.assertEqual(shape_color_12, "Purple")
        # self.assertEqual(text_color_12, "Black")

        shape_color_13, text_color_13 = color.get_shape_text_colors(
            self.image_path_13)
        # self.assertEqual(shape_color_13, "Brown")
        # self.assertEqual(text_color_13, "Orange")

        shape_color_14, text_color_14 = color.get_shape_text_colors(
            self.image_path_14)
        self.assertEqual(shape_color_14, "Red")
        self.assertEqual(text_color_14, "Purple")

        shape_color_15, text_color_15 = color.get_shape_text_colors(
            self.image_path_15)
        self.assertEqual(shape_color_15, "Blue")
        # self.assertEqual(text_color_15, "Red")

        shape_color_16, text_color_16 = color.get_shape_text_colors(
            self.image_path_16)
        self.assertEqual(shape_color_16, "White")
        # self.assertEqual(text_color_16, "Purple")

        shape_color_17, text_color_17 = color.get_shape_text_colors(
            self.image_path_17)
        self.assertEqual(shape_color_17, "Green")
        self.assertEqual(text_color_17, "White")

        shape_color_18, text_color_18 = color.get_shape_text_colors(
            self.image_path_18)
        self.assertEqual(shape_color_18, "White")
        # self.assertEqual(text_color_18, "Brown")

        shape_color_19, text_color_19 = color.get_shape_text_colors(
            self.image_path_19)
        self.assertEqual(shape_color_19, "Green")
        self.assertEqual(text_color_19, "Orange")


if __name__ == "__main__":
    unittest.main()
