import axios from "axios";
const BASE = "http://localhost:5000";

export const getState = (id) =>
  axios.get(`${BASE}/state/${id}`);

