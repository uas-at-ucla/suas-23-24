import numpy as np
import cv2
import os
import time
import onnxruntime as ort
from threading import Thread

import vision.util as util


# File Paths
TARGET_CHECKPOINT_FILE = "/app/vision/odlc/models/alphanumeric_detection.onnx"
SHAPE_COLOR_CKPT_FILE = ""

# MODEL CONSTANTS (DO NOT CHANGE)
STEP = int(os.getenv("ALPHANUMERIC_MODEL_STEP"))
FRAME_SIZE = int(os.getenv("ALPHANUMERIC_MODEL_FRAME_SIZE"))
ITERATIONS = int(os.getenv("ALPHANUMERIC_MODEL_ITERATIONS"))
CROP_AMNT = int(os.getenv("ALPHANUMERIC_MODEL_CROP_AMOUNT"))

DEBUGGING = int(os.getenv("DEBUG"))


def compute_iou(box, boxes):
    # Compute xmin, ymin, xmax, ymax for both boxes
    xmin = np.maximum(box[0], boxes[:, 0])
    ymin = np.maximum(box[1], boxes[:, 1])
    xmax = np.minimum(box[2], boxes[:, 2])
    ymax = np.minimum(box[3], boxes[:, 3])

    # Compute intersection area
    intersection_area = np.maximum(0, xmax - xmin) * np.maximum(0, ymax - ymin)

    # Compute union area
    box_area = (box[2] - box[0]) * (box[3] - box[1])
    boxes_area = (boxes[:, 2] - boxes[:, 0]) * (boxes[:, 3] - boxes[:, 1])
    union_area = box_area + boxes_area - intersection_area

    # Compute IoU
    iou = intersection_area / union_area

    return iou

# Determine if bounding box is a "Square"
def keepSquare(boxes, indices):
    keep_boxes = []
    for i in indices:
        box = boxes[i]
        width = (box[2] - box[0])
        length = (box[3] - box[1])
        if length == 0:
            continue
        if abs(width / length - 1) < 0.1:
            keep_boxes.append(i)
    return keep_boxes

def nms(boxes, scores, iou_threshold):
    # Sort by score
    sorted_indices = np.argsort(scores)[::-1]

    keep_boxes = []
    while sorted_indices.size > 0:
        # Pick the last box
        box_id = sorted_indices[0]
        keep_boxes.append(box_id)

        # Compute IoU of the picked box with the rest
        ious = compute_iou(boxes[box_id, :], boxes[sorted_indices[1:], :])

        # Remove boxes with IoU over the threshold or are not square
        keep_indices = np.where(ious < iou_threshold)[0]

        # print(keep_indices.shape, sorted_indices.shape)
        sorted_indices = sorted_indices[keep_indices + 1]

    return keep_boxes

def xywh2xyxy(x):
    # Convert bounding box (x, y, w, h) to bounding box (x1, y1, x2, y2)
    y = np.copy(x)
    y[..., 0] = x[..., 0] - x[..., 2] / 2
    y[..., 1] = x[..., 1] - x[..., 3] / 2
    y[..., 2] = x[..., 0] + x[..., 2] / 2
    y[..., 3] = x[..., 1] + x[..., 3] / 2
    return y

