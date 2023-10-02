# uas-2024/flight
Instructions and scripts for installing 'stuff' for SUAS flight

## Python3.9
---
Note: If you already have a  newer version of python installed, see [pyenv](https://github.com/pyenv/pyenv).
### **Install python3.9 on Linux (Ubuntu)**
Run the following script in terminal
```bash
sudo apt install python3
```
### **Install python3.9 on Windows**
Go to https://www.python.org/downloads/, then download and install python 3.9.13. 

i.e. 
1. Look for python 3.9.13
2. click download
3. choose the installer that matches your machine specs
4. download it
5. run installation
6. complete installation.
### **Install python3.9 on MacOS**
Install homebrew (the package manager, not a coffee preparation heuristic) by running the following script in your terminal
``` bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Then, restart your terminal and run the following script
``` bash
brew install python3
brew install pyenv
pyenv install 3.9.13
```
## ArduPlane
---
#### **Linux**
Navigate to this folder in your command window, then run `bash setup/ubuntu_ardupilot_install.sh`.
#### **MAC**
**[WIP]**
Instructions for OSX can be found on the Ardupilot documentation [here](https://ardupilot.org/dev/docs/building-setup-mac.html#building-setup-mac).
### **Windows**
**[WIP]**
Instructions for Windows users can be found on the Ardupilot documentation [here](https://ardupilot.org/dev/docs/building-setup-windows.html#building-setup-windows).

## Gazebo (optional)
Navigate to this folder in your command window, then run `bash setup/gazebo_install.sh`.
Note: For windows users, run this command inside wsl.


