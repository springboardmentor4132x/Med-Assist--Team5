checkLogin();

document.getElementById("logoutBtn").addEventListener("click", logout);

const viewBox = document.getElementById("viewBox");
const editBox = document.getElementById("editBox");
const profileForm = document.getElementById("profileForm");
const saveBtn = document.getElementById("saveBtn");

let currentUser = null;

async function loadProfile() {
    try {
        const response = await authFetch("/profile");
        const data = await response.json();

        if (!response.ok) {
            showMessage(data.message, "error");
            return;
        }

        currentUser = data.user;
        showProfile();
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }
}

function showProfile() {
    document.getElementById("roleText").textContent = currentUser.role;
    document.getElementById("infoName").textContent = currentUser.full_name;
    document.getElementById("infoEmail").textContent = currentUser.email;
    document.getElementById("infoAge").textContent = currentUser.age;
    document.getElementById("infoGender").textContent = currentUser.gender;
    document.getElementById("infoContact").textContent = currentUser.contact || "Not provided";
    document.getElementById("infoJoined").textContent = currentUser.created_at.split(" ")[0];
}

document.getElementById("editBtn").addEventListener("click", function () {
    hideMessage();
    document.getElementById("fullName").value = currentUser.full_name;
    document.getElementById("email").value = currentUser.email;
    document.getElementById("age").value = currentUser.age;
    document.getElementById("gender").value = currentUser.gender;
    document.getElementById("contact").value = currentUser.contact || "";

    viewBox.classList.add("hidden");
    editBox.classList.remove("hidden");
});

document.getElementById("cancelBtn").addEventListener("click", function () {
    hideMessage();
    editBox.classList.add("hidden");
    viewBox.classList.remove("hidden");
});

profileForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    hideMessage();

    const fullName = document.getElementById("fullName").value.trim();
    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const contact = document.getElementById("contact").value.trim();

    // frontend validation
    if (!fullName || !age || !gender) {
        showMessage("Name, age and gender are required", "error");
        return;
    }

    if (fullName.length < 3) {
        showMessage("Name must be at least 3 characters", "error");
        return;
    }

    if (age < 1 || age > 120) {
        showMessage("Enter a valid age", "error");
        return;
    }

    if (contact && !/^\d{10}$/.test(contact)) {
        showMessage("Contact number must be 10 digits", "error");
        return;
    }

    saveBtn.disabled = true;

    try {
        const response = await authFetch("/profile", {
            method: "PUT",
            body: JSON.stringify({
                full_name: fullName,
                age: age,
                gender: gender,
                contact: contact
            })
        });

        const data = await response.json();

        if (response.ok) {
            currentUser = data.user;
            showProfile();
            editBox.classList.add("hidden");
            viewBox.classList.remove("hidden");
            showMessage(data.message, "success");
        } else {
            showMessage(data.message, "error");
        }
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }

    saveBtn.disabled = false;
});

loadProfile();
