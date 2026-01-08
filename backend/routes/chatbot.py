import os # Importante para leer variables del sistema
from flask import Blueprint, request, jsonify
from models import Producto, Alerta, ConsultaChatbot
from database import db
import google.generativeai as genai 
from datetime import datetime
from dotenv import load_dotenv # Nueva importación
chatbot_bp = Blueprint("chatbot", __name__)

# 🔑 CONFIGURACIÓN SEGURA
# Ahora la clave se lee de forma oculta
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-pro')

@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    mensaje = data.get("mensaje", "").lower()

    # 1. Obtener contexto de la base de datos para la IA
    # Buscamos productos con stock bajo o próximos a caducar
    productos_alerta = Producto.query.filter(
        (Producto.stock <= Producto.stock_minimo) | 
        (Producto.fecha_caducidad <= datetime.now())
    ).all()

    # Creamos un resumen de inventario para que la IA sepa de qué habla
    contexto_inventario = ""
    for p in productos_alerta:
        contexto_inventario += f"- {p.nombre}: Stock {p.stock}, Caduca el {p.fecha_caducidad}\n"

    # 2. Lógica de respuesta
    try:
        # Prompt especializado para no gastar tokens en tonterías
        prompt = f"""
        Eres un experto en gestión de inventarios y ventas para SOLTEC.
        Datos actuales de productos en alerta:
        {contexto_inventario}
        
        Pregunta del usuario: {mensaje}
        
        Instrucciones:
        - Si pregunta por ventas/recomendaciones, usa los datos de arriba para dar estrategias (descuentos, combos).
        - Si pregunta algo general, responde brevemente.
        - Formato: Usa negritas y puntos para scannability.
        """

        response = model.generate_content(prompt)
        respuesta = response.text

    except Exception as e:
        # Fallback si falla la API o no hay internet
        respuesta = "Lo siento, tengo problemas para conectarme con mi cerebro de IA, pero puedo ayudarte con el stock básico."

    # 3. Guardar historial en la base de datos
    nueva_consulta = ConsultaChatbot(
        pregunta=mensaje,
        respuesta=respuesta
    )
    db.session.add(nueva_consulta)
    db.session.commit()

    return jsonify({"respuesta": respuesta})