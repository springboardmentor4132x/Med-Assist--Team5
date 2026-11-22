checkLogin();

document.getElementById("logoutBtn").addEventListener("click", logout);

// assessment number comes from the url, assessment.html?id=3
const assessmentId = new URLSearchParams(window.location.search).get("id");

function makeCell(text) {
    const cell = document.createElement("td");
    cell.textContent = text;
    return cell;
}

async function loadAssessment() {
    if (!assessmentId || !/^\d+$/.test(assessmentId)) {
        showMessage("Assessment not found. Please open it from My Assessments.", "error");
        return;
    }

    try {
        const response = await authFetch("/symptoms/assessments/" + assessmentId);
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

        showAssessment(data.assessment);
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }
}

function showAssessment(assessment) {
    document.getElementById("subTitle").textContent =
        "Assessment no. " + assessment.assessment_id + " | " + assessment.created_at + " (UTC)";

    showSymptoms(assessment);
    showCorrelation(assessment.correlation);
    showRelated(assessment.correlation);
    showHistory(assessment.medical_history);

    document.getElementById("disclaimer").textContent = assessment.disclaimer;
    document.getElementById("content").classList.remove("hidden");
}

function showSymptoms(assessment) {
    document.getElementById("symptomCount").textContent = assessment.symptom_count;

    const box = document.getElementById("symptomChips");
    box.innerHTML = "";
    assessment.symptoms.forEach(function (item) {
        const chip = document.createElement("span");
        chip.className = "chip chosen";
        chip.textContent = item.label;
        box.appendChild(chip);
    });
}

function showCorrelation(correlation) {
    const table = document.getElementById("pairTable");
    table.innerHTML = "";

    if (correlation.pairs.length === 0) {
        document.getElementById("pairWrap").classList.add("hidden");
        document.getElementById("noPairs").classList.remove("hidden");
        document.getElementById("strongestText").textContent = "";
        return;
    }

    const best = correlation.strongest_pair;
    document.getElementById("strongestText").textContent =
        "Strongest relation: " + best.symptom_a_label + " and " + best.symptom_b_label +
        " (" + best.strength + ", seen together in " + best.rows_together + " of " + correlation.dataset_rows + " dataset rows).";

    correlation.pairs.forEach(function (pair) {
        const row = document.createElement("tr");
        row.appendChild(makeCell(pair.symptom_a_label));
        row.appendChild(makeCell(pair.symptom_b_label));
        row.appendChild(makeCell(pair.rows_together));
        row.appendChild(makeCell(pair.b_given_a + "%"));
        row.appendChild(makeCell(pair.a_given_b + "%"));

        const strengthCell = document.createElement("td");
        const badge = document.createElement("span");
        badge.className = "badge " + pair.strength;
        badge.textContent = pair.strength;
        strengthCell.appendChild(badge);
        row.appendChild(strengthCell);

        table.appendChild(row);
    });
}

function showRelated(correlation) {
    const list = document.getElementById("relatedList");
    list.innerHTML = "";

    if (correlation.related_symptoms.length === 0) {
        document.getElementById("relatedInfo").textContent = "";
        document.getElementById("noRelated").classList.remove("hidden");
        return;
    }

    if (correlation.related_based_on === "all_selected") {
        document.getElementById("relatedInfo").textContent =
            "In the " + correlation.rows_used + " dataset rows that have all your selected symptoms, these symptoms are seen most often.";
    } else {
        document.getElementById("relatedInfo").textContent =
            "No dataset row has all your selected symptoms together, so this is based on the " +
            correlation.rows_used + " rows that have at least one of them.";
    }

    correlation.related_symptoms.forEach(function (item) {
        const row = document.createElement("div");
        row.className = "related-row";

        const name = document.createElement("div");
        name.className = "related-name";
        name.textContent = item.label;

        const track = document.createElement("div");
        track.className = "bar-track";
        const fill = document.createElement("div");
        fill.className = "bar-fill";
        fill.style.width = item.percent + "%";
        track.appendChild(fill);

        const percent = document.createElement("div");
        percent.className = "related-percent";
        percent.textContent = item.percent + "%";

        row.appendChild(name);
        row.appendChild(track);
        row.appendChild(percent);
        list.appendChild(row);
    });
}

function showHistory(history) {
    const summary = document.getElementById("historySummary");
    const list = document.getElementById("historyList");
    list.innerHTML = "";

    if (history.total_records === 0) {
        summary.textContent = "You have not added any medical history yet. You can add it from the Medical History page.";
        return;
    }

    summary.textContent = history.total_records + " record(s) in your history, " +
        history.relevant_count + " related to the selected symptoms.";

    history.all_records.forEach(function (item) {
        const box = document.createElement("div");
        box.className = "history-item";
        if (item.relevant) {
            box.classList.add("relevant");
        }

        const date = document.createElement("div");
        date.className = "history-date";
        date.textContent = item.record_date;

        const title = document.createElement("h4");
        title.textContent = item.condition;

        if (item.relevant) {
            const tag = document.createElement("span");
            tag.className = "relevant-tag";
            tag.textContent = "Related to: " + item.matched_symptoms.join(", ");
            title.appendChild(tag);
        }

        box.appendChild(date);
        box.appendChild(title);

        if (item.notes) {
            const notes = document.createElement("p");
            notes.textContent = item.notes;
            box.appendChild(notes);
        }

        list.appendChild(box);
    });
}

loadAssessment();
