import subprocess
import signal

# This script executes shell commands to add an exeternal
# usb camera to be usable by OpenCV on an Ubuntu machine.

# Must run this sudo command every fresh computer startup
# sudo modprobe v4l2loopback
"""
modprobe_command = [
    'sudo',
    'modprobe',
    'v4l2loopback'
]
"""
gphoto2_command = ["gphoto2", "--stdout", "--capture-movie"]

# Define the ffmpeg command to convert and stream to /dev/video4
ffmpeg_command = [
    "ffmpeg",
    "-i",
    "-",  # Input from stdin
    "-vcodec",
    "rawvideo",
    "-pix_fmt",
    "yuv420p",
    "-threads",
    "0",
    "-f",
    "v4l2",
    "/dev/video4",
]

# Run modprobe command
# modprobe_command = subprocess.Popen(modprobe_command)

# Start gphoto process to capture video
gphoto2_process = subprocess.Popen(gphoto2_command, stdout=subprocess.PIPE)


# Start ffmpeg process to convert and stream to v4l2loopback
ffmpeg_process = subprocess.Popen(ffmpeg_command, stdin=gphoto2_process.stdout)


# When sent a SIGINT (Control + C) Error, terminate everything and exit
def signal_handler(sig, frame):
    gphoto2_process.send_signal(signal.SIGINT)
    ffmpeg_process.send_signal(signal.SIGINT)
    gphoto2_process.terminate()
    ffmpeg_process.terminate()
    exit(0)


signal.signal(signal.SIGINT, signal_handler)


# Continue using camera until program terminated
while True:
    continue
