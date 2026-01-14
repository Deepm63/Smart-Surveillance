import axios from "axios";
const BASE = "http://localhost:5000";

export const detectCameras = () =>
  axios.get(`${BASE}/detect_cameras`).then(r => r.data.cameras);

export const addCamera = ({ path, name }) =>
  axios.post(`${BASE}/add_source`, { path, name });


