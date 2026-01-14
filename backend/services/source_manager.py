"""from video_sources.camera import CameraSource


class SourceManager:
    def __init__(self):
        self.sources = {}
        self.meta = {}
        self.counter = 0

    def add_source(self, path, source_type="camera"):
        source_id = self.counter
        self.counter += 1

        # Create camera/video source
        self.sources[source_id] = CameraSource(path)

        # Metadata for frontend
        self.meta[source_id] = {
            "id": source_id,
            "type": source_type,   # "camera" or "video"
            "path": str(path),
            "active": True
        }

        return source_id

    def get_source(self, source_id):
        return self.sources.get(source_id)

    def remove_source(self, source_id):
        if source_id in self.sources:
            self.sources[source_id].release()
            del self.sources[source_id]
            del self.meta[source_id]

    def list_sources(self):
        return list(self.meta.values())

    def shutdown(self):
        for cam in self.sources.values():
            cam.release()

"""
from video_sources.camera import CameraSource

class SourceManager:
    def __init__(self):
        self.sources = {}
        self.meta = {}
        self.counter = 0

    def add_source(self, path, source_type="camera", name=None):
        source_id = self.counter
        self.counter += 1

        self.sources[source_id] = CameraSource(path)

        self.meta[source_id] = {
            "id": source_id,
            "name": name.strip() if isinstance(name, str) and name.strip()
        else f"{source_type.capitalize()} {source_id}",

            "type": source_type,     # camera | video
            "path": str(path),
            "active": True
        }

        return source_id

    def get_source(self, source_id):
        return self.sources.get(source_id)

    def remove_source(self, source_id):
        if source_id in self.sources:
            self.sources[source_id].release()
            del self.sources[source_id]
            del self.meta[source_id]

    def list_sources(self):
        return list(self.meta.values())

    def shutdown(self):
        for cam in self.sources.values():
            cam.release()

