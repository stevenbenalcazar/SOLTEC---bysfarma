# SOLTEC - Sistema Inteligente de Gestión de Inventarios 🚀
SOLTEC es una solución integral diseñada para optimizar el control de inventarios en farmacias o bodegas técnicas. El sistema combina un potente backend en Python con una interfaz web moderna, permitiendo la gestión masiva de productos (900+ registros) y análisis de stock en tiempo real.

## 🛠️ Tecnologías Utilizadas
Frontend: HTML5, CSS3 (Diseño responsivo), JavaScript (ES6+), Chart.js (Visualización de datos).

Backend: Python 3.x, Flask (Framework web), Flask-SQLAlchemy (ORM), Flask-CORS, Flask-Bcrypt (Seguridad).

Base de Datos: MySQL 8.0+.

Procesamiento de Datos: Pandas & OpenPyXL (Para la migración masiva desde Excel/CSV).

## 📋 Características Principales
Autenticación Segura: Sistema de login con roles diferenciados (Admin y Operador).

Dashboard Dinámico: Visualización de KPIs como Total de Productos, Stock Bajo y Alertas de Caducidad.

Gestión de Inventario: Carga masiva de datos corrigiendo errores comunes de Excel (notación científica en códigos de barras).

Seguridad por Roles: El acceso a la gestión de usuarios está restringido únicamente a administradores.

Chatbot IA (Simulado): Interfaz preparada para consultas inteligentes sobre el stock.

## ⚙️ Configuración del Entorno
1. Requisitos Previos
* Tener instalado Python 3.10+.
* Servidor MySQL (XAMPP, WAMP o MySQL Installer).

2. Base de Datos
* Crea la base de datos en tu servidor MySQL:
* SQL
* CREATE DATABASE soltec_inventario;

Asegúrate de configurar tus credenciales en backend/config.py.

3. Instalación
* Desde la terminal (Git Bash o VS Code), clona el proyecto y configura el entorno virtual:
* Bash

## Activar entorno virtual
python -m venv venv

### Activación del Entorno Virtual según tu Terminal
| Terminal | Comando de Activación |
| :--- | :--- |
| **Git Bash** | `source venv/Scripts/activate` |
| **PowerShell** | `.\venv\Scripts\Activate.ps1` |
| **CMD** | `.\venv\Scripts\activate` |

## Instalar dependencias
pip install -r requirements.txt
## 🚀 Cómo Correr el Programa
Iniciar el Backend:

Bash
* python backend/app.py


El servidor correrá en http://127.0.0.1:5000.

Abrir el Frontend:

Utiliza la extensión Live Server de VS Code sobre frontend/index.html para evitar problemas de rutas.

URL por defecto: http://127.0.0.1:5500/frontend/index.html.

📂 Estructura del Proyecto
Plaintext

SOLTEC---bysfarma/
├── backend/            # Lógica en Python (Flask)
│   ├── models/         # Modelos de SQLAlchemy
│   ├── routes/         # Endpoints de la API (Auth, Inventario, etc.)
│   └── app.py          # Punto de entrada del servidor
├── frontend/           # Interfaz de usuario
│   ├── js/             # Lógica del lado del cliente (Fetch API)
│   └── css/            # Estilos del sistema
└── requirements.txt    # Librerías necesarias
Un paso importante: Crear el requirements.txt
Para que otros puedan correr tu programa fácilmente, genera el archivo de requerimientos. Con tu venv activo, corre este comando en la terminal:

Bash

pip freeze > backend/requirements.txt
Esto guardará las versiones exactas de Flask, Pandas, SQLAlchemy y demás en un archivo de texto.

## 🗄️ Base de Datos (MySQL)

El sistema utiliza una base de datos relacional con las siguientes tablas principales:
* **usuarios**: Almacena credenciales (hashes), roles (admin/operador) y estado.
* **productos**: Gestión de stock, códigos de barras (EAN-13 corregidos) y fechas de caducidad.
* **alertas**: Registro de notificaciones automáticas por stock bajo o proximidad de vencimiento.