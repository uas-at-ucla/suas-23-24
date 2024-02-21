import cv2
import subprocess
import time
import signal

# This example executes the "usb_to_camera.py" file
# and uses OpenCV to stream the newly added usb camera
# to the screen.
# Only run this file by itself to have the camera running.

# Optionally commented out is the option to take photos
# from the stream once per frame (capped at 1000).
camera_command = ["python3", "usb_to_camera.py"]
add_camera = subprocess.Popen(camera_command)
time.sleep(5)
cap = cv2.VideoCapture(4)
counter = 0

while True:
    ret, frame = cap.read()  # Read a frame from the virtual webcam
    if not ret:
        break

    # Display the frame (you can perform processing here if needed)
    cv2.imshow("Camera Output", frame)

    key = cv2.waitKey(1) & 0xFF

    """ Will take a photo every loop up to 1000 photos and store it in the-
        src/ folder
    """
    file_name = 'images/image' + str(counter) + '.jpg'
    if(counter < 1000):
        cv2.imwrite(file_name, frame)
        print("Captured an Image")
        counter = counter + 1

    # Break the loop on 'q' key press
    if key == ord("q"):
        break

# Release resources & terminate subprocesses
add_camera.send_signal(signal.SIGINT)
cap.release()
cv2.destroyAllWindows()
