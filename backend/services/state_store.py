import redis
import json
import time
from config import REDIS_TTL

class StateStore:
    def __init__(self, host="localhost", port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)

    def update_camera_state(self, source_id, person_count, alert_active):
        key = f"camera:{source_id}:state"
        value = {
            "person_count": person_count,
            "alert_active": alert_active,
            "last_updated": time.time()
        }
        self.redis.set(key, json.dumps(value))

    def get_camera_state(self, source_id):
        key = f"camera:{source_id}:state"
        data = self.redis.get(key)
        return json.loads(data) if data else None
        
    def close(self):
    	self.redis.close()
    def update_camera_state(self, source_id, person_count, alert_active):
    	key = f"camera:{source_id}:state"
    	value = {
    	    "person_count": person_count,
    	    "alert_active": alert_active,
    	    "last_updated": time.time()
    	}
    	self.redis.set(key, json.dumps(value), ex=REDIS_TTL)  # 10s TTL



