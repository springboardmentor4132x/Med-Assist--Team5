// backend url, change this if flask runs on a different port
const API_URL = "http://127.0.0.1:5000/api";

function saveToken(token) {
    localStorage.setItem("token", token);
}

function getToken() {
    return localStorage.getItem("token");
}

function logout() {
    localStorage.removeItem("token");
    window.location.href = "login.html";
}

// use this on pages that need login
function checkLogin() {
    if (!getToken()) {
        window.location.href = "login.html";
    }
}

function showMessage(text, type) {
    const box = document.getElementById("message");
    box.textContent = text;
    box.className = "message " + type;
}

function hideMessage() {
    const box = document.getElementById("message");
    box.className = "message";
    box.textContent = "";
}

// fetch for protected apis, adds the token and handles expired token
async function authFetch(path, options) {
    options = options || {};
    options.headers = options.headers || {};
    options.headers["Authorization"] = "Bearer " + getToken();

    if (options.body) {
        options.headers["Content-Type"] = "application/json";
    }

    const response = await fetch(API_URL + path, options);

    if (response.status === 401) {
        const data = await response.clone().json();
        alert(data.message);
        logout();
    }

    return response;
}
