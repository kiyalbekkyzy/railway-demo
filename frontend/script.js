const API_URL = "https://railway-demo-production-8ae2.up.railway.app/api/data";

async function loadItems() {
    const res = await fetch(API_URL);
    const data = await res.json();

    const list = document.getElementById("list");
    list.innerHTML = "";

    data.forEach(item => {
        const li = document.createElement("li");
        li.innerHTML = item.name + 
        ` <button onclick="deleteItem(${item.id})">Delete</button>`;
        list.appendChild(li);
    });
}

async function addItem() {
    const name = document.getElementById("name").value;

    await fetch(API_URL, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({name})
    });

    loadItems();
}

async function deleteItem(id) {
    await fetch(`${API_URL}/${id}`, {
        method: "DELETE"
    });

    loadItems();
}

loadItems();
