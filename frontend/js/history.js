checkLogin();

document.getElementById("logoutBtn").addEventListener("click", logout);

const historyForm = document.getElementById("historyForm");
const historyList = document.getElementById("historyList");
const addBtn = document.getElementById("addBtn");

// today's date in yyyy-mm-dd, future dates are not allowed
const today = new Date();
const todayText = today.getFullYear() + "-" + String(today.getMonth() + 1).padStart(2, "0") + "-" + String(today.getDate()).padStart(2, "0");
document.getElementById("recordDate").max = todayText;

async function loadHistory() {
    try {
        const response = await authFetch("/history");
        const data = await response.json();

        if (response.status === 403) {
            alert("Only patients can open this page");
            window.location.href = "dashboard.html";
            return;
        }

        if (!response.ok) {
            showMessage(data.message, "error");
            return;
        }

        showHistory(data.history);
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }
}

function showHistory(list) {
    historyList.innerHTML = "";

    if (list.length === 0) {
        const empty = document.createElement("p");
        empty.className = "empty-text";
        empty.textContent = "No records added yet.";
        historyList.appendChild(empty);
        return;
    }

    list.forEach(function (item) {
        const box = document.createElement("div");
        box.className = "history-item";

        const date = document.createElement("div");
        date.className = "history-date";
        date.textContent = item.record_date;

        const title = document.createElement("h4");
        title.textContent = item.condition;

        box.appendChild(date);
        box.appendChild(title);

        if (item.notes) {
            const notes = document.createElement("p");
            notes.textContent = item.notes;
            box.appendChild(notes);
        }

        historyList.appendChild(box);
    });
}

historyForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    hideMessage();

    const condition = document.getElementById("condition").value.trim();
    const recordDate = document.getElementById("recordDate").value;
    const notes = document.getElementById("notes").value.trim();

    // frontend validation
    if (!condition || !recordDate) {
        showMessage("Condition and date are required", "error");
        return;
    }

    if (condition.length < 3) {
        showMessage("Condition must be at least 3 characters", "error");
        return;
    }

    if (recordDate > todayText) {
        showMessage("Date cannot be in the future", "error");
        return;
    }

    addBtn.disabled = true;

    try {
        const response = await authFetch("/history", {
            method: "POST",
            body: JSON.stringify({ condition: condition, record_date: recordDate, notes: notes })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(data.message, "success");
            historyForm.reset();
            loadHistory();
        } else {
            showMessage(data.message, "error");
        }
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }

    addBtn.disabled = false;
});

loadHistory();
