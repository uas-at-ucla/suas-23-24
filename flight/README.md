
# uas-2024/flight
---
### Prerequisites
+ If you are on a Windows system, you will have to either (1) *dual-boot Linux!!!!* or (2) install [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install).
+ Ensure you have Python and [Git](https://git-scm.com/downloads) installed.
+ Install the python requirements by navigating to this folder and running `pip3 install -r requirements.txt`.
+ Clone the repository by running `git clone https://github.com/uas-at-ucla/uas-2024` in your terminal.

### PX4 Autopilot
PX4 is the autopilot controller for the drone. Below are the installation links for each OS:
+ [Mac](https://docs.px4.io/main/en/dev_setup/dev_env_mac.html)
+ [Windows](https://docs.px4.io/main/en/dev_setup/dev_env_windows_wsl.html) (Skip the "Flashing" section at the bottom)
+ [Linux](https://docs.px4.io/main/en/dev_setup/building_px4.html) (Only the "Simulation and NuttX (Pixhawk) Targets" section)

### QGroundControl
QGroundControl is our Ground Control Station (GCS). You can install it [here](https://docs.qgroundcontrol.com/master/en/getting_started/download_and_install.html).
Note that Windows users should have installed this in the previous step.

### MAVSDK
MAVSDK is the Python library used to communicate with the autopilot system. Install it with:
```bash
pip3 install mavsdk
```

### Test Installation
First, start QGroundControl. Then navigate to the `PX4-Autopilot` directory, and run one of the following commands based on which simulation environment you want to use:
+ Gazebo: `make px4_sitl gz_x500`
+ Gazebo Classic: `make px4_sitl gazebo-classic`
+ jMAVSim (Use this one if none of the above worked): `make px4_sitl jmavsim`

You should see a simulation window appear, as well as the drone appear in QGroundControl.
Then, navigate to this directory (`/flight`) and run:
```bash
python example_mission.py
```
The drone should move around in both the simulation window and QGroundControl.
