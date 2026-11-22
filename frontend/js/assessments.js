checkLogin();

document.getElementById("logoutBtn").addEventListener("click", logout);

async function loadAssessments() {
    try {
        const response = await authFetch("/symptoms/assessments");
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

        if (data.assessments.length === 0) {
            document.getElementById("noAssessments").classList.remove("hidden");
            return;
        }

        const table = document.getElementById("assessmentTable");
        data.assessments.forEach(function (item) {
            const row = document.createElement("tr");

            [item.id, item.created_at, item.symptoms.map(function (s) { return s.label; }).join(", ")].forEach(function (value) {
                const cell = document.createElement("td");
                cell.textContent = value;
                row.appendChild(cell);
            });

            const actionCell = document.createElement("td");
            const link = document.createElement("a");
            link.href = "assessment.html?id=" + item.id;
            link.textContent = "View";
            link.className = "small-btn";
            actionCell.appendChild(link);
            row.appendChild(actionCell);

            table.appendChild(row);
        });

        document.getElementById("tableWrap").classList.remove("hidden");
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }
}

loadAssessments();
