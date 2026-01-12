from pymongo import MongoClient
from config import MONGO_URI

class EventStore:
    def __init__(self, uri=MONGO_URI):
        self.client = MongoClient(uri)
        self.db = self.client["smart_surveillance"]
        self.collection = self.db["events"]

    def save_alert(self, alert_event):
        """
        alert_event: dict
        """
        self.collection.insert_one(alert_event)

    def get_events(self, source_id=None, limit=50):
        query = {}
        if source_id is not None:
            query["source_id"] = source_id

        return list(
            self.collection.find(query, {"_id": 0})
            .sort("timestamp", -1)
            .limit(limit)
        )
        
        
    def close(self):
    	self.client.close()


