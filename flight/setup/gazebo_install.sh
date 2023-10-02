# Gazebo Garden
sudo apt-get update
sudo apt-get install lsb-release wget gnupg
sudo wget https://packages.osrfoundation.org/gazebo.gpg -O /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null
sudo apt-get update
sudo apt-get install gz-garden

# Plugin for Gazebo Garden
sudo apt update
sudo apt install libgz-sim7-dev rapidjson-dev
CUR_LOC="$(pwd)"
mkdir -p gz_ws/src && cd gz_ws/src
git clone https://github.com/ArduPilot/ardupilot_gazebo
cd ardupilot_gazebo
mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=RelWithDebInfo
make -j4

echo "export GZ_SIM_SYSTEM_PLUGIN_PATH=${CUR_LOC}/gz_ws/src/ardupilot_gazebo/build:\${GZ_SIM_SYSTEM_PLUGIN_PATH}" >> ~/.bashrc
echo "export GZ_SIM_RESOURCE_PATH=${CUR_LOC}/gz_ws/src/ardupilot_gazebo/models:${CUR_LOC}/gz_ws/src/ardupilot_gazebo/worlds:\${GZ_SIM_RESOURCE_PATH}" >> ~/.bashrc
source ~/.bashrc
