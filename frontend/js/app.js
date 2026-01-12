function sendMessage(event) {
    if (event.key === "Enter") {
        alert("Respuesta IA simulada: El producto tiene stock suficiente.");
        event.target.value = "";
    }
}

const API_URL = "http://127.0.0.1:5000/api";


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
                    <td>${p.precio ?? "0.00"}</td>
                    <td>
                    <button onclick="abrirEditarProducto(${p.id})">
                        ✏️ Editar
                    </button>
                </td>
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
            contenedor.innerHTML = `
                <tr>
                    <td colspan="5">No hay alertas activas.</td>
                </tr>
            `;
            return;
        }

        alertas.forEach(a => {

            let clase = "bajo";
            let icono = "⚠️";
        
            if (a.estado === "CRÍTICO") {
                clase = "critico";
                icono = "🚨";
            } else if (a.estado === "CADUCADO") {
                clase = "caducado";
                icono = "⛔";
            } else if (a.estado === "PRÓXIMO A CADUCAR") {
                clase = "proximo";
                icono = "⏳";
            }
        
            contenedor.innerHTML += `
                <tr>
                    <td><strong>${a.producto}</strong></td>
                    <td>${a.fecha_caducidad}</td>
                    <td>${a.stock} unidades</td>
                    <td>
                        <span class="estado ${clase}">
                            ${icono} ${a.estado}
                        </span>
                    </td>
                    <td>
                        <button class="btn-reponer"
                            onclick="abrirReponer(${a.producto_id})">
                            Reponer
                        </button>
                    </td>
                </tr>
            `;
        });        

    } catch (error) {
        console.error("Error cargando alertas", error);
    }
}

