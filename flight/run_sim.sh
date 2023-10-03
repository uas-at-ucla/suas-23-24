#!/bin/bash

cd ardupilot

# Default values
use_gz=true

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case "$1" in
    -gz|--gz)
      use_gz="${2:-true}"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Build Docker image
docker build . -t ardupilot

# Determine the value of the -f flag based on the use_gz variable
gz_flag=""
if [ "$use_gz" == true ]; then
  gz_flag="-f gazebo-iris"
fi

# Run Docker container
docker run -e DISPLAY=$DISPLAY --rm -it --net=host -v "$(pwd)":/ardupilot ardupilot:latest sh -c "cd ArduCopter; sim_vehicle.py -v ArduCopter $gz_flag --model JSON --map --console"
