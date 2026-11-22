// already logged in, go to dashboard
if (getToken()) {
    window.location.href = "dashboard.html";
}

const loginForm = document.getElementById("loginForm");
const loginBtn = document.getElementById("loginBtn");

loginForm.addEventListener("submit", async function (event) {
    event.preventDefault();
    hideMessage();

    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value;

    if (!email || !password) {
        showMessage("Enter your email and password", "error");
        return;
    }

    loginBtn.disabled = true;
    loginBtn.textContent = "Please wait...";

    try {
        const response = await fetch(API_URL + "/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email: email, password: password })
        });

        const data = await response.json();

        if (response.ok) {
            saveToken(data.token);
            window.location.href = "dashboard.html";
        } else {
            showMessage(data.message, "error");
        }
    } catch (error) {
        showMessage("Cannot connect to the server. Is the backend running?", "error");
    }

    loginBtn.disabled = false;
    loginBtn.textContent = "Login";
});
