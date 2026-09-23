**Run these steps in order: setup → identify hardware → record → train.** Use the same physical arms, and keep the Terminal open.

1. **Extract the package and install the environment.** Conda must already be installed.

```bash
cd ~/Downloads
tar -xzf so101_team_handoff_20260923.tar.gz
cd so101_team_handoff_20260923

# Run this installation command only once:
conda env create -n so101-handoff -f environment/environment.no-builds.yml

conda activate so101-handoff
bash restore_handoff.sh --apply
```

2. **Get the Leader and Follower IDs from the calibration filenames.**

```bash
find calibration -name 'haoyu_so101_*.json'
```

The filename without `.json` is the ID. These are already known and must stay unchanged:

- Leader ID: `haoyu_so101_leader`
- Follower ID: `haoyu_so101_follower`

3. **Find each arm’s USB port.**

```bash
lerobot-find-port
```

On the **first run**, unplug only the **Leader’s USB cable** when prompted, then press Enter. Copy the reported `/dev/tty.usbmodem...` path and reconnect it.

Run the same command again for the **Follower**, unplugging only its USB cable when prompted. Copy its port and reconnect it. [Port discovery instructions](https://huggingface.co/docs/lerobot/so101)

4. **Find the camera indices.**

```bash
lerobot-find-cameras opencv
open outputs/captured_images
```

Match the captured images to the cameras:

- The view from the Follower’s wrist → `WRIST_INDEX`.
- The external view → `EXTERNAL_INDEX`.

Use the integer indices reported by the tool. **Do not assume they are still 0 and 1.** [Camera instructions](https://huggingface.co/docs/lerobot/cameras)

5. **Enter the four values you just found.**

Replace every `REPLACE_...` below, then paste the whole block:

```bash
LEADER_PORT='REPLACE_LEADER_PORT'
FOLLOWER_PORT='REPLACE_FOLLOWER_PORT'
WRIST_INDEX='REPLACE_WITH_INTEGER'
EXTERNAL_INDEX='REPLACE_WITH_INTEGER'

CAMERAS="{wrist: {type: opencv, index_or_path: $WRIST_INDEX, width: 640, height: 480, fps: 30}, external: {type: opencv, index_or_path: $EXTERNAL_INDEX, width: 640, height: 480, fps: 30}}"

ARM_ARGS=(
  --robot.type=so101_follower
  "--robot.port=$FOLLOWER_PORT"
  --robot.id=haoyu_so101_follower
  "--robot.cameras=$CAMERAS"
  --teleop.type=so101_leader
  "--teleop.port=$LEADER_PORT"
  --teleop.id=haoyu_so101_leader
  --display_data=true
)
```

6. **Briefly test the arms and cameras.**

```bash
lerobot-teleoperate "${ARM_ARGS[@]}" --fps=30
```

Move the Leader gently and check that the Follower responds correctly. Check both camera views. Press **Ctrl+C** to finish the test.

7. **Create a new dataset ID and start recording.**

This generates a unique ID from the agreed base name and the current time. It saves the ID and folder path for the training step. **Recording stays local; no Hugging Face login is needed.**

```bash
DATASET_ID="Dan1el131/coffee-apple-grab_$(date +%Y%m%d_%H%M%S)"
DATASET_ROOT="$PWD/recordings/$DATASET_ID"

printf '%s\n' "$DATASET_ID" > latest_dataset_id.txt
printf '%s\n' "$DATASET_ROOT" > latest_dataset_root.txt

echo "Recording dataset: $DATASET_ID"

lerobot-record "${ARM_ARGS[@]}" \
  --dataset.repo_id="$DATASET_ID" \
  --dataset.root="$DATASET_ROOT" \
  --dataset.no_stamp=true \
  --dataset.fps=30 \
  --dataset.num_episodes=50 \
  --dataset.episode_time_s=60 \
  --dataset.reset_time_s=30 \
  --dataset.single_task="Put the coffee sachet in the cup and put the apple on the plate" \
  --dataset.streaming_encoding=true \
  --dataset.encoder_threads=2 \
  --dataset.push_to_hub=false
```

During recording: **`n` = next, `r` = rerecord, `q` = finish**. Wait until saving finishes and the Terminal prompt returns.

8. **Train ACT on the dataset you just recorded.**

The commands below read the saved dataset ID and path automatically:

```bash
DATASET_ID="$(cat latest_dataset_id.txt)"
DATASET_ROOT="$(cat latest_dataset_root.txt)"

echo "Training dataset: $DATASET_ID"

lerobot-train \
  --dataset.repo_id="$DATASET_ID" \
  --dataset.root="$DATASET_ROOT" \
  --dataset.video_backend=pyav \
  --policy.type=act \
  --policy.device=mps \
  --policy.push_to_hub=false \
  --output_dir="$PWD/outputs/act_$(date +%Y%m%d_%H%M%S)" \
  --job_name=act_coffee_apple \
  --batch_size=8 \
  --num_workers=0 \
  --steps=20000 \
  --wandb.enable=false
```

On an **Intel Mac**, replace `mps` with `cpu`. Training checkpoints will be saved under `outputs/act_.../checkpoints/`.
