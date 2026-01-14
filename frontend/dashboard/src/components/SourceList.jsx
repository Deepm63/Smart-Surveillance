import { removeSource } from "../api/sources";

export default function SourceList({ sources, active, onSelect, onRemoved }) {
  const handleRemove = async (id, e) => {
    e.stopPropagation();
    await removeSource(id);
    onRemoved();
  };

  return (
    <div className="bg-slate-800 rounded-lg p-3">
      <h3 className="font-semibold mb-3">Sources</h3>

      <ul className="space-y-2 text-sm">
        {sources.map(s => (
          <li
            key={s.id}
            onClick={() => onSelect(s.id)}
            className={`flex justify-between items-center p-2 rounded cursor-pointer
              ${active === s.id ? "bg-slate-700" : "hover:bg-slate-700"}`}
          >
            <span>
  		{s.type === "camera" ? "📷" : "🎞️"} {s.name}
	    </span>


            <button
              onClick={(e) => handleRemove(s.id, e)}
              className="flex items-center gap-1 text-red-400 hover:text-red-500 text-xs"
            >
              ❌ <span>Delete source</span>
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}

