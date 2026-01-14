import axios from "axios";
const BASE = "http://localhost:5000";

export const alertsBySource = () =>
  axios.get(`${BASE}/analytics/alerts/by_source`)
       .then(r => r.data.data);

export const alertsOverTime = (hours = 24) =>
  axios.get(`${BASE}/analytics/alerts/over_time?hours=${hours}`)
       .then(r => r.data.data);

