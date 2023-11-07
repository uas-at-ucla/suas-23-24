import asyncio
import os
import shutil
import requests
import random
import websockets

# from mavsdk import System

# Setup Prometheus metrics

vision_endoint = "http://localhost:8003/"


OUTPUT_IMAGE_DIRECTORY = "../vision/images/odlc"


async def run():

    print("Starting flight software")

    while True:
        await asyncio.sleep(1)
        # make a POST request to vision/post_telemetry with random data

        endpoint = vision_endoint + "post_telemetry"
        data = {
            "altitude": random.uniform(0, 10000),  # Altitude in feet
            "latitude": random.uniform(-90, 90),  # Latitude in degrees
            "longitude": random.uniform(-180, 180),  # Longitude in degrees
            "heading": random.uniform(0, 360)  # Heading in degrees
        }

        r = requests.post(endpoint, json=data)
        print(r.status_code)



    # Create image output directory
    if os.path.exists(os.path.join(os.getcwd(), OUTPUT_IMAGE_DIRECTORY)):
        shutil.rmtree(os.path.join(os.getcwd(), OUTPUT_IMAGE_DIRECTORY))
    os.makedirs(os.path.join(os.getcwd(), OUTPUT_IMAGE_DIRECTORY),
                exist_ok=True)

    # Initialize camera

    # Post targets

    # Connect to drone
    print('Conencting to drone')
    drone = System()
    await drone.connect(system_address="udp://:14540")

    # Upload mission fences

    # Setup waypoint mission

    # Start autopilot

    # Start waypoint mission

    # Upload airdrop fences

    # Airdrop scan

    # Get image detections

    # Do airdrops, possibly return to refuel or refill payloads

    # Return to home


if __name__ == "__main__":
    asyncio.run(run())
