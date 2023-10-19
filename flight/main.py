import asyncio
import os
import shutil

from mavsdk import System


OUTPUT_IMAGE_DIRECTORY = "../vision/images/odlc"


async def run():

    print("Starting flight software")

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