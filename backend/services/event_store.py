from pymongo import MongoClient
from config import MONGO_URI
import time


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

    def count_alerts_by_source(self):
        pipeline = [
            {"$group": {"_id": "$source_id", "count": {"$sum": 1}}},
            {"$sort": {"count": -1}}
        ]
        return list(self.collection.aggregate(pipeline))

    def count_alerts_over_time(self, hours=24):
        since = time.time() - hours * 3600

        pipeline = [
            {"$match": {"timestamp": {"$gte": since}}},
            {
                "$group": {
                    "_id": {
                        "hour": {
                            "$hour": {
                                "$toDate": {
                                    "$multiply": ["$timestamp", 1000]
                                }
                            }
                        }
                    },
                    "count": {"$sum": 1}
                }
            },
            {"$sort": {"_id.hour": 1}}
        ]
        return list(self.collection.aggregate(pipeline))

    def close(self):
        self.client.close()

