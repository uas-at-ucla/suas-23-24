import asyncio
from dronekit import connect, VehicleMode
import websockets
import json

async def connect_vehicle():
    vehicle = connect("/dev/tty.usbmodem01")
    print("Connected to vehicle")
    return vehicle

async def arm_and_takeoff(vehicle, aTargetAltitude):
    """
    Arms vehicle and fly to aTargetAltitude.
    """
    print("Basic pre-arm checks")
    # Don't try to arm until autopilot is ready
    while not vehicle.is_armable:
        print(" Waiting for vehicle to initialise...")
        await asyncio.sleep(1)

    print("Arming motors")
    # Copter should arm in GUIDED mode
    vehicle.mode = VehicleMode("GUIDED")
    vehicle.armed = True

    # Confirm vehicle armed before attempting to take off
    while not vehicle.armed:
        print(" Waiting for arming...")
        await asyncio.sleep(1)

    print("Vehicle is now armed.")
    print("Taking off to a target altitude of", aTargetAltitude)
    vehicle.simple_takeoff(aTargetAltitude)

async def post_orientation_and_gps(vehicle):
    async with websockets.connect('ws://localhost:8001') as ws:
        while True:
            position = vehicle.location.global_frame
            print(vehicle.velocity)
            attitude = vehicle.attitude
            payload = {
                "orientation": {
                    "pitch": attitude.pitch,
                    "roll": attitude.roll,
                    "yaw": attitude.yaw
                },
                "GPS": {
                    "lat": position.lat,
                    "lon": position.lon,
                    "alt": position.alt
                },
                "barometric_altitude": position.alt,
                "battery": 0,
                "type": "attitude"
            }
            await ws.send(json.dumps(payload))
            await asyncio.sleep(0.01)  # Adjust the sleep time as needed

async def main():
    vehicle = await connect_vehicle()
    print(1)
    await asyncio.gather(
        arm_and_takeoff(vehicle, 10),
        post_orientation_and_gps(vehicle),
    )
# Run the main function
asyncio.run(main())
