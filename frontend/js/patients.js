checkLogin();

document.getElementById("logoutBtn").addEventListener("click", logout);

const patientTable = document.getElementById("patientTable");
const detailBox = document.getElementById("detailBox");
const historyList = document.getElementById("historyList");

async function loadPatients() {
    try {
        const response = await authFetch("/doctor/patients");
        const data = await response.json();

        if (response.status === 403) {
            alert("Only doctors can open this page");
            window.location.href = "dashboard.html";
            return;
        }

        if (!response.ok) {
            showMessage(data.message, "error");
            return;
        }

        patientTable.innerHTML = "";
        data.patients.forEach(addRow);

        if (data.patients.length === 0) {
            document.getElementById("noPatients").classList.remove("hidden");
        }
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }
}

function addRow(patient) {
    const row = document.createElement("tr");

    const values = [patient.full_name, patient.email, patient.age, patient.gender, patient.contact || "-"];
    values.forEach(function (value) {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.appendChild(cell);
    });

    const actionCell = document.createElement("td");
    const viewBtn = document.createElement("button");
    viewBtn.textContent = "View History";
    viewBtn.className = "small-btn";
    viewBtn.addEventListener("click", function () {
        loadHistory(patient);
    });
    actionCell.appendChild(viewBtn);
    row.appendChild(actionCell);

    patientTable.appendChild(row);
}

async function loadHistory(patient) {
    hideMessage();

    try {
        const response = await authFetch("/history/patient/" + patient.id);
        const data = await response.json();

        if (!response.ok) {
            showMessage(data.message, "error");
            return;
        }

        document.getElementById("patientName").textContent = patient.full_name;
        document.getElementById("patientInfo").textContent =
            patient.email + " | Age " + patient.age + " | " + patient.gender + " | Contact: " + (patient.contact || "-");

        historyList.innerHTML = "";

        if (data.history.length === 0) {
            const empty = document.createElement("p");
            empty.className = "empty-text";
            empty.textContent = "This patient has no history records.";
            historyList.appendChild(empty);
        }

        data.history.forEach(function (item) {
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

        detailBox.classList.remove("hidden");
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }
}

loadPatients();
