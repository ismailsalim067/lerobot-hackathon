import os
import time

from lerobot.robots.so_follower import (
    SO101Follower,
    SO101FollowerConfig,
)

from lerobot.teleoperators.so_leader import (
    SO101Leader,
    SO101LeaderConfig,
)

from lerobot.cameras.opencv import OpenCVCameraConfig


# Override with e.g. `FOLLOWER_PORT=/dev/tty.usbmodemXXXX python initiate_camera.py`
FOLLOWER_PORT = os.environ.get("FOLLOWER_PORT", "/dev/tty.usbmodem_follower")
LEADER_PORT = os.environ.get("LEADER_PORT", "/dev/tty.usbmodem_leader")

FOLLOWER_ID = "my_follower"
LEADER_ID = "my_leader"


# ==========================================
# CAMERA CONFIG
# ==========================================

while True:
    try:
        camera_index = int(input("Enter camera index: "))
        break
    except ValueError:
        print("Please enter a valid integer.")

cameras = {
    "front": OpenCVCameraConfig(
        index_or_path=camera_index,
        width=640,
        height=480,
        fps=30,
    )
}


# ==========================================
# FOLLOWER
# ==========================================

follower_config = SO101FollowerConfig(
    port=FOLLOWER_PORT,
    id=FOLLOWER_ID,
    cameras=cameras,
)

follower = SO101Follower(follower_config)


# ==========================================
# LEADER
# ==========================================

leader_config = SO101LeaderConfig(
    port=LEADER_PORT,
    id=LEADER_ID,
)

leader = SO101Leader(leader_config)


# ==========================================
# CONNECT
# ==========================================

print("Connecting follower + camera...")
follower.connect()

print("Connecting leader...")
leader.connect()

print("System ready")


# ==========================================
# CONTROL LOOP
# ==========================================

try:

    while True:

        # Leader position
        action = leader.get_action()

        # Move follower
        follower.send_action(action)

        # Get follower observation
        # This includes camera images
        observation = follower.get_observation()

        print(observation.keys())

        time.sleep(0.01)


except KeyboardInterrupt:
    print("Stopping...")


finally:

    if leader.is_connected:
        leader.disconnect()
    if follower.is_connected:
        follower.disconnect()
