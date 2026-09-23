import cv2

print("Checking which camera indices are active:")
for i in range(4):
    cap = cv2.VideoCapture(i)
    print(i, cap.isOpened())
    cap.release()