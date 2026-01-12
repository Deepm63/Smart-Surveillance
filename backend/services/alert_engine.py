import time
from config import COOLDOWN_SEC, THRESHOLD

class AlertEngine:
    def __init__(self):
        self.last_alert_time = {}

    def evaluate(self, source_id, detections):
        """
        Returns:
        - alerts: list of alert events (cooldown-based)
        - violating_boxes: list of boxes that violate rules (continuous)
        """
        alerts = []
        violating_boxes = []

        # ---- RULE: Person count ----
        persons = [d for d in detections if d[0] == "person"]
        person_count = len(persons)


        now = time.time()
        last_time = self.last_alert_time.get(source_id, 0)

        # --- STATE: violating boxes (NO cooldown) ---
        if person_count > THRESHOLD:
            violating_boxes = [p[2] for p in persons]

        # --- EVENT: alert text (WITH cooldown) ---
        if person_count > THRESHOLD and (now - last_time) > COOLDOWN_SEC:
            alerts.append({
                "type": "PERSON_COUNT",
                "message": f"PERSON COUNT EXCEEDED ({person_count})",
                "timestamp": now
            })
            self.last_alert_time[source_id] = now

        return alerts, violating_boxes

