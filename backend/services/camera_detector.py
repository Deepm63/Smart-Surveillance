import cv2

def detect_cameras(max_devices=5):
    cameras = []

    for i in range(max_devices):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            cameras.append({
                "id": i,
                "name": f"Camera {i}",
                "path": i
            })
            cap.release()

    return cameras

