const SOURCE_ID = 0;

// ---- Poll Redis-backed state ----
async function fetchState() {
    try {
        const res = await fetch(`http://localhost:5000/state/${SOURCE_ID}`);
        if (!res.ok) {
            document.getElementById("status").innerHTML =
                "<span class='alert'>Camera Offline</span>";
            return;
        }

        const data = await res.json();

        document.getElementById("status").innerHTML = `
            <p>Persons: <b>${data.person_count}</b></p>
            <p>Alert Active: <b>${data.alert_active}</b></p>
            <p>Last Update: ${new Date(data.last_updated * 1000).toLocaleTimeString()}</p>
        `;
    } catch (e) {
        console.error("State fetch failed", e);
    }
}

// ---- Poll Mongo-backed events ----
async function fetchEvents() {
    try {
        const res = await fetch(
            `http://localhost:5000/events?source_id=${SOURCE_ID}&limit=10`
        );
        const data = await res.json();

        const list = document.getElementById("events");
        list.innerHTML = "";

        data.events.forEach(ev => {
            const li = document.createElement("li");
            li.innerText = `${new Date(ev.timestamp * 1000).toLocaleTimeString()} - ${ev.message}`;
            list.appendChild(li);
        });
    } catch (e) {
        console.error("Event fetch failed", e);
    }
}

// ---- Poll intervals ----
setInterval(fetchState, 1500);
setInterval(fetchEvents, 4000);

// Initial load
fetchState();
fetchEvents();