async function cargarDashboard() {
    try {
        const res = await fetch(`${API_URL}/dashboard`);
        const data = await res.json();

        document.getElementById("totalProductos").innerText = data.total_productos;
        document.getElementById("stockBajo").innerText = data.stock_bajo;
        document.getElementById("stockCritico").innerText = data.stock_critico;
        document.getElementById("porCaducar").innerText = data.por_caducar;
        document.getElementById("caducados").innerText = data.caducados;
        document.getElementById("alertasActivas").innerText = data.alertas_activas;

        const ctx = document.getElementById("dashboardChart").getContext("2d");

if (window.dashboardChartInstance) {
    window.dashboardChartInstance.destroy();
}

window.dashboardChartInstance = new Chart(ctx, {
    type: "doughnut",
    data: {
        labels: [
            "Stock crítico",
            "Stock bajo",
            "Por caducar",
            "Caducados"
        ],
        datasets: [{
            data: [
                data.stock_critico,
                data.stock_bajo,
                data.por_caducar,
                data.caducados
            ],
            backgroundColor: [
                "#dc2626",  // crítico
                "#f59e0b",  // bajo
                "#2563eb",  // por caducar
                "#6b7280"   // caducados (gris)
            ]
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: "bottom"
            }
        }
    }
});

const ctxBar = document.getElementById("estadoChart").getContext("2d");

if (window.estadoChartInstance) {
    window.estadoChartInstance.destroy();
}

window.estadoChartInstance = new Chart(ctxBar, {
    type: "bar",
    data: {
        labels: ["Crítico", "Bajo", "Por caducar", "Caducados"],
        datasets: [{
            label: "Productos",
            data: [
                data.stock_critico,
                data.stock_bajo,
                data.por_caducar,
                data.caducados
            ],
            backgroundColor: [
                "#dc2626",
                "#f59e0b",
                "#2563eb",
                "#6b7280"
            ],
            borderRadius: 6
        }]
    },
    options: {
        responsive: true,
        plugins: {
            legend: { display: false }
        },
        scales: {
            y: {
                beginAtZero: true,
                ticks: { precision: 0 }
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

        // Mostrar mensaje del usuario
        chatBox.innerHTML += `<div class="user">🧑 ${mensaje}</div>`;

        try {
            const res = await fetch("http://127.0.0.1:5000/api/chatbot", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ mensaje })
            });

            const data = await res.json();

            // 🔹 MEJORA AQUÍ: Procesar la respuesta de la IA
            // 1. Reemplazamos los saltos de línea por <br>
            // 2. Reemplazamos las negritas de Markdown (**) por etiquetas <b> de HTML
            let respuestaFormateada = data.respuesta
                .replace(/\n/g, '<br>')
                .replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');

            chatBox.innerHTML += `<div class="bot">🤖 ${respuestaFormateada}</div>`;
            
            // Scroll automático al final
            chatBox.scrollTop = chatBox.scrollHeight;

        } catch (error) {
            console.error("Error:", error);
            chatBox.innerHTML += `<div class="bot">⚠️ Error al conectar con la IA.</div>`;
        }

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

    // 🔒 VALIDACIÓN DE CORREO (AQUÍ VA)
    if (!validarCorreo(correo)) {
        alert("Correo inválido");
        return; // ⛔ corta aquí, no llega al backend
    }

    const res = await fetch(`${API_URL}/usuarios`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ nombre, correo, password, rol })
    });

    const data = await res.json();
    alert(data.message || data.error);

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

function syncProductos() {
    fetch(`${API_URL}/sync-productos`, {
        method: "POST"
    })
    .then(res => res.json())
    .then(data => {
        alert(`✔ ${data.creados} creados | 🔁 ${data.actualizados} actualizados`);
        location.reload();
    });
}

function validarCorreo(correo) {
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return regex.test(correo);

}

function enviarFormularioUsuario() {
    const correo = document.getElementById("correo").value;

    if (!validarCorreo(correo)) {
        alert("Correo inválido");
        return; // ✅ AHORA sí es válido
    }

    // fetch aquí
}

function buscarInventario() {
    const texto = document.getElementById("busquedaInventario").value.toLowerCase();
    const filas = document.querySelectorAll("#tablaInventario tr");

    filas.forEach(fila => {
        const contenido = fila.innerText.toLowerCase();
        fila.style.display = contenido.includes(texto) ? "" : "none";
    });
}

function editarProducto(id) {
    const nuevoStock = prompt("Nuevo stock:");
    const nuevoPrecio = prompt("Nuevo precio:");

    if (nuevoStock === null || nuevoPrecio === null) return;

    fetch(`${API_URL}/productos/${id}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            stock: nuevoStock,
            precio: nuevoPrecio
        })
    })
    .then(res => res.json())
    .then(data => {
        alert(data.message);
        cargarInventario();
    });
}

function buscarAlertas() {
    const texto = document.getElementById("busquedaAlertas").value.toLowerCase();
    const alertas = document.querySelectorAll(".alert");

    alertas.forEach(a => {
        a.style.display = a.innerText.toLowerCase().includes(texto) ? "" : "none";
    });
}


let productoSeleccionado = null;

function abrirReponer(id) {
    productoSeleccionado = id;
    document.getElementById("modalReponer").style.display = "block";
}

function cerrarModal() {
    document.getElementById("modalReponer").style.display = "none";
}

async function confirmarReponer() {
    const stock = document.getElementById("nuevoStock").value;
    const fecha = document.getElementById("nuevaFecha").value;
    const observacion = document.getElementById("observacion").value;

    const usuario = JSON.parse(localStorage.getItem("usuario"));

    await fetch(`${API_URL}/productos/${productoSeleccionado}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            stock,
            fecha_caducidad: fecha,
            observacion,
            usuario_id: usuario.id
        })
    });

    cerrarModal();
    cargarAlertas();
    cargarDashboard();
}


let productoEditando = null;

function abrirEditarProducto(id) {
    productoEditando = id;
    document.getElementById("modalEditarProducto").style.display = "block";
}

function cerrarModalProducto() {
    document.getElementById("modalEditarProducto").style.display = "none";
}

async function guardarEdicionProducto() {
    const stock = document.getElementById("editStock").value;
    const stock_minimo = document.getElementById("editStockMin").value;
    const fecha_caducidad = document.getElementById("editFecha").value;
    const precio = document.getElementById("editPrecio").value;

    fetch(`${API_URL}/productos/${productoEditando}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            stock,
            stock_minimo,
            fecha_caducidad,
            precio
        })
    })
    .then(res => {
        if (!res.ok) throw new Error("Error al guardar");
        return res.json();
    })
    .then(() => {
        cerrarModalProducto();
        cargarInventario(); // 🔁 refresca tabla
    })
    .catch(err => {
        alert("No se pudo actualizar el producto");
        console.error(err);
    });
}