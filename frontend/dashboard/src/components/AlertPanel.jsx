import { useEffect, useState } from "react";
import { getEvents } from "../api/events";

export default function AlertPanel({ sourceId }) {
  const [events, setEvents] = useState([]);

useEffect(() => {
  let alive = true;

  const fetchEvents = async () => {
    try {
      const res = await getEvents(sourceId);
      if (alive) setEvents(res.data.events);
    } catch {
      if (alive) setEvents([]);
    }
  };

  fetchEvents();
  const t = setInterval(fetchEvents, 4000);

  return () => {
    alive = false;
    clearInterval(t);
  };
}, [sourceId]);

  return (
    <div className="bg-slate-800 rounded-lg p-3">
      <h3 className="font-semibold mb-2">Alerts</h3>
      <ul className="text-sm space-y-1">
        {events.length === 0 && <li className="text-slate-400">No alerts</li>}
        {events.map((e, i) => (
          <li key={i} className="text-red-400">
            {new Date(e.timestamp * 1000).toLocaleTimeString()} — {e.message}
          </li>
        ))}
      </ul>
    </div>
  );
}

