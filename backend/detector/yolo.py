"""
from ultralytics import YOLO
class YOLODetector:
    def __init__(self, model_path="yolov8n.pt"):
        self.model = YOLO(model_path)
        self.class_names = self.model.names

    def detect(self, frame, conf_threshold=0.4):
        results = self.model(frame, verbose=False)
        detections = []

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                conf = float(box.conf[0])
                if conf < conf_threshold:
                    continue

                cls_id = int(box.cls[0])
                cls_name = self.class_names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append((cls_name, conf, (x1, y1, x2, y2)))

        return detections
"""
from ultralytics import YOLO

class YOLODetector:
    def __init__(self, model_path="yolov8m.pt"):
        # Load YOLO ONCE
        self.model = YOLO(model_path)
        self.class_names = self.model.names

    def detect(self, frame, conf_threshold=0.35):
        results = self.model(frame, verbose=False)
        detections = []

        for r in results:
            if r.boxes is None:
                continue

            for box in r.boxes:
                conf = float(box.conf[0])
                if conf < conf_threshold:
                    continue

                cls_id = int(box.cls[0])
                cls_name = self.class_names[cls_id]
                x1, y1, x2, y2 = map(int, box.xyxy[0])

                detections.append((cls_name, conf, (x1, y1, x2, y2)))

        return detections

