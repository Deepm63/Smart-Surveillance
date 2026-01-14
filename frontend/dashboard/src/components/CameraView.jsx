export default function CameraView({ sourceId }) {
  return (
    <div className="bg-black rounded-lg overflow-hidden">
      <img
        src={`http://localhost:5000/video/${sourceId}`}
        className="w-full"
      />
    </div>
  );
}

