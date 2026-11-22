checkLogin();

document.getElementById("logoutBtn").addEventListener("click", logout);

const roles = ["patient", "doctor", "clinic", "admin"];
const userTable = document.getElementById("userTable");
let myId = null;

// first check that the logged in user is an admin
async function start() {
    try {
        const response = await authFetch("/me");
        const data = await response.json();

        if (!response.ok) {
            showMessage(data.message, "error");
            return;
        }

        if (data.user.role !== "admin") {
            alert("Only admin can open this page");
            window.location.href = "dashboard.html";
            return;
        }

        myId = data.user.id;
        loadStats();
        loadUsers();
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }
}

async function loadStats() {
    const response = await authFetch("/admin/stats");
    const data = await response.json();

    if (response.ok) {
        document.getElementById("statTotal").textContent = data.total;
        document.getElementById("statPatient").textContent = data.patient;
        document.getElementById("statDoctor").textContent = data.doctor;
        document.getElementById("statClinic").textContent = data.clinic;
        document.getElementById("statAdmin").textContent = data.admin;
    }
}

async function loadUsers() {
    const response = await authFetch("/admin/users");
    const data = await response.json();

    if (!response.ok) {
        showMessage(data.message, "error");
        return;
    }

    userTable.innerHTML = "";
    data.users.forEach(addRow);

    fillAssignSelects(data.users);
    loadAssignments();
}

function addRow(user) {
    const row = document.createElement("tr");

    const values = [user.id, user.full_name, user.email, user.age, user.gender, user.contact || "-"];
    values.forEach(function (value) {
        const cell = document.createElement("td");
        cell.textContent = value;
        row.appendChild(cell);
    });

    // role the user asked for while registering
    const requestedCell = document.createElement("td");
    requestedCell.textContent = user.requested_role !== user.role ? user.requested_role : "-";
    row.appendChild(requestedCell);

    // role dropdown
    const roleCell = document.createElement("td");
    const select = document.createElement("select");
    roles.forEach(function (role) {
        const option = document.createElement("option");
        option.value = role;
        option.textContent = role;
        if (role === user.role) {
            option.selected = true;
        }
        select.appendChild(option);
    });
    roleCell.appendChild(select);
    row.appendChild(roleCell);

    // buttons
    const actionCell = document.createElement("td");

    const saveBtn = document.createElement("button");
    saveBtn.textContent = "Save";
    saveBtn.className = "small-btn";
    saveBtn.addEventListener("click", function () {
        changeRole(user.id, select.value);
    });

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "Delete";
    deleteBtn.className = "small-btn delete";
    deleteBtn.addEventListener("click", function () {
        deleteUser(user.id, user.full_name);
    });

    // admin cannot edit or delete himself
    if (user.id === myId) {
        select.disabled = true;
        saveBtn.disabled = true;
        deleteBtn.disabled = true;
    }

    actionCell.appendChild(saveBtn);
    actionCell.appendChild(deleteBtn);
    row.appendChild(actionCell);

    userTable.appendChild(row);
}

async function changeRole(userId, role) {
    hideMessage();
    const response = await authFetch("/admin/users/" + userId + "/role", {
        method: "PUT",
        body: JSON.stringify({ role: role })
    });
    const data = await response.json();

    if (response.ok) {
        showMessage(data.message, "success");
        loadStats();
        loadUsers();
    } else {
        showMessage(data.message, "error");
    }
}

async function deleteUser(userId, name) {
    hideMessage();
    if (!confirm("Delete user " + name + "?")) {
        return;
    }

    const response = await authFetch("/admin/users/" + userId, { method: "DELETE" });
    const data = await response.json();

    if (response.ok) {
        showMessage(data.message, "success");
        loadStats();
        loadUsers();
    } else {
        showMessage(data.message, "error");
    }
}

// doctor - patient assignment
const doctorSelect = document.getElementById("doctorSelect");
const patientSelect = document.getElementById("patientSelect");
const assignTable = document.getElementById("assignTable");

function fillAssignSelects(users) {
    doctorSelect.innerHTML = "<option value=''>Select doctor</option>";
    patientSelect.innerHTML = "<option value=''>Select patient</option>";

    users.forEach(function (user) {
        const option = document.createElement("option");
        option.value = user.id;
        option.textContent = user.full_name + " (" + user.email + ")";

        if (user.role === "doctor") {
            doctorSelect.appendChild(option);
        } else if (user.role === "patient") {
            patientSelect.appendChild(option);
        }
    });
}

async function loadAssignments() {
    const response = await authFetch("/admin/assignments");
    const data = await response.json();

    if (!response.ok) {
        showMessage(data.message, "error");
        return;
    }

    assignTable.innerHTML = "";

    data.assignments.forEach(function (item) {
        const row = document.createElement("tr");

        [item.doctor_name, item.patient_name].forEach(function (value) {
            const cell = document.createElement("td");
            cell.textContent = value;
            row.appendChild(cell);
        });

        const actionCell = document.createElement("td");
        const removeBtn = document.createElement("button");
        removeBtn.textContent = "Remove";
        removeBtn.className = "small-btn delete";
        removeBtn.addEventListener("click", function () {
            removeAssignment(item.id);
        });
        actionCell.appendChild(removeBtn);
        row.appendChild(actionCell);

        assignTable.appendChild(row);
    });

    if (data.assignments.length === 0) {
        const row = document.createElement("tr");
        const cell = document.createElement("td");
        cell.colSpan = 3;
        cell.textContent = "No assignments yet";
        row.appendChild(cell);
        assignTable.appendChild(row);
    }
}

document.getElementById("assignBtn").addEventListener("click", async function () {
    hideMessage();

    if (!doctorSelect.value || !patientSelect.value) {
        showMessage("Select a doctor and a patient", "error");
        return;
    }

    const response = await authFetch("/admin/assignments", {
        method: "POST",
        body: JSON.stringify({ doctor_id: doctorSelect.value, patient_id: patientSelect.value })
    });
    const data = await response.json();

    if (response.ok) {
        showMessage(data.message, "success");
        loadAssignments();
    } else {
        showMessage(data.message, "error");
    }
});

async function removeAssignment(id) {
    hideMessage();
    const response = await authFetch("/admin/assignments/" + id, { method: "DELETE" });
    const data = await response.json();

    if (response.ok) {
        showMessage(data.message, "success");
        loadAssignments();
    } else {
        showMessage(data.message, "error");
    }
}

start();
