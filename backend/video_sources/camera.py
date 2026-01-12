import cv2
import time

class CameraSource:
    def __init__(self, source):
        self.source = source
        self.cap = cv2.VideoCapture(source)

        if not self.cap.isOpened():
            raise RuntimeError("Could not open video source: {source}")

        # Get FPS for file sources (fallback to 25)
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        if self.fps == 0 or self.fps is None:
            self.fps = 25

        self.delay = 1 / self.fps

    def frames(self):
        while True:
            ret, frame = self.cap.read()

            # If video ends, restart it
            if not ret:
                self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                continue

            time.sleep(self.delay)
            yield frame

    def release(self):
        self.cap.release()

