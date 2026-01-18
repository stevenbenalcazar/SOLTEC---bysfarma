from flask import Blueprint, request, jsonify
from models import db, Producto
from datetime import datetime

productos_bp = Blueprint("productos", __name__)

@productos_bp.route("/productos", methods=["POST"])
def crear_producto():
    data = request.json

    producto = Producto(
        nombre=data["nombre"],
        categoria=data["categoria"],
        stock=data["stock"],
        stock_minimo=data["stock_minimo"],
        precio=data["precio"],
        lote=data["lote"],
        fecha_caducidad=datetime.strptime(
            data["fecha_caducidad"], "%Y-%m-%d"
        ) if data.get("fecha_caducidad") else None
    )

    db.session.add(producto)
    db.session.commit()

    return jsonify({
        "message": "Producto creado",
        "id": producto.id
    }), 201