import requests
import subprocess
from datetime import datetime

def take_picture_and_queue():
    current_time = datetime.now()
    time = current_time.strftime("%H%M%S")

    # Define the gphoto2 command to capture an image
    command = ['gphoto2', '--capture-image-and-download', f'--filename=../../vision/images/odlc/{time}.jpg']

    # Run the gphoto2 command
    subprocess.run(command, check=True)

    # Send request to vision server
    requests.post('http://localhost:8003/odlc', json={
        'img_name': f'{time}.jpg',
        'altitude': 0,
        'latitude': 0, 
        'longitude': 0,
        'heading': 0
    })

if __name__ == "__main__":
    take_picture_and_queue()
