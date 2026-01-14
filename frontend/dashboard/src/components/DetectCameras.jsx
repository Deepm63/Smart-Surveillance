import { useState } from "react";
import { detectCameras, addCamera } from "../api/cameras";

export default function DetectCameras({ onAdded }) {
  const [cams, setCams] = useState([]);
  const [names, setNames] = useState({});

  const handleDetect = async () => {
    const list = await detectCameras();
    setCams(list);
  };

  const handleAdd = async (cam) => {
    await addCamera({
      path: cam.path,
      name: names[cam.id]
    });
    onAdded();
  };

  return (
    <div className="bg-slate-800 rounded-lg p-3">
      <button
        onClick={handleDetect}
        className="w-full bg-blue-600 rounded p-2 mb-3"
      >
        Detect Cameras
      </button>

      {cams.map(cam => (
        <div key={cam.id} className="mb-2 space-y-1">
          <input
            placeholder="Camera name (e.g. Parking Gate)"
            className="w-full p-1 text-sm bg-slate-700 rounded"
            onChange={(e) =>
              setNames({ ...names, [cam.id]: e.target.value })
            }
          />
          <button
            onClick={() => handleAdd(cam)}
            className="w-full bg-green-600 rounded p-1 text-xs"
          >
            Add Camera {cam.id}
          </button>
        </div>
      ))}
    </div>
  );
}

