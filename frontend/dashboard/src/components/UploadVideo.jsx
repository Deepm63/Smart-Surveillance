import { uploadVideo } from "../api/sources";
import { useState } from "react";

export default function UploadVideo({ onUploaded }) {
  const [name, setName] = useState("");
  const [inputKey, setInputKey] = useState(Date.now());

  const handleFile = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    if (!name.trim()) {
      alert("Please enter a video name");
      return;
    }

    const form = new FormData();
    form.append("file", file);
    form.append("name", name.trim());

    try {
      await uploadVideo(form);
      setName("");
      setInputKey(Date.now()); // 🔑 RESET FILE INPUT
      onUploaded();
    } catch (err) {
      console.error("Upload failed", err);
    }
  };

  return (
    <div className="bg-slate-800 p-3 rounded-lg space-y-2">
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Video name"
        className="w-full p-2 rounded bg-slate-700 text-sm"
      />

      <label className="block cursor-pointer text-sm">
        <input
          key={inputKey}        // 🔑 forces remount
          type="file"
          hidden
          accept="video/*"
          onChange={handleFile}
        />
        <div className="border border-dashed border-slate-500 rounded p-3 text-center">
          Upload Video
        </div>
      </label>
    </div>
  );
}

