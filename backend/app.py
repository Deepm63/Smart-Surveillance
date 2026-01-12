from flask import Flask, Response, request, jsonify, abort
import cv2

from detector.yolo import YOLODetector
from services.source_manager import SourceManager
from services.alert_engine import AlertEngine
from services.state_store import StateStore
from services.event_store import EventStore
from config import FRAME_SKIP, RESIZE_W, RESIZE_H


import signal
import sys

def shutdown_handler(sig, frame):
    print("Shutting down gracefully...")
    manager.shutdown()          # release cameras
    event_store.close()         # close Mongo
    state_store.close()         # close Redis
    sys.exit(0)

signal.signal(signal.SIGINT, shutdown_handler)
signal.signal(signal.SIGTERM, shutdown_handler)


app = Flask(__name__)

# ---------------- Core Singletons ----------------
manager = SourceManager()
detector = YOLODetector()
alert_engine = AlertEngine()
state_store = StateStore()
event_store = EventStore()


# -------------------------------------------------


# ------------------------------------------------------


def generate(camera, source_id):
    count = 0

    for frame in camera.frames():
        count += 1

        # ---- Frame skipping ----
        if count % FRAME_SKIP != 0:
            continue

        # ---- Frame resizing ----
        frame = cv2.resize(frame, (RESIZE_W, RESIZE_H))

        # ---- YOLO inference ----
        try:
            detections = detector.detect(frame)
        except Exception as e:
            print("YOLO error:", e)
            continue


        # ---- Alert evaluation ----
        alerts, violating_boxes = alert_engine.evaluate(source_id, detections)
        
        # ---- Compute state ----
        person_count = sum(1 for d in detections if d[0] == "person")
        alert_active = len(violating_boxes) > 0
        
        # ---- Update Redis state ----
        state_store.update_camera_state(
            source_id,
            person_count=person_count,
            alert_active=alert_active
        )    

        # ---- Log alert EVENTS (cooldown-based) ----
        for alert in alerts:
            print("ALERT:", alert)
            
            try:
            	event_store.save_alert({
                "source_id": source_id,
                "type": alert["type"],
                "message": alert["message"],
                "person_count": int(alert["message"].split("(")[-1][:-1]),
                "timestamp": alert["timestamp"]})
            except Exception as e:
            	print("Mongo write failed:",e)

        # ---- Draw bounding boxes ----
        for cls, conf, (x1, y1, x2, y2) in detections:
            box_tuple = (x1, y1, x2, y2)

            # RED if violating rule, else GREEN
            if box_tuple in violating_boxes:
                color = (0, 0, 255)
                label = f"{cls}:{conf:.2f} ALERT"
            else:
                color = (0, 255, 0)
                label = f"{cls}:{conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(
                frame,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                color,
                1
            )

        # ---- Text alert (cooldown-based only) ----
        for alert in alerts:
            cv2.putText(
                frame,
                alert["message"],
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        # ---- Encode & stream ----
        success, jpeg = cv2.imencode(".jpg", frame)
        if not success:
            continue

        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + jpeg.tobytes()
            + b"\r\n"
        )


# ---------------- API ROUTES ----------------

@app.route("/add_source", methods=["POST"])
def add_source():
    data = request.json
    if not data or "path" not in data:
        return jsonify({"error": "path required"}), 400

    source_id = manager.add_source(data["path"])
    return jsonify({"source_id": source_id})


@app.route("/video/<int:source_id>")
def video(source_id):
    camera = manager.get_source(source_id)
    if camera is None:
        abort(404)

    return Response(
        generate(camera, source_id),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )


@app.route("/remove_source/<int:source_id>", methods=["DELETE"])
def remove_source(source_id):
    camera = manager.get_source(source_id)
    if camera is None:
        return {"error": "source not found"}, 404

    manager.remove_source(source_id)
    return {"removed": source_id}


@app.route("/sources")
def list_sources():
    return {"sources": manager.list_sources()}


@app.route("/state/<int:source_id>")
def get_state(source_id):
    state = state_store.get_camera_state(source_id)
    if state is None:
        return {"error": "state not found"}, 404
    return state

@app.route("/events")
def get_events():
    source_id = request.args.get("source_id", type=int)
    limit = request.args.get("limit", default=50, type=int)

    events = event_store.get_events(source_id=source_id, limit=limit)
    return {"events": events}

# ------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)

