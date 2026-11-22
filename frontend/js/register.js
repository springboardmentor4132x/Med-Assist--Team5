// if already logged in, no need to register again
if (getToken()) {
    window.location.href = "dashboard.html";
}

const registerForm = document.getElementById("registerForm");
const registerBtn = document.getElementById("registerBtn");

// patient, doctor or clinic tab
let selectedRole = "patient";
const tabs = document.querySelectorAll(".tab");

tabs.forEach(function (tab) {
    tab.addEventListener("click", function () {
        tabs.forEach(function (item) {
            item.classList.remove("active");
        });
        tab.classList.add("active");
        selectedRole = tab.dataset.role;

        // only show the note for doctor and clinic
        document.getElementById("roleNote").classList.toggle("hidden", selectedRole === "patient");
    });
});

registerForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    hideMessage();

    const fullName = document.getElementById("fullName").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const age = document.getElementById("age").value;
    const gender = document.getElementById("gender").value;
    const contact = document.getElementById("contact").value.trim();

    // frontend validation
    if (!fullName || !email || !password || !confirmPassword || !age || !gender) {
        showMessage("Please fill all the required fields", "error");
        return;
    }

    if (fullName.length < 3) {
        showMessage("Name must be at least 3 characters", "error");
        return;
    }

    const emailPattern = /^[\w.-]+@[\w.-]+\.\w+$/;
    if (!emailPattern.test(email)) {
        showMessage("Enter a valid email address", "error");
        return;
    }

    if (password.length < 6) {
        showMessage("Password must be at least 6 characters", "error");
        return;
    }

    if (password !== confirmPassword) {
        showMessage("Passwords do not match", "error");
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

    registerBtn.disabled = true;
    registerBtn.textContent = "Please wait...";

    try {
        const response = await fetch(API_URL + "/register", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                full_name: fullName,
                email: email,
                password: password,
                age: age,
                gender: gender,
                contact: contact,
                role: selectedRole
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage(data.message, "success");
            registerForm.reset();
            setTimeout(function () {
                window.location.href = "login.html";
            }, selectedRole === "patient" ? 1500 : 3500);
        } else {
            showMessage(data.message, "error");
        }
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }

    registerBtn.disabled = false;
    registerBtn.textContent = "Register";
});
