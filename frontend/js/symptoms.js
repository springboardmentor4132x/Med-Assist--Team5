checkLogin();

document.getElementById("logoutBtn").addEventListener("click", logout);

const MAX_SYMPTOMS = 20;

const searchBox = document.getElementById("searchBox");
const commonList = document.getElementById("commonList");
const symptomList = document.getElementById("symptomList");
const selectedList = document.getElementById("selectedList");
const submitBtn = document.getElementById("submitBtn");

let allSymptoms = [];
let selected = [];

async function loadSymptoms() {
    try {
        const response = await authFetch("/symptoms");
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

        allSymptoms = data.symptoms;
        showCommon();
        showList();
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }
}

function getLabel(key) {
    const symptom = allSymptoms.find(function (item) {
        return item.key === key;
    });
    return symptom ? symptom.label : key;
}

function makeChip(symptom) {
    const chip = document.createElement("button");
    chip.type = "button";
    chip.className = "chip";
    chip.textContent = symptom.label;
    chip.dataset.key = symptom.key;
    chip.addEventListener("click", function () {
        addSymptom(symptom.key);
    });
    return chip;
}

function showCommon() {
    commonList.innerHTML = "";
    allSymptoms.filter(function (item) {
        return item.common;
    }).forEach(function (item) {
        commonList.appendChild(makeChip(item));
    });
    updateChips();
}

// shows all symptoms, or only the ones matching the search text
function showList() {
    const text = searchBox.value.trim().toLowerCase();
    const keyText = text.replace(/ /g, "_");

    symptomList.innerHTML = "";
    let count = 0;

    allSymptoms.forEach(function (item) {
        if (text === "" || item.label.toLowerCase().includes(text) || item.key.includes(keyText)) {
            symptomList.appendChild(makeChip(item));
            count++;
        }
    });

    document.getElementById("noMatch").classList.toggle("hidden", count > 0);
    updateChips();
}

// chips of selected symptoms look different
function updateChips() {
    document.querySelectorAll(".chip[data-key]").forEach(function (chip) {
        chip.classList.toggle("selected", selected.includes(chip.dataset.key));
    });
}

function addSymptom(key) {
    hideMessage();

    if (selected.includes(key)) {
        showMessage(getLabel(key) + " is already selected", "error");
        return;
    }

    if (selected.length >= MAX_SYMPTOMS) {
        showMessage("You can select up to " + MAX_SYMPTOMS + " symptoms at a time", "error");
        return;
    }

    selected.push(key);
    showSelected();
}

function removeSymptom(key) {
    hideMessage();
    selected = selected.filter(function (item) {
        return item !== key;
    });
    showSelected();
}

function showSelected() {
    selectedList.innerHTML = "";

    selected.forEach(function (key) {
        const chip = document.createElement("span");
        chip.className = "chip chosen";
        chip.textContent = getLabel(key);

        const removeBtn = document.createElement("button");
        removeBtn.type = "button";
        removeBtn.className = "chip-remove";
        removeBtn.textContent = "x";
        removeBtn.title = "Remove";
        removeBtn.addEventListener("click", function () {
            removeSymptom(key);
        });

        chip.appendChild(removeBtn);
        selectedList.appendChild(chip);
    });

    document.getElementById("selectedCount").textContent = selected.length;
    document.getElementById("noSelected").classList.toggle("hidden", selected.length > 0);
    updateChips();
}

searchBox.addEventListener("input", showList);

document.getElementById("clearBtn").addEventListener("click", function () {
    hideMessage();
    selected = [];
    showSelected();
});

submitBtn.addEventListener("click", async function () {
    hideMessage();

    // frontend validation
    if (selected.length === 0) {
        showMessage("Please select at least one symptom.", "error");
        return;
    }

    if (new Set(selected).size !== selected.length) {
        showMessage("Duplicate symptoms are selected", "error");
        return;
    }

    const supported = allSymptoms.map(function (item) {
        return item.key;
    });
    const unknown = selected.filter(function (key) {
        return !supported.includes(key);
    });
    if (unknown.length > 0) {
        showMessage("Unsupported symptom: " + unknown.join(", "), "error");
        return;
    }

    submitBtn.disabled = true;

    try {
        const response = await authFetch("/symptoms/submit", {
            method: "POST",
            body: JSON.stringify({ selected_symptoms: selected })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(data.message + ". Preparing your assessment...", "success");
            setTimeout(function () {
                window.location.href = "assessment.html?id=" + data.assessment_id;
            }, 800);
            return;
        } else {
            showMessage(data.error || data.message, "error");
        }
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }

    submitBtn.disabled = false;
});

loadSymptoms();
