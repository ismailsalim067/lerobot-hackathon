# lerobot-hackathon

# Shape-Sorting VLA: Data Collection Guide

**Goal:** Train the follower arm to place blocks into three boxes according to shape, regardless of size or color. The leader arm is used to demonstrate the task.

## 1. What to prepare

- SO-101 leader and follower arms, firmly mounted.
- Correct power supplies: **5V for the leader; 12V for the follower**, following their labels.
- Both arm USB data cables connected to the recording computer.
- UGREEN camera and wrist camera, connected to that same computer.
- Three wide, low-sided boxes labeled **Cylinder**, **Triangle**, and **Rectangular Block**. Cubes and rectangular blocks share the third box.
- Blocks in different sizes that the gripper can reliably hold.
- A clear workspace with steady lighting.
- A LeRobot recording setup that saves synchronized camera images, robot states, and action commands. **The camera snapshot scripts alone are insufficient.**

Keep box positions and camera mounting unchanged between recording and evaluation.

## 2. Which camera to use

**Record both cameras simultaneously.**

| Camera | Placement | What must be visible |
|---|---|---|
| UGREEN — scene view | Fixed above and at an angle to the table | Entire pickup area, all three boxes, and the working gripper |
| Wrist camera — close-up view | Mounted near the follower’s gripper | Gripper opening and the block during approach and grasping |

Use consistent camera names, such as `scene` and `wrist`. Confirm the actual views before recording; USB camera indices can change after reconnection.

## 3. What action to record

Start with **one block on the table per episode**.

1. Put the follower in a consistent starting position.
2. Place a block in the pickup area, then remove your hands.
3. Start recording.
4. Use the leader arm to demonstrate:
   - Approach the block.
   - Grasp it.
   - Lift it clear of the table.
   - Move it over the correct box.
   - Lower it and release it inside.
   - Move the gripper away and return to the starting position.
5. Stop recording before resetting the scene.

Use smooth, deliberate movements. Keep failed grasps, drops, wrong-box placements, and hand-assisted attempts separate from the initial successful-demonstration dataset.

Use the same task instruction:

> Sort the block by shape into the corresponding bin, regardless of its size or color.

## 4. What variety to include

**First record five trial episodes and inspect them.** Then aim for approximately 150–180 successful single-block demonstrations as an initial collection budget, not a guarantee of performance.

Balance examples across:

- All three shape categories.
- Available sizes within each category.
- Different pickup positions and orientations.

Avoid making color predict the destination. Ideally, include different colors of each shape and the same color across different shapes.

Once single-block sorting works, add complete episodes containing **two or three blocks**, with varied arrangements and sorting orders.

## 5. Conditions to meet

**Before collecting the full dataset:**

- Both camera recordings are clear and continuous.
- Video, robot state, and action data are aligned in time.
- Every block is graspable and every box is reachable.
- Trial recordings contain the entire action, including release.
- Scene resets are excluded from recordings.

**A successful episode means:**

- The block ends fully inside the correct box.
- No drop outside the box or human assistance occurs.
- The gripper releases the block and withdraws successfully.

**Before calling the system autonomous:**

Test on new arrangements excluded from training. Record grasp success, correct-box placement, and complete-task success separately. A practical first milestone is **at least 18 successful attempts out of 20**, balanced across categories; this is a project target, not a safety certification.

For multi-block operation, also verify that it sorts every block and stops when finished. Keep an operator nearby with an accessible stop control during evaluation.
