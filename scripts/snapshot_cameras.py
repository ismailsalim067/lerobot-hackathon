import cv2
import sys

indices = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [0, 1]

for i in indices:
    cap = cv2.VideoCapture(i)
    ret, frame = cap.read()
    if ret:
        cv2.imwrite(f"test_cam_{i}.jpg", frame)
        print(f"Saved test_cam_{i}.jpg")
    else:
        print(f"Camera {i} failed to capture")
    cap.release()