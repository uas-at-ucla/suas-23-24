import torch

from ultralytics import YOLO

import cv2
import math


model = YOLO("/app/vision/odlc/models/shape_color_checkpoint.pt")
model.info()

# get class names
classes = []
with open("/app/vision/odlc/shape_color_classes.txt", "r") as f:
    for class_name in f.read().splitlines():
        classes.append(class_name)

# define device
if torch.cuda.is_available():
    print(torch.cuda.get_device_name(0))
    print(torch.cuda.get_device_properties(0))
else:
    print("CPU")


def detect_shape_color(frame):
    results = model(frame, verbose=False)
    ans = []
    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            conf = math.ceil(box.conf[0] * 100) / 100
            cls = int(box.cls[0])

            if conf > 0.5:
                # target_info = handle_target(frame[y1:y2,x1:x2])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 1)
                cv2.putText(
                    frame,
                    (classes[cls]),
                    (x1, y1),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    1,
                )
                ans.append(classes[cls])
    return ans
