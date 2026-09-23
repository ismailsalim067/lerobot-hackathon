"""
Recording script for the shape-sort task.
Update the placeholders below before running.
"""

import os
import subprocess

# --- Ports (from lerobot-find-port output) ---
FOLLOWER_PORT = os.environ.get("FOLLOWER_PORT", "TODO")
LEADER_PORT = os.environ.get("LEADER_PORT", "TODO")

# --- Arm IDs (should match calibration) ---
FOLLOWER_ID = "my_follower_arm"
LEADER_ID = "my_leader_arm"

# --- Cameras: update indices once confirmed via detect_cameras.py/snapshot_cameras.py ---
CAMERAS = '{"front": {"type": "opencv", "index_or_path": 0}, "overhead": {"type": "opencv", "index_or_path": 1}}'

# --- Dataset settings ---
DATASET_REPO_ID = "TODO/shape-sort-arm"   
NUM_EPISODES = 3                           # start small to test, raise to ~30 for the real run
TASK_DESCRIPTION = "Pick up the shape and place it in the matching hole"

cmd = [
    "lerobot-record",
    "--robot.type=so101_follower",
    f"--robot.port={FOLLOWER_PORT}",
    f"--robot.id={FOLLOWER_ID}",
    f"--robot.cameras={CAMERAS}",
    "--teleop.type=so101_leader",
    f"--teleop.port={LEADER_PORT}",
    f"--teleop.id={LEADER_ID}",
    f"--dataset.repo_id={DATASET_REPO_ID}",
    f"--dataset.num_episodes={NUM_EPISODES}",
    f"--dataset.single_task={TASK_DESCRIPTION}",
]

print("Running:", " ".join(cmd))
subprocess.run(cmd, check=True)