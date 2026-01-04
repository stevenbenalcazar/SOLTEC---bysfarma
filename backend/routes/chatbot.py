from flask import Blueprint, request, jsonify
from database import db
from models import ConsultaChatbot, Producto

chatbot_bp = Blueprint("chatbot", __name__)


@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot():
    pregunta = request.json.get("pregunta", "").lower()
    respuesta = "No entendí la consulta."

    if "stock" in pregunta:
        productos = Producto.query.all()
        respuesta = "Stock disponible:\n"
        for p in productos:
            respuesta += f"- {p.nombre}: {p.stock} unidades\n"

    consulta = ConsultaChatbot(
        pregunta=pregunta,
        respuesta=respuesta
    )

    db.session.add(consulta)
    db.session.commit()

    return jsonify({"respuesta": respuesta})
