import axios from "axios";
const BASE = "http://localhost:5000";

export const uploadVideo = (formData) =>
  axios.post(`${BASE}/upload`, formData, {
    headers: { "Content-Type": "multipart/form-data" }
  });

export const getSources = () =>
  axios.get(`${BASE}/sources`).then(r => r.data.sources);

export const removeSource = (id) =>
  axios.delete(`${BASE}/remove_source/${id}`);

