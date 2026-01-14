import { useEffect, useState } from "react";
import { getState } from "../api/state";

export default function StatusBadge({ sourceId }) {
  const [state, setState] = useState(null);

  useEffect(() => {
  let alive = true;

  const fetchState = async () => {
    try {
      const res = await getState(sourceId);
      if (alive) setState(res.data);
    } catch {
      if (alive) setState(null);
    }
  };

  fetchState();
  const t = setInterval(fetchState, 1500);

  return () => {
    alive = false;
    clearInterval(t);
  };
}, [sourceId]);


  if (!state) return <div className="text-red-400">Offline</div>;

  return (
    <div className="text-sm space-y-1">
      <div>Persons: <b>{state.person_count}</b></div>
      <div>
        Alert:{" "}
        <span className={state.alert_active ? "text-red-400" : "text-green-400"}>
          {state.alert_active ? "ACTIVE" : "NORMAL"}
        </span>
      </div>
    </div>
  );
}

