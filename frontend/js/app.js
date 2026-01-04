function login() {
    window.location.href = "dashboard.html";
}

function sendMessage(event) {
    if (event.key === "Enter") {
        alert("Respuesta IA simulada: El producto tiene stock suficiente.");
        event.target.value = "";
    }
}

const API_URL = "http://127.0.0.1:5000/api";

async function cargarDashboard() {
    try {
        const res = await fetch(`${API_URL}/productos`);
        const productos = await res.json();

        document.getElementById("totalProductos").innerText = productos.length;

        const stockBajo = productos.filter(p => p.stock <= p.stock_minimo).length;
        document.getElementById("stockBajo").innerText = stockBajo;

        const hoy = new Date();
        const porCaducar = productos.filter(p => {
            const fecha = new Date(p.fecha_caducidad);
            return fecha <= hoy;
        }).length;

        document.getElementById("porCaducar").innerText = porCaducar;

    } catch (error) {
        console.error("Error cargando dashboard", error);
    }
}

async function cargarInventario() {
    try {
        const res = await fetch(`${API_URL}/productos`);
        const productos = await res.json();

        const tbody = document.getElementById("tablaInventario");
        if (!tbody) return;

        tbody.innerHTML = "";

        productos.forEach(p => {
            tbody.innerHTML += `
                <tr>
                    <td>${p.nombre}</td>
                    <td>${p.categoria || "-"}</td>
                    <td>${p.stock}</td>
                    <td>${p.stock_minimo}</td>
                    <td>${p.fecha_caducidad || "-"}</td>
                </tr>
            `;
        });

    } catch (error) {
        console.error("Error cargando inventario", error);
    }
}

async function cargarAlertas() {
    try {
        const res = await fetch(`${API_URL}/alertas`);
        const alertas = await res.json();

        const contenedor = document.getElementById("contenedorAlertas");
        if (!contenedor) return;

        contenedor.innerHTML = "";

        if (alertas.length === 0) {
            contenedor.innerHTML = "<p>No hay alertas activas.</p>";
            return;
        }

        alertas.forEach(a => {
            const tipoClase = a.tipo.toLowerCase().includes("stock")
                ? "warning"
                : "danger";

            contenedor.innerHTML += `
                <div class="alert ${tipoClase}">
                    <strong>${a.tipo}:</strong> ${a.descripcion}
                </div>
            `;
        });

    } catch (error) {
        console.error("Error cargando alertas", error);
    }
}

async function cargarDashboard() {
    try {
        const res = await fetch("http://127.0.0.1:5000/api/dashboard");
        const data = await res.json();

        // KPIs
        document.getElementById("totalProductos").innerText = data.total_productos;
        document.getElementById("stockBajo").innerText = data.stock_bajo;
        document.getElementById("alertasActivas").innerText = data.alertas_activas;

        // Gráfico
        const ctx = document.getElementById("dashboardChart").getContext("2d");

        new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Total Productos", "Stock Bajo", "Alertas Activas"],
                datasets: [{
                    label: "Estado del Inventario",
                    data: [
                        data.total_productos,
                        data.stock_bajo,
                        data.alertas_activas
                    ],
                    backgroundColor: [
                        "#2563eb",
                        "#f59e0b",
                        "#dc2626"
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });

    } catch (error) {
        console.error("Error cargando dashboard", error);
    }
}

async function enviarMensaje(event) {
    if (event.key === "Enter") {
        const input = document.getElementById("mensaje");
        const mensaje = input.value.trim();
        if (!mensaje) return;

        const chatBox = document.getElementById("chatBox");

        chatBox.innerHTML += `<div class="user">🧑 ${mensaje}</div>`;

        const res = await fetch("http://127.0.0.1:5000/api/chatbot", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ mensaje })
        });

        const data = await res.json();

        chatBox.innerHTML += `<div class="bot">🤖 ${data.respuesta}</div>`;
        chatBox.scrollTop = chatBox.scrollHeight;

        input.value = "";
    }
}

async function login() {
    const correo = document.getElementById("correo").value;
    const password = document.getElementById("password").value;

    const res = await fetch("http://127.0.0.1:5000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ correo, password })
    });

    if (!res.ok) {
        alert("Credenciales incorrectas");
        return;
    }

    const data = await res.json();

    // GUARDAR USUARIO
    localStorage.setItem("usuario", JSON.stringify(data.usuario));

    window.location.href = "dashboard.html";
}

function protegerRutaAdmin() {
    const usuario = JSON.parse(localStorage.getItem("usuario"));

    if (!usuario || usuario.rol !== "admin") {
        alert("Acceso denegado");
        window.location.href = "dashboard.html";
    }
}

async function cargarUsuarios() {
    const res = await fetch(`${API_URL}/usuarios`);
    const usuarios = await res.json();

    const tabla = document.getElementById("tablaUsuarios");
    tabla.innerHTML = "";

    usuarios.forEach(u => {
        tabla.innerHTML += `
            <tr>
                <td>${u.nombre}</td>
                <td>${u.correo}</td>
                <td>${u.rol}</td>
                <td>${u.estado ? "Activo" : "Inactivo"}</td>
                <td>
                    <button onclick="cambiarEstado(${u.id})">
                        ${u.estado ? "Desactivar" : "Activar"}
                    </button>
                </td>
            </tr>
        `;
    });
}

async function crearUsuario() {
    const nombre = document.getElementById("nombre").value;
    const correo = document.getElementById("correo").value;
    const password = document.getElementById("password").value;
    const rol = document.getElementById("rol").value;

    const res = await fetch(`${API_URL}/usuarios`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, correo, password, rol })
    });

    const data = await res.json();
    alert(data.message);

    cargarUsuarios();
}

async function cambiarEstado(id) {
    await fetch(`${API_URL}/usuarios/${id}/estado`, {
        method: "PUT"
    });

    cargarUsuarios();
}

function mostrarMenuUsuariosSegunRol() {
    const usuario = JSON.parse(localStorage.getItem("usuario"));

    // Si no hay usuario logueado, ocultar siempre
    if (!usuario) return;

    const menuUsuarios = document.querySelector('a[href="usuarios.html"]');
    if (!menuUsuarios) return;

    // Solo mostrar si el rol es admin
    if (usuario.rol !== "admin") {
        menuUsuarios.style.display = "none";
    } else {
        menuUsuarios.style.display = "block";
    }
}

// Llamar la función al cargar la página
mostrarMenuUsuariosSegunRol();
