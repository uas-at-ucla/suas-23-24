import numpy as np
import cv2
import os
import time
import tensorrt as trt

from vision.odlc import trt_common
import vision.util as util


# File Paths
TARGET_CHECKPOINT_FILE = "/app/vision/odlc/models/alphanumeric_detector.engine"
SHAPE_COLOR_CKPT_FILE = ""

# MODEL CONSTANTS (DO NOT CHANGE)
STEP = int(os.getenv("ALPHANUMERIC_MODEL_STEP"))
FRAME_SIZE = int(os.getenv("ALPHANUMERIC_MODEL_FRAME_SIZE"))
ITERATIONS = int(os.getenv("ALPHANUMERIC_MODEL_ITERATIONS"))
CROP_AMNT = int(os.getenv("ALPHANUMERIC_MODEL_CROP_AMOUNT"))

CONF_THRESHOLD = float(os.getenv("ALPHANUMERIC_MODEL_CONF_THRESHOLD"))
IOU_THRESHOLD = float(os.getenv("ALPHANUMERIC_MODEL_IOU_THRESHOLD"))

DEBUGGING = int(os.getenv("DEBUG"))

INPUT_SIZE = 640
TRT_LOGGER = trt.Logger(trt.Logger.WARNING)


def load_engine(model_file):
    with open(model_file, "rb") as f:
        engine_bytes = f.read()

    runtime = trt.Runtime(TRT_LOGGER)
    return runtime.deserialize_cuda_engine(engine_bytes)


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

    def __init__(self):

        # initialize model, allocate memory
        self.engine = load_engine(TARGET_CHECKPOINT_FILE)

        self.inputs, self.outputs, self.bindings, self.stream = \
            trt_common.allocate_buffers(self.engine)
        self.context = self.engine.create_execution_context()

        # declare return values
        self.model = None
        self.boxes = None
        self.shapes = None
        self.texts = None

    # need to free gpu memory
    def __del__(self):
        trt_common.free_buffers(self.inputs, self.outputs, self.stream)

    # run text model
    def __runText(self, img):
        input_img = np.zeros((INPUT_SIZE, INPUT_SIZE, 3), dtype=np.uint8)
        for i, box in enumerate(self.boxes):
            frame = img[
                box[1]+CROP_AMNT:box[3]-CROP_AMNT,
                box[0]+CROP_AMNT:box[2]-CROP_AMNT
            ]
            frame = cv2.resize(frame, (120, 120))
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            row = int(i / 4) * 120
            col = int(i % 4) * 120
            input_img[row:row+120, col:col+120] = gray
        util.debug_imwrite(input_img,
                           f"/app/vision/images/debug/{time.time()}.png")

    # run target model
    def run(self, img, text=False):

        def run_model(input_tensor):

            # copy input tensor to gpu memory
            np.copyto(self.inputs[0].host, input_tensor.ravel())

            outputs = trt_common.do_inference(
                self.context,
                engine=self.engine,
                bindings=self.bindings,
                inputs=self.inputs,
                outputs=self.outputs,
                stream=self.stream
            )
            outputs = outputs[0].reshape(ITERATIONS,1,5,8400)

            boxes = []
            count = 0
            for row in range(0, img.shape[0] - FRAME_SIZE, STEP):
                for col in range(0, img.shape[1] - FRAME_SIZE, STEP):
                    curr_boxes, _, _ = self.process_output(outputs[count])
                    add_frame = np.array([col, row, col, row])

                    for box in curr_boxes:
                        boxes.append(box.astype(int) + add_frame)
                    count += 1

            return np.array(boxes)

        # SLIDING WINDOW
        input_tensor = np.zeros((ITERATIONS, 3, 640, 640))
        count = 0
        
        for row in range(0, img.shape[0] - FRAME_SIZE, STEP):
            for col in range(0, img.shape[1] - FRAME_SIZE, STEP):
                frame = img[row:row+FRAME_SIZE, col:col+FRAME_SIZE]
                resized = cv2.resize(frame, (INPUT_SIZE, INPUT_SIZE))
                resized = cv2.cvtColor(
                    cv2.cvtColor(resized, cv2.COLOR_BGR2HSV)[:, :, 0],
                    cv2.COLOR_BGR2RGB) / 255
                resized = resized.transpose(2, 0, 1)

                input_tensor[count] = \
                    resized[np.newaxis, :, :, :].astype(np.float32)
                count += 1

        self.boxes = run_model(input_tensor)

        if DEBUGGING:
            for box in self.boxes:
                cv2.rectangle(img, (box[0], box[1]), (box[2], box[3]),
                              (255, 0, 0), 5)
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
        predictions = np.squeeze(output).T

        # Filter out object confidence scores below threshold
        scores = np.max(predictions[:, 4:], axis=1)
        predictions = predictions[scores > CONF_THRESHOLD, :]
        scores = scores[scores > CONF_THRESHOLD]

        if len(scores) == 0:
            return [], [], []

        # Get the class with the highest confidence
        class_ids = np.argmax(predictions[:, 4:], axis=1)

        # Get bounding boxes for each object
        boxes = self.extract_boxes(predictions)

        # Apply non-maxima suppression to suppress
        # weak, overlapping bounding boxes
        indices = nms(boxes, scores, IOU_THRESHOLD)
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
        input_shape = np.array([INPUT_SIZE] * 4)
        boxes = np.divide(boxes, input_shape, dtype=np.float32)
        boxes *= FRAME_SIZE
        return boxes
