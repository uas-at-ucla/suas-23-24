import requests
import subprocess
from datetime import datetime

current_time = datetime.now()
time = current_time.strftime("%H%M%S")

# Define the gphoto2 command to capture an image
command = ['gphoto2', '--capture-image-and-download', f'--filename=../../vision/images/{time}']


# Run the gphoto2 command
subprocess.run(command, check=True)
