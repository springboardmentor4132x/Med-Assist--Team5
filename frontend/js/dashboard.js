// page is protected, send to login if there is no token
checkLogin();

document.getElementById("logoutBtn").addEventListener("click", logout);

// cards shown for each role, link is empty if that page is not ready yet
const roleLinks = {
    patient: [
        { name: "My Profile", text: "View and edit your personal details", link: "profile.html" },
        { name: "Enter Symptoms", text: "Describe how you are feeling", link: "symptoms.html" },
        { name: "My Assessments", text: "Your past symptom assessments", link: "assessments.html" },
        { name: "Health Reports", text: "Your disease prediction results and reports", link: "" },
        { name: "Medical History", text: "Your past medical records", link: "history.html" }
    ],
    doctor: [
        { name: "My Profile", text: "View and edit your personal details", link: "profile.html" },
        { name: "My Patients", text: "Assigned patients and their medical history", link: "patients.html" },
        { name: "Health Reports", text: "Review patient health assessment reports", link: "" }
    ],
    clinic: [
        { name: "My Profile", text: "View and edit your details", link: "profile.html" },
        { name: "Clinic Information", text: "Healthcare information for your clinic", link: "" }
    ],
    admin: [
        { name: "My Profile", text: "View and edit your personal details", link: "profile.html" },
        { name: "Manage Users", text: "View users, change roles, monitor the application", link: "admin.html" }
    ]
};

function showRoleLinks(role) {
    const box = document.getElementById("roleLinks");
    const links = roleLinks[role] || [];

    links.forEach(function (item) {
        let card;

        if (item.link) {
            card = document.createElement("a");
            card.href = item.link;
            card.className = "link-card";
        } else {
            card = document.createElement("div");
            card.className = "link-card disabled";
        }

        const title = document.createElement("h4");
        title.textContent = item.name;
        const text = document.createElement("p");
        text.textContent = item.text;
        card.appendChild(title);
        card.appendChild(text);

        if (!item.link) {
            const soon = document.createElement("span");
            soon.className = "soon";
            soon.textContent = "Coming soon";
            card.appendChild(soon);
        }

        box.appendChild(card);
    });
}

async function loadUser() {
    try {
        const response = await authFetch("/me");
        const data = await response.json();

        if (!response.ok) {
            showMessage(data.message, "error");
            return;
        }

        const user = data.user;
        document.getElementById("navName").textContent = user.full_name;
        document.getElementById("welcomeText").textContent = "Welcome, " + user.full_name;
        document.getElementById("roleText").textContent = user.role;
        document.getElementById("infoName").textContent = user.full_name;
        document.getElementById("infoEmail").textContent = user.email;
        document.getElementById("infoAge").textContent = user.age;
        document.getElementById("infoGender").textContent = user.gender;
        document.getElementById("infoContact").textContent = user.contact || "Not provided";

        showRoleLinks(user.role);
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }
}

loadUser();
