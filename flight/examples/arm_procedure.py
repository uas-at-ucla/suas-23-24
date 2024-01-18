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
    print("Conencting to drone")
    drone = System()
    await drone.connect(system_address="udp://:14540")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    print("Checking for calibration status...")
    async for health in drone.telemetry.health():
        if not health.is_gyrometer_calibration_ok:
            print("Gyrometer requires calibration")
        if not health.is_accelerometer_calibration_ok:
            print("Accelerometer requires calibration")
        if not health.is_magnetometer_calibration_ok:
            print("Magnetometer requires calibration")
        break

    while not drone.telemetry.health_all_ok():
        print("Drone not ready to arm. Waiting for -")
        async for health in drone.telemetry.health():
            if not health.is_global_position_ok:
                print(" - GPS fix")
            if not health.is_local_position_ok:
                print(" - Local position estimate")
            if not health.is_home_position_ok:
                print(" - Home position to be set")
        break

    print("Arming now...")
    await drone.action.arm()
    print("Drone armed.")

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
