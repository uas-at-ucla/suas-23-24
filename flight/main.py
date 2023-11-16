import asyncio
import os
import shutil
import json
import random
import websockets

# from mavsdk import System

# Setup Prometheus metrics

GLOBAL_ENDPOINT = "wss://free.blr2.piesocket.com/v3/1?api_key=VoyZpzPDK56LAUAxV7UdXceZYiUBLGnKLeLg5v69&notify_self=1"
LOCAL_ENDPOINT = "ws://localhost:8001"

CURRENT_ENDPOINT = LOCAL_ENDPOINT


OUTPUT_IMAGE_DIRECTORY = "../vision/images/odlc"

# Connect to vision websocket
websockets.connect(CURRENT_ENDPOINT)


async def run():

    print("Starting flight software")

    # Create a persistent connection to the websocket
    async with websockets.connect(CURRENT_ENDPOINT) as websocket:
        # Initialize data with starting values
        data = {
            "altitude": 0,  # Altitude in feet
            "latitude": 0,  # Latitude in degrees
            "longitude": 0,  # Longitude in degrees
            "heading": 180,  # Heading in degrees
            "x": 0,
            "y": 0,
            "z": 0,
        }

        while True:
            await asyncio.sleep(0.1)
            # Update data with random walk

            data["type"] = "location_update"
            data["altitude"] += random.uniform(-0.1, 0.1)
            data["latitude"] += random.uniform(-1, 1)
            data["longitude"] += random.uniform(-0.01, 0.01)
            data["heading"] += random.uniform(-1, 1)
            data["x"] = + random.uniform(-0.4, 0.4)
            data["y"] = + random.uniform(-0.4, 0.4)
            data["z"] = + random.uniform(-0.4, 0.4)
            # Ensure heading stays within 0-360 degrees
            data["heading"] %= 360

            # Post to websockets
            await websocket.send(json.dumps(data))
            print(f"> {data}")

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
