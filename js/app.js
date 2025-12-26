function login() {
    window.location.href = "dashboard.html";
}

function sendMessage(event) {
    if (event.key === "Enter") {
        alert("Respuesta IA simulada: El producto tiene stock suficiente.");
        event.target.value = "";
    }
}
