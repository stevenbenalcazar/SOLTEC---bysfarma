import os
import re
from flask import Blueprint, request, jsonify
from models import Producto
from dotenv import load_dotenv
from google import genai

load_dotenv()

chatbot_bp = Blueprint("chatbot", __name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    mensaje = data.get("mensaje", "").lower().strip()

    if not mensaje:
        return jsonify({"respuesta": "No se recibió ninguna consulta."})

    # -------------------------------------------------
    # 1️⃣ Extraer palabras clave del mensaje
    # -------------------------------------------------
    palabras = re.findall(r"\b[a-záéíóúñ]+\b", mensaje)

    # -------------------------------------------------
    # 2️⃣ Buscar productos relacionados en BD
    # -------------------------------------------------
    productos_encontrados = []

    for palabra in palabras:
        resultados = Producto.query.filter(
            Producto.nombre.ilike(f"%{palabra}%")
        ).all()
        productos_encontrados.extend(resultados)

    # Eliminar duplicados usando PK real
    productos_encontrados = {
        p.id_producto: p for p in productos_encontrados
    }.values()

    # -------------------------------------------------
    # 3️⃣ Construir contexto dinámico
    # -------------------------------------------------
    contexto_inventario = ""

    if productos_encontrados:
        for p in productos_encontrados:
            contexto_inventario += (
                f"Producto: {p.nombre}\n"
                f"Stock actual: {p.stock}\n"
                f"Precio: ${p.precio}\n"
                f"Fecha de caducidad: {p.fecha_caducidad or 'No registrada'}\n\n"
            )
    else:
        # Resumen general real (NO inventado)
        productos = Producto.query.order_by(Producto.stock.asc()).limit(20).all()

        contexto_inventario = "Resumen del inventario (productos con menor stock):\n\n"
        for p in productos:
            contexto_inventario += (
                f"- {p.nombre}: Stock {p.stock}\n"
            )

    # -------------------------------------------------
    # 4️⃣ Prompt profesional para IA
    # -------------------------------------------------
    prompt_sistema = f"""
Eres el asistente inteligente de SOLTEC, un sistema de gestión de inventarios farmacéuticos.

Tienes acceso a información REAL del inventario de la farmacia.

Datos del inventario:
{contexto_inventario}

Instrucciones estrictas:
- Responde solo usando los datos proporcionados.
- Si el producto existe, indica su stock real.
- Si el stock es bajo, sugiere reabastecimiento.
- Si el producto no existe, indícalo claramente.
- Usa un lenguaje profesional, ejecutivo y claro.
- No inventes información.

Pregunta del usuario:
"{mensaje}"
"""

    # -------------------------------------------------
    # 5️⃣ Llamada a IA (controlada)
    # -------------------------------------------------
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_sistema
        )
        respuesta = response.text

    except Exception as e:
        print("ERROR IA:", e)
        respuesta = "No pude analizar el inventario en este momento."

    return jsonify({"respuesta": respuesta})