class TargetShapeText:
    # initialization
    def __init__(self):
        # NMS + Detection constants
        self.conf_threshold = 0.4
        self.iou_threshold = 0.4

        # initialize model
        self.session = ort.InferenceSession(
            TARGET_CHECKPOINT_FILE, 
            providers=['CUDAExecutionProvider']
        )
        model_inputs = self.session.get_inputs()
        self.input_names = [model_inputs[i].name
            for i in range(len(model_inputs))]
        self.input_shape = model_inputs[0].shape
        self.input_height = self.input_shape[2]
        self.input_width = self.input_shape[3]
        model_outputs = self.session.get_outputs()
        self.output_names = [model_outputs[i].name
            for i in range(len(model_outputs))]

        # declare return values
        self.model = None
        self.boxes = None
        self.shapes = None
        self.texts = None

        util.info(f"{ort.get_device()=}")


    # run text model
    def __runText(self, img):
        input_img = np.zeros((640,640,3),dtype=np.uint8)
        for i,box in enumerate(self.boxes):
            frame = img[
                box[1]+CROP_AMNT:box[3]-CROP_AMNT,
                box[0]+CROP_AMNT:box[2]-CROP_AMNT
            ]
            frame = cv2.resize(frame, (120,120))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            row = int(i / 4) * 120
            col = int(i % 4) * 120
            input_img[row:row+120, col:col+120] = gray
        util.debug_imwrite(input_img,
                           f"/app/vision/images/debug/{time.time()}.png")

    
    # run target model
    def run(self, img, text=False):

        # THREADING FUNCTION
        def run_model(input_tensor, results, index, row, col):
            outputs = self.session.run(self.output_names,
                                       {self.input_names[0]: input_tensor})
            boxes, _, _ = self.process_output(outputs)
            result = np.zeros((len(boxes),4), dtype=np.int32)
            add_frame = np.array([col, row, col, row])
            for i, box in enumerate(boxes):
                result[i] = box.astype(int) + add_frame
            results[index] = result

        # SLIDING WINDOW
        threads = [None] * ITERATIONS
        self.boxes = [None] * ITERATIONS
        count = 0
        for row in range(0, img.shape[0] - FRAME_SIZE, STEP):
            for col in range(0,img.shape[1] - FRAME_SIZE, STEP):
                frame = img[row:row+FRAME_SIZE,col:col+FRAME_SIZE]
                self.img_height, self.img_width = frame.shape[:2]
                resized = cv2.resize(frame, (640,640))
                resized = cv2.cvtColor(
                    cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)[:,:,0],
                    cv2.COLOR_BGR2RGB) / 255
                resized = resized.transpose(2, 0, 1)
                input_tensor = resized[np.newaxis, :, :, :].astype(np.float16)
                threads[count] = Thread(
                    target = run_model,
                    args=(input_tensor, self.boxes, count, row, col)
                )
                threads[count].start()
                count += 1

        # JOIN THREADS
        for i in range(ITERATIONS):
            threads[i].join()

        # SQUEEZE BOXES TO EASILY READABLE ARRAY
        squeezed_results = []
        for i in self.boxes:
            for box in i:
                squeezed_results.append(box) 
        self.boxes = np.array(squeezed_results)

        if DEBUGGING:
            for box in self.boxes:
                cv2.rectangle(img, (box[0],box[1]), (box[2],box[3]),
                              (255,0,0), 5)
            util.debug_imwrite(img,
                               f"/app/vision/images/debug/{time.time()}.png")

        # RUN TEXT MODEL
        if text:
            self.__runText(img)

    # Getters
    def get_boxes(self) -> np.ndarray:  
        return self.boxes
    def get_shapes(self) -> np.ndarray:
        return self.shapes
    def get_text(self) -> np.ndarray:
        return self.texts
    
    def process_output(self, output):
        predictions = np.squeeze(output[0]).T

        # Filter out object confidence scores below threshold
        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > self.conf_threshold, :]
        scores = scores[scores > self.conf_threshold]

        if len(scores) == 0:
            return [], [], []

        # Get the class with the highest confidence
        class_ids = np.argmax(predictions[:, 4:], axis=1)

        # Get bounding boxes for each object
        boxes = self.extract_boxes(predictions)

        # Apply non-maxima suppression to suppress weak, overlapping bounding boxes
        indices = nms(boxes, scores, self.iou_threshold)
        indices = keepSquare(boxes, indices=indices)

        return boxes[indices], scores[indices], class_ids[indices]

    def extract_boxes(self, predictions):
        # Extract boxes from predictions
        boxes = predictions[:, :4]

        # Scale boxes to original image dimensions
        boxes = self.rescale_boxes(boxes)

        # Convert boxes to xyxy format
        boxes = xywh2xyxy(boxes)

        return boxes

    def rescale_boxes(self, boxes):

        # Rescale boxes to original image dimensions
        input_shape = np.array([self.input_width, self.input_height, self.input_width, self.input_height])
        boxes = np.divide(boxes, input_shape, dtype=np.float32)
        boxes *= np.array([self.img_width, self.img_height, self.img_width, self.img_height])
        return boxes
    