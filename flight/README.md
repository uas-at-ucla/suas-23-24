
# uas-2024/flight
---
## Prerequisites
+ If you are on a Windows system, we recommend you to install [Windows Subsystem for Linux (WSL)](https://learn.microsoft.com/en-us/windows/wsl/install). You will be doing all your work inside the WSL terminal for this point on.
    + If you are on Windows 10 (not 11), then see https://github.com/uas-at-ucla/SUAS-Installs/tree/main#vcxsrv.
+ Ensure you have Python, [Git](https://git-scm.com/downloads), and [Docker](https://docs.docker.com/get-docker/) installed.
+ Install the python requirements by navigating to this folder and running `pip3 install -r requirements.txt`.
+ Clone the repository by running `git clone https://github.com/uas-at-ucla/uas-2024` in your terminal.

## Dronekit
Dronekit is the python library we will use to send commands to the drone. To install run:
```bash
git clone https://github.com/dronekit/dronekit-python
cd dronekit-python
sudo python setup.py install
```

## ArduPlane
In your terminal, navigate to the `/flight` directory and run:
```bash
git clone --recurse-submodules https://github.com/ArduPilot/ardupilot.git
```
Then navigate to the `ardupilot` directory and replace the `Dockerfile` with the one [here](https://gist.github.com/nathanchan631/b11d6706369ad092583bde1704ac10fb).

## Gazebo (optional)
+ For Linux/WSL systems, we have provided a script for you [here](https://github.com/uas-at-ucla/SUAS-Installs/blob/main/gazebo_install.sh), which you should put in the `/flight` directory and run using `bash gazebo_install.sh`.
+ For macOS, a script is in progress. For now, see the [Gazebo Docs](https://gazebosim.org/docs/all/getstarted) for installation instructions. You will also have to install the [Gazebo Plugin for Ardupilot](https://github.com/ArduPilot/ardupilot_gazebo).

### Building and Running the SITL (Simulation in The Loop)
##### With Gazebo:

Start Ardupilot with:
```bash
bash run_sim.sh
```
You can then start the simulation with:
```bash
gz sim -v4 -r iris_runway.sdf
```

##### Without Gazebo:
Start Ardupilot with:
```bash
bash run_sim.sh -gz false
```

### Test Installation
In a terminal window separate from where the simulation is running, navigate to this directory and run:
```bash
python mission_basic.py --connect=tcp:127.0.0.1:5762
```
After taking a minute to connect, the drone should fly around on the map and information should be printed to the console. If you are running Gazebo, the drone should move around there as well.
