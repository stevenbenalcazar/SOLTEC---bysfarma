import os
from flask import Blueprint, request, jsonify
from models import Producto, Alerta, ConsultaChatbot
from database import db
from datetime import date
from dotenv import load_dotenv
from google import genai

load_dotenv()

chatbot_bp = Blueprint("chatbot", __name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

PALABRAS_IA = [
    "caducar", "caducan", "vencer", "vence",
    "recomendación", "recomendar",
    "qué hacer", "estrategia", "promoción"
]


@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    mensaje = data.get("mensaje", "").lower()

    usar_ia = any(p in mensaje for p in PALABRAS_IA)

    # 🔹 1. Obtener productos en alerta (máx 10, ordenados por urgencia)
    productos_alerta = Producto.query.filter(
        Producto.fecha_caducidad.isnot(None),
        Producto.fecha_caducidad >= date.today()
    ).order_by(Producto.fecha_caducidad.asc()).limit(10).all()


    if not productos_alerta:
        return jsonify({"respuesta": "No hay productos próximos a caducar."})

    # 🔹 2. Preparar resumen limpio (NO todo el inventario)
    resumen = []
    for p in productos_alerta:

        dias = (p.fecha_caducidad - date.today()).days

        resumen.append(
            f"{p.nombre} (vence en {dias} días, stock: {p.stock})"
        )

    resumen_texto = "\n".join(resumen)

    # 🔹 3. Si NO se necesita IA
    if not usar_ia:
        respuesta = (
            "Productos próximos a caducar:\n" +
            "\n".join(f"- {r}" for r in resumen)
        )
    else:
        # 🔹 4. Usar IA SOLO aquí
        prompt = f"""
Eres un asistente experto en gestión de inventario farmacéutico.

Productos próximos a caducar:
{resumen_texto}

El usuario pregunta:
"{mensaje}"

Responde en el siguiente formato:

📦 Productos más urgentes:
- Nombre (días restantes)

💡 Recomendaciones:
- Estrategia concreta (descuento, promoción, rotación)

⚠️ Tono profesional y claro.
"""

        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            respuesta = response.text
        except Exception as e:
            print("ERROR IA:", e)
            respuesta = "⚠️ Error al conectar con la IA."

    # 🔹 5. Guardar historial
    db.session.add(ConsultaChatbot(
        pregunta=mensaje,
        respuesta=respuesta
    ))
    db.session.commit()

    return jsonify({"respuesta": respuesta})