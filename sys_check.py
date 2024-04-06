"""
https://github.com/NVIDIA-AI-IOT/jetson_benchmarks/blob/c029c7de35d69fd85e10b624b4908b6de10194b0/utils/utilities.py
"""

import os
import subprocess
FNULL = open(os.devnull, 'w')


def is_jetson():
    if os.path.isfile('/sys/firmware/devicetree/base/model'):
        with open('/sys/firmware/devicetree/base/model', 'r') as f:
            return 'jetson' in f.read().lower()
    return False


def set_power_mode(power_mode):
    power_cmd0 = 'nvpmodel'
    power_cmd1 = str('-m'+str(power_mode))
    subprocess.call('sudo {} {}'.format(power_cmd0, power_cmd1), shell=True,
                    stdout=FNULL)
    print('Setting Jetson Orin Nano in max performance mode')


def clear_ram_space():
    cmd_0 = str("sh" + " " + "-c")
    cmd_1 = str("'echo") + " " + "2" + " " + " >" + " " + \
        "/proc/sys/vm/drop_caches'"
    cmd = cmd_0 + " " + cmd_1
    subprocess.call('sudo {}'.format(cmd), shell=True)


def set_jetson_clocks():
    clocks_cmd = 'jetson_clocks'
    subprocess.call('sudo {}'.format(clocks_cmd), shell=True,
                    stdout=FNULL)
    print("Jetson clocks are Set")


def main():
    if is_jetson():
        print("Running on a Jetson Device - Performing System Check")
        set_power_mode(0)
        clear_ram_space()
        set_jetson_clocks()
    else:
        print("Not Running on a Jetson Device - Skipping System Check")


if __name__ == "__main__":
    main()
