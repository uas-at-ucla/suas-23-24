import torch
from ultralytics import YOLO
import cv2
import math

import vision.util as util


class ShapeColorDetector:
    def __init__(self):
        self.model = YOLO('vision/odlc/models/shape_color_checkpoint.pt')
        self.model.info()

        # get class names
        self.classes = []
        with open("vision/odlc/shape_color_classes.txt", "r") as f:
            for class_name in f.read().splitlines():
                self.classes.append(class_name)

        # define device
        if torch.cuda.is_available():
            util.info(torch.cuda.get_device_name(0))
            util.info(torch.cuda.get_device_properties(0))
        else:
            util.info("CPU")

    def detect_shape_color(self, frame_name):
        frame = cv2.imread(frame_name)
        results = self.model(frame, verbose=False)
        ans = []
        for r in results:
            boxes = r.boxes
            for box in boxes:
                x1, y1, x2, y2 = box.xyxy[0]
                x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

                conf = math.ceil(box.conf[0] * 100) / 100
                cls = int(box.cls[0])

                if (conf > 0.5):
                    # target_info = handle_target(frame[y1:y2,x1:x2])
                    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 1)
                    cv2.putText(
                        frame,
                        (self.classes[cls]),
                        (x1, y1),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        (255, 0, 0),
                        1)
                    ans.append(self.classes[cls])
        return ans
