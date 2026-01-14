import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { alertsBySource, alertsOverTime } from "../api/analytics";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  LineChart,
  Line,
  ResponsiveContainer
} from "recharts";

export default function Analytics() {
  const [bySource, setBySource] = useState([]);
  const [overTime, setOverTime] = useState([]);

  useEffect(() => {
    alertsBySource().then(setBySource);
    alertsOverTime(24).then(setOverTime);
  }, []);

  return (
    <div className="p-6 space-y-6">

      {/* ===== TOP NAVIGATION ===== */}
      <div className="flex items-center gap-4 text-sm font-medium">
        <Link
          to="/"
          className="text-blue-400 hover:underline"
        >
          ← Back to Dashboard
        </Link>
      </div>

      <h1 className="text-2xl font-bold">Alert Analytics</h1>

      {/* ===== Alerts by Source ===== */}
      <div className="bg-slate-800 p-4 rounded">
        <h2 className="mb-3 font-semibold">Alerts by Source</h2>

        <ResponsiveContainer width="100%" height={300}>
          <BarChart data={bySource}>
            <XAxis dataKey="_id" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="count" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* ===== Alerts Over Time ===== */}
      <div className="bg-slate-800 p-4 rounded">
        <h2 className="mb-3 font-semibold">
          Alerts Over Last 24 Hours
        </h2>

        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={overTime}>
            <XAxis dataKey="_id.hour" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="count" />
          </LineChart>
        </ResponsiveContainer>
      </div>

    </div>
  );
}

