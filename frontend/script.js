const API = import.meta.env.VITE_API_URL || "http://localhost:5000";

async function load() {
  const res = await fetch(API + "/api/data");
  const data = await res.json();

  const list = document.getElementById("list");
  list.innerHTML = "";

  data.forEach(item => {
    const li = document.createElement("li");
    li.innerText = item[1];

    const btn = document.createElement("button");
    btn.innerText = "Delete";
    btn.onclick = () => del(item[0]);

    li.appendChild(btn);
    list.appendChild(li);
  });
}

async function add() {
  const value = document.getElementById("input").value;
  await fetch(API + "/api/data", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({name: value})
  });
  load();
}

async function del(id) {
  await fetch(API + "/api/data/" + id, { method: "DELETE" });
  load();
}

load();
