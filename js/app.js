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
