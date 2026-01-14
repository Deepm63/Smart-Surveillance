import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getSources } from "../api/sources";

import SourceList from "../components/SourceList";
import UploadVideo from "../components/UploadVideo";
import CameraView from "../components/CameraView";
import StatusBadge from "../components/StatusBadge";
import AlertPanel from "../components/AlertPanel";
import DetectCameras from "../components/DetectCameras";

export default function Dashboard() {
  const [sources, setSources] = useState([]);
  const [active, setActive] = useState(null);

  const refresh = async () => {
  try {
    const data = await getSources();
    setSources(data);

    // Reset active source if it no longer exists
    if (active !== null && !data.find(s => s.id === active)) {
      setActive(null);
    }
  } catch (e) {
    console.error("Refresh failed", e);
  }
};

  useEffect(() => {
    refresh();
  }, []);

  return (
    <div className="p-4 space-y-4">

      {/* ================= TOP NAVIGATION ================= */}
      <div className="flex gap-6 text-sm font-medium">
        <Link
          to="/"
          className="text-blue-400 hover:underline"
        >
          Dashboard
        </Link>

        <Link
          to="/analytics"
          className="text-blue-400 hover:underline"
        >
          Analytics
        </Link>
      </div>

      {/* ================= MAIN GRID ================= */}
      <div className="grid grid-cols-1 xl:grid-cols-5 gap-4">

        {/* -------- Sidebar -------- */}
        <div className="xl:col-span-1 space-y-4">
          <DetectCameras onAdded={refresh} />

          <UploadVideo onUploaded={refresh} />

          <SourceList
            sources={sources}
            active={active}
            onSelect={setActive}
            onRemoved={() => {
              setActive(null);
              refresh();
            }}
          />
        </div>

        {/* -------- Video + Status -------- */}
        <div className="xl:col-span-3 space-y-4">
          {active !== null && <CameraView sourceId={active} />}
          {active !== null && <StatusBadge sourceId={active} />}
        </div>

        {/* -------- Alerts -------- */}
        <div className="xl:col-span-1">
          {active !== null && <AlertPanel sourceId={active} />}
        </div>

      </div>
    </div>
  );
}

