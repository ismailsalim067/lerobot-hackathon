# lerobot-hackathon

# Windows Camera & Calibration File Toolkit

English setup and diagnostics for a Windows teammate working with SO-101 cameras.

**Included:** a private Python environment, USB camera detection, multi-camera preview,
snapshots, camera labels, Windows COM-port inventory, and offline calibration JSON
validation/backup.

**Calibration scope:** this toolkit checks and backs up existing calibration files.
It does **not** perform physical arm calibration, apply calibration to motors, enable
torque, run teleoperation, or run a robot policy. Physical calibration and first-motion
checks belong to the on-site manufacturer's workflow. See [calibration handoff](docs/calibration.md).

## Start here on Windows

1. Download this repository as a ZIP and **extract it** into a normal local folder,
   for example `C:\Users\YourName\Projects\camera-kit`. Do not run it inside the ZIP.
2. Double-click **`01_setup.cmd`**. It looks for 64-bit Python 3.12. If missing,
   it offers to install Python for the current user using Windows Package Manager.
   You can instead install Python 3.12 yourself from [python.org](https://www.python.org/downloads/windows/).
3. Setup creates `.venv` in this folder and installs the pinned packages in
   `requirements.txt`. Internet access is required for setup. It does not change an
   existing Conda environment, install GPU packages, or install LeRobot.
4. Connect the USB camera(s), then double-click **`02_camera_tools.cmd`**.
5. Choose **3: Detect cameras**, then **4: Preview**. Enter only the indices you
   want to open. Confirm each camera by its picture; do not assume index 0 is the
   external camera. The laptop's built-in webcam may also be listed.
6. In the preview window, press **S** to save pictures or **Q / Esc** to close.
   For two cameras, enter two indices separated by a space. This opens both at once
   so you can check whether the USB hub can sustain both streams.
7. After identifying a view, use **6: Save a camera label**, such as `scene` or
   `wrist`. Detect and identify again after changing USB connections or backend.
8. For an existing calibration JSON, double-click **`03_check_calibration.cmd`**.

Allow camera access for the application when Windows asks. Under Windows 11, check
**Settings > Privacy & security > Camera > Camera access** and
**Let desktop apps access your camera** if access is blocked. See
[Microsoft's camera-permission guide](https://support.microsoft.com/en-us/windows/manage-app-permissions-for-your-camera-in-windows-87ebc757-1f87-7bbf-84b5-0686afb6ca6b).

## What gets connected

Each USB camera connects to the same Windows laptop, directly or through a data-capable
USB hub. A UGREEN webcam uses its own matching cable. The USB-A-to-small-white-connector
cable from the SO-101 kit is for a matching camera module; do not assume it fits the
UGREEN webcam. Camera power normally comes from USB. Do not connect a camera to the
arm's DC motor-power input.

This toolkit's camera functions do not need either arm's motor controller connected.
The COM-port menu only reads the operating system's device list; it does not open a
serial port or verify motor communication.

## Menu

| Item | Function |
|---|---|
| 1 | Check Python, OpenCV, NumPy and pyserial |
| 2 | List COM ports from OS metadata only |
| 3 | Probe indices 0 through 9; confirm a usable video frame |
| 4 | Preview one to four selected cameras; S saves frames |
| 5 | Save a snapshot from each selected camera |
| 6 | Give an identified camera a local label |
| 7 | Validate and optionally back up an existing calibration JSON |
| 8 | Export a local diagnostic report |
| 9 | Switch video backend; clears stale camera labels |

**Detection briefly opens the cameras being tested, including a built-in webcam.**
Detection does not save images. Snapshots are saved only when explicitly requested.
The toolkit does not capture audio, upload files, or contact a server after setup.

## Files on the Windows laptop

| Path | Contents |
|---|---|
| `.venv/` | This toolkit's Python environment |
| `local/setup.log` | Latest installation output |
| `local/camera_detection.json` | Detection results and backend used |
| `local/cameras.json` | User-assigned camera labels and requested capture settings |
| `local/snapshots/` | JPEG snapshots with unique filenames |
| `local/calibration_backups/` | Unmodified calibration files and validation reports |
| `local/diagnostics_*.json` | Diagnostic reports you can review and share |

`.venv/` and all of `local/` are ignored by Git. **Do not force-add them.**
No real calibration files, photographs, Mac paths, or machine-specific COM ports are
included in the distributed toolkit. A calibration backup is not installed into
LeRobot's calibration directory and is not applied to hardware.

## Camera debugging

Start with 640x480 at 30 requested FPS. Cameras may negotiate another resolution or
frame rate; detection reports the returned frame size. Reported camera FPS can be
inaccurate, and the preview's display FPS is not a synchronization guarantee.

If detection finds nothing:

- Close other camera users, such as Teams, Zoom, OBS or the Windows Camera app.
- Check camera privacy permissions and the lens shutter/protective film.
- Try the camera directly in the laptop, or another data-capable USB port/cable.
- Try menu 9 to switch from `dshow` to `msmf`, then detect again.
- If the device might be above index 9, use the advanced detection command below.

If each camera works alone but not together, test a lower requested resolution/frame
rate and a different USB connection. Separate snapshot files are taken sequentially;
they are **not** a synchronized robot-training dataset.

If OpenCV reports `DLL load failed`, consult the [OpenCV package troubleshooting notes](https://pypi.org/project/opencv-python/4.12.0.88/).
Windows N/KN may need the Media Feature Pack; the Visual C++ runtime may also be required.
If no preview window can be created, make sure this environment has `opencv-python`,
not a conflicting `opencv-python-headless` or `opencv-contrib-python` installation.

If a driver freezes during detection, the probe is stopped after 15 seconds and the
tool moves on. If a preview freezes, return to its terminal and press **Ctrl+C**.

## Advanced camera-only commands

Run these from PowerShell in the extracted toolkit folder. The example indices are
placeholders: replace them with indices you have identified on this Windows laptop.

```powershell
.\.venv\Scripts\python.exe kit.py doctor
.\.venv\Scripts\python.exe kit.py ports
.\.venv\Scripts\python.exe kit.py detect --max-index 15 --backend dshow
.\.venv\Scripts\python.exe kit.py preview --indices 1 2 --backend dshow
.\.venv\Scripts\python.exe kit.py preview --indices 1 --width 1280 --height 720 --fps 15
.\.venv\Scripts\python.exe kit.py snapshot --indices 1 2
.\.venv\Scripts\python.exe kit.py report
```

The teammate's familiar script names are also available:

```powershell
.\.venv\Scripts\python.exe detect_cameras.py
.\.venv\Scripts\python.exe snapshot_cameras.py 1 2
```

These are expanded replacements for the supplied short scripts. Detection now checks
for real frames and isolates potentially hanging drivers. Snapshot indices must be
chosen explicitly instead of assuming that 0 and 1 are the desired cameras.
