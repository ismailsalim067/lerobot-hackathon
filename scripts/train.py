"""
Draft training script for the shape-sort task.
Fill in DATASET_REPO_ID once Person 1 finishes recording and pushes the dataset.
"""

import subprocess

# TODO: update once dataset is recorded and pushed to the Hub
# current has placeholders

DATASET_REPO_ID = "TODO/shape-sort-arm"
POLICY_TYPE = "act"
OUTPUT_DIR = "outputs/train/shape_sort"
JOB_NAME = "shape_sort_run1"

cmd = [
    "lerobot-train",
    f"--dataset.repo_id={DATASET_REPO_ID}",
    f"--policy.type={POLICY_TYPE}",
    f"--output_dir={OUTPUT_DIR}",
    f"--job_name={JOB_NAME}",
    "--policy.device=cuda",
    "--wandb.enable=false",
]

print("Running:", " ".join(cmd))
subprocess.run(cmd, check=True)