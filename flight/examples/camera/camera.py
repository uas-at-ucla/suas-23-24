#!/usr/bin/env python3

import asyncio

import cv2

from mavsdk import System
from mavsdk.mission import MissionItem, MissionPlan
from vision import Video
import os


async def run():
    drone = System()
    video = Video()

    os.makedirs("data/temp", exist_ok=True)

    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    print_mission_progress_task = asyncio.ensure_future(
        print_mission_progress(drone))

    running_tasks = [print_mission_progress_task]
    termination_task = asyncio.ensure_future(
        observe_is_in_air(drone, running_tasks))

    mission_items = []
    mission_items.append(
        MissionItem(
            47.398039859999997,
            8.5455725400000002,
            25,
            10,
            True,
            float("nan"),
            float("nan"),
            MissionItem.CameraAction.NONE,
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
            float("nan"),
        )
    )

    mission_plan = MissionPlan(mission_items)

    await drone.mission.set_return_to_launch_after_mission(True)

    print("-- Uploading mission")
    await drone.mission.upload_mission(mission_plan)

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position estimate OK")
            break

    print("-- Arming")
    await drone.action.arm()

    print("-- Starting mission")
    await drone.mission.start_mission()

    await mission_complete(drone, 1)

    while not video.frame_available():
        continue

    frame = video.frame()
    string = "data/temp/image.jpg"
    cv2.imwrite(string, frame)
    print("Success write image")

    await termination_task


async def print_mission_progress(drone):
    async for mission_progress in drone.mission.mission_progress():
        print(
            f"Mission progress: "
            f"{mission_progress.current}/"
            f"{mission_progress.total}"
        )


async def mission_complete(drone, task_id):
    async for mission_progress in drone.mission.mission_progress():
        if mission_progress.current == task_id:
            return


async def observe_is_in_air(drone, running_tasks):
    """Monitors whether the drone is flying or not and
    returns after landing"""

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            for task in running_tasks:
                task.cancel()
                try:
                    await task
                except asyncio.CancelledError:
                    pass
            await asyncio.get_event_loop().shutdown_asyncgens()

            return


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
