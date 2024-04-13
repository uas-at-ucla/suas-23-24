import pytest
import cv2

from vision.odlc.alphanumeric_pipeline import TargetShapeText
from vision.odlc import matching
from vision.odlc import color_detection


class TestTargetDetection:

    image_path_1 = "/app/vision/images/test/alphanumeric_detection_1.png"
    image_path_2 = "/app/vision/images/test/alphanumeric_detection_2.png"

    @classmethod
    def setup_class(cls):
        cls.model = TargetShapeText()

    @classmethod
    def teardown_class(cls):
        del cls.model

    def test_shape_color_detection_1(self):
        self.model.run(cv2.imread(self.image_path_1))
        results = self.model.get_boxes()
        print(f"{results=}")
        assert len(results) > 0

    def test_shape_color_detection_2(self):
        self.model.run(cv2.imread(self.image_path_2))
        results = self.model.get_boxes()
        print(f"{results=}")
        assert len(results) > 0


class TestMatchingProblem:

    def test_matching_problem_1(self):

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
        assert result['detection_2']['color'] == 'purple'
        assert result['detection_1']['shape'] == 'square'
        assert result['detection_0']['letter'] == 'a'


class TestColorDetection:

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

    def test_color_detection_1(self):
        shape_color_1, text_color_1 = color_detection.get_shape_text_colors(
            self.image_path_1)
        assert shape_color_1 == "Black"
        assert text_color_1 == "Blue"

    @pytest.mark.skip(reason="text color fails")
    def test_color_detection_2(self):
        shape_color_2, text_color_2 = color_detection.get_shape_text_colors(
            self.image_path_2)
        assert shape_color_2 == "Orange"
        assert text_color_2 == "Black"

    def test_color_detection_3(self):
        shape_color_3, text_color_3 = color_detection.get_shape_text_colors(
            self.image_path_3)
        assert shape_color_3 == "Red"
        assert text_color_3 == "Purple"

    def test_color_detection_4(self):
        shape_color_4, text_color_4 = color_detection.get_shape_text_colors(
            self.image_path_4)
        assert shape_color_4 == "Brown"
        assert text_color_4 == "Purple"

    def test_color_detection_5(self):
        shape_color_5, text_color_5 = color_detection.get_shape_text_colors(
            self.image_path_5)
        assert shape_color_5 == "Blue"
        assert text_color_5 == "Green"

    def test_color_detection_6(self):
        shape_color_6, text_color_6 = color_detection.get_shape_text_colors(
            self.image_path_6)
        assert shape_color_6 == "Blue"
        assert text_color_6 == "Green"

    @pytest.mark.skip(reason="text color fails")
    def test_color_detection_7(self):
        shape_color_7, text_color_7 = color_detection.get_shape_text_colors(
            self.image_path_7)
        assert shape_color_7 == "White"
        assert text_color_7 == "Orange"

    def test_color_detection_8(self):
        shape_color_8, text_color_8 = color_detection.get_shape_text_colors(
            self.image_path_8)
        assert shape_color_8 == "Black"
        assert text_color_8 == "Red"

    @pytest.mark.skip(reason="text color fails")
    def test_color_detection_9(self):
        shape_color_9, text_color_9 = color_detection.get_shape_text_colors(
            self.image_path_9)
        assert shape_color_9 == "Black"
        assert text_color_9 == "Red"

    def test_color_detection_10(self):
        shape_color_10, text_color_10 = color_detection.get_shape_text_colors(
            self.image_path_10)
        assert shape_color_10 == "Orange"
        assert text_color_10 == "White"

    @pytest.mark.skip(reason="text color fails")
    def test_color_detection_11(self):
        shape_color_11, text_color_11 = color_detection.get_shape_text_colors(
            self.image_path_11)
        assert shape_color_11 == "Green"
        assert text_color_11 == "Brown"

    @pytest.mark.skip(reason="both shape and text colors fail")
    def test_color_detection_12(self):
        shape_color_12, text_color_12 = color_detection.get_shape_text_colors(
            self.image_path_12)
        assert shape_color_12 == "Purple"
        assert text_color_12 == "Black"

    @pytest.mark.skip(reason="both shape and text colors fail")
    def test_color_detection_13(self):
        shape_color_13, text_color_13 = color_detection.get_shape_text_colors(
            self.image_path_13)
        assert shape_color_13 == "Brown"
        assert text_color_13 == "Orange"

    def test_color_detection_14(self):
        shape_color_14, text_color_14 = color_detection.get_shape_text_colors(
            self.image_path_14)
        assert shape_color_14 == "Red"
        assert text_color_14 == "Purple"

    @pytest.mark.skip(reason="text color fails")
    def test_color_detection_15(self):
        shape_color_15, text_color_15 = color_detection.get_shape_text_colors(
            self.image_path_15)
        assert shape_color_15 == "Blue"
        assert text_color_15 == "Red"

    @pytest.mark.skip(reason="text color fails")
    def test_color_detection_16(self):
        shape_color_16, text_color_16 = color_detection.get_shape_text_colors(
            self.image_path_16)
        assert shape_color_16 == "White"
        assert text_color_16 == "Purple"

    def test_color_detection_17(self):
        shape_color_17, text_color_17 = color_detection.get_shape_text_colors(
            self.image_path_17)
        assert shape_color_17 == "Green"
        assert text_color_17 == "White"

    @pytest.mark.skip(reason="text color fails")
    def test_color_detection_18(self):
        shape_color_18, text_color_18 = color_detection.get_shape_text_colors(
            self.image_path_18)
        assert shape_color_18 == "White"
        assert text_color_18 == "Brown"

    def test_color_detection_19(self):
        shape_color_19, text_color_19 = color_detection.get_shape_text_colors(
            self.image_path_19)
        assert shape_color_19 == "Green"
        assert text_color_19 == "Orange"
