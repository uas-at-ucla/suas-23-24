import mmap
import io
import numpy as np
import cv2

with open("/dev/shm/PictureData", "r+b") as f:
    mapped_file = mmap.mmap(f.fileno(), 0)
    data = mapped_file.read()
    binary_stream = io.BytesIO(data)
    image_array = np.asarray(bytearray(binary_stream.read()), dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

    cv2.imwrite("test.jpg", image)
