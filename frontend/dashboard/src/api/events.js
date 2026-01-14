import axios from "axios";
const BASE = "http://localhost:5000";

export const getEvents = (id) =>
  axios.get(`${BASE}/events?source_id=${id}&limit=10`);

