import torch
from ultralytics import YOLO
import cv2
import math

model = YOLO('vision/odlc/models/best.pt')
model.info()

CLASSES = [
    'black circle',
    'black semicircle',
    'black quarter circle',
    'black triangle',
    'black rectangle',
    'black pentagon',
    'black star',
    'black cross',
    'white circle',
    'white semicircle',
    'white quarter circle',
    'white triangle',
    'white rectangle',
    'white pentagon',
    'white star',
    'white cross',
    'red circle',
    'red semicircle',
    'red quarter circle',
    'red triangle',
    'red rectangle',
    'red pentagon',
    'red star',
    'red cross',
    'green circle',
    'green semicircle',
    'green quarter circle',
    'green triangle',
    'green rectangle',
    'green pentagon',
    'green star',
    'green cross',
    'blue circle',
    'blue semicircle',
    'blue quarter circle',
    'blue triangle',
    'blue rectangle',
    'blue pentagon',
    'blue star',
    'blue cross',
    'purple circle',
    'purple semicircle',
    'purple quarter circle',
    'purple triangle',
    'purple rectangle',
    'purple pentagon',
    'purple star',
    'purple cross',
    'orange circle',
    'orange semicircle',
    'orange quarter circle',
    'orange triangle',
    'orange rectangle',
    'orange pentagon',
    'orange star',
    'orange cross',
    'brown circle',
    'brown semicircle',
    'brown quarter circle',
    'brown triangle',
    'brown rectangle',
    'brown pentagon',
    'brown star',
    'brown cross',
]

# define device
if torch.cuda.is_available():
    print(torch.cuda.get_device_name(0))
    print(torch.cuda.get_device_properties(0))
else:
    print("CPU")


def detect_shape_color(frame_name):
    frame = cv2.imread(frame_name)
    results = model(frame, verbose=False)
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
                    (CLASSES[cls]),
                    (x1, y1),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (255, 0, 0),
                    1)
                ans.append(CLASSES[cls])
    return ans
