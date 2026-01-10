import os
from flask import Blueprint, request, jsonify
from models import Producto
from database import db
from datetime import date
from dotenv import load_dotenv
from google import genai

load_dotenv()

chatbot_bp = Blueprint("chatbot", __name__)
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    mensaje = data.get("mensaje", "").lower()

    # 1. Obtener una visión general del inventario (Top 20 productos variados)
    # Traemos productos con poco stock y productos próximos a vencer para que la IA tenga contexto
    productos = Producto.query.limit(30).all()
    
    # 2. Construir una "Base de Conocimiento" dinámica para el prompt
    contexto_inventario = ""
    for p in productos:
        estado_vencimiento = f"vence el {p.fecha_caducidad}" if p.fecha_caducidad else "sin fecha"
        contexto_inventario += f"- {p.nombre}: Stock {p.stock}, Precio ${p.precio}, {estado_vencimiento}.\n"

    # 3. El Prompt del Sistema (Aquí es donde ocurre la magia)
    prompt_sistema = f"""
Eres el asistente inteligente de SOLTEC, un sistema de gestión de inventarios.
Tienes acceso a una muestra del inventario actual:
{contexto_inventario}

Instrucciones:
1. Si el usuario pregunta por stock, revisa los datos proporcionados.
2. Si el usuario pregunta qué comprar o qué vender, actúa como un consultor de negocios.
3. Si te preguntan algo fuera de inventarios, responde amablemente que solo manejas SOLTEC.
4. Usa un tono ejecutivo, profesional y breve.

Pregunta del usuario: "{mensaje}"
"""

    try:
        # Nota: He corregido el modelo a gemini-1.5-flash que es el estándar actual
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_sistema
        )
        respuesta = response.text
    except Exception as e:
        print("ERROR IA:", e)
        respuesta = "Lo siento, tuve un problema técnico al analizar los datos de SOLTEC."

    return jsonify({"respuesta": respuesta})