import unittest

from vision.odlc import shape_color_detection

class ShapeColorDetectionTests(unittest.TestCase):
    image_path_1 = "vision/images/test/shape_color_detection_1.jpg"
    image_path_2 = "vision/images/test/shape_color_detection_2.jpg"

    def test_shape_color_detection(self):
        results = sorted(
            shape_color_detection.detect_shape_color(
                self.image_path_1))
        self.assertEqual(results[0], "blue triangle")
        self.assertEqual(results[1], "orange pentagon")

    def test_shape_color_detection_false_positive(self):
        results = shape_color_detection.detect_shape_color(self.image_path_2)
        self.assertEqual(results, [])

if __name__ == "__main__":
    unittest.main()
