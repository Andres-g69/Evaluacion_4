// =====================
// AUTH MODULE (Login + Logout + JWT)
// =====================

const API_LOGIN = "/api/auth/login/";
const API_REFRESH = "/api/auth/refresh/";

//
// Guardar tokens
//
function saveTokens(access, refresh) {
    localStorage.setItem("access", access);
    localStorage.setItem("refresh", refresh);
}

//
// Obtener header con JWT
//
function getAuthHeaders() {
    const access = localStorage.getItem("access");
    return {
        "Content-Type": "application/json",
        "Authorization": access ? `Bearer ${access}` : ""
    };
}

//
// LOGIN
//
async function login() {
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value;

    if (!username || !password) {
        alert("Debe ingresar usuario y contraseña");
        return;
    }

    const r = await fetch(API_LOGIN, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({username, password})
    });

    const data = await r.json();

    if (!r.ok) {
        alert("Credenciales incorrectas");
        return;
    }

    saveTokens(data.access, data.refresh);

    // Redirigir al dashboard
    window.location.href = "/frontend/dashboard.html";
}

//
// LOGOUT
//
function logout() {
    localStorage.removeItem("access");
    localStorage.removeItem("refresh");
    window.location.href = "/frontend/login.html";
}

//
// RENOVAR TOKEN (opcional)
//
async function autoRefreshToken() {
    const refresh = localStorage.getItem("refresh");
    if (!refresh) return;

    const r = await fetch(API_REFRESH, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({refresh})
    });

    if (r.ok) {
        const data = await r.json();
        localStorage.setItem("access", data.access);
    }
}

// Renovar cada 4 minutos
setInterval(autoRefreshToken, 240000);
