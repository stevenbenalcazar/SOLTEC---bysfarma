from flask import Blueprint, request, jsonify
from models import Producto, Alerta, ConsultaChatbot
from database import db

chatbot_bp = Blueprint("chatbot", __name__)

@chatbot_bp.route("/chatbot", methods=["POST"])
def chatbot():
    data = request.get_json()
    mensaje = data.get("mensaje", "").lower()

    respuesta = "No entendí tu consulta 🤔"

    # 🔹 CONSULTA STOCK
    if "stock" in mensaje:
        productos = Producto.query.filter(Producto.stock <= Producto.stock_minimo).all()
        if productos:
            respuesta = "Productos con stock bajo:\n"
            for p in productos:
                respuesta += f"- {p.nombre}: {p.stock} unidades\n"
        else:
            respuesta = "No hay productos con stock bajo."

    # 🔹 CONSULTA ALERTAS
    elif "alerta" in mensaje:
        alertas = Alerta.query.filter_by(estado="activa").all()
        if alertas:
            respuesta = "Alertas activas:\n"
            for a in alertas:
                respuesta += f"- {a.descripcion}\n"
        else:
            respuesta = "No hay alertas activas."

    # 🔹 BUSCAR PRODUCTO
    elif "producto" in mensaje:
        palabras = mensaje.split()
        for palabra in palabras:
            producto = Producto.query.filter(Producto.nombre.ilike(f"%{palabra}%")).first()
            if producto:
                respuesta = (
                    f"Producto: {producto.nombre}\n"
                    f"Stock: {producto.stock}\n"
                    f"Ubicación: {producto.percha}"
                )
                break

    # Guardar historial
    consulta = ConsultaChatbot(
        pregunta=mensaje,
        respuesta=respuesta
    )
    db.session.add(consulta)
    db.session.commit()

    return jsonify({"respuesta": respuesta})
