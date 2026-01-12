from video_sources.camera import CameraSource

class SourceManager:
    def __init__(self):
        self.sources = {}
        self.next_id = 0

    def add_source(self, source_path):
        source_id = self.next_id
        self.sources[source_id] = CameraSource(source_path)
        self.next_id += 1
        return source_id

    def get_source(self, source_id):
        return self.sources.get(source_id)

    def remove_source(self, source_id):
        camera = self.sources.pop(source_id, None)
        if camera:
            camera.release()
            
    def list_sources(self):
    	return list(self.sources.keys())
    
    def shutdown(self):
    	for cam in self.sources.values():
            cam.release()

