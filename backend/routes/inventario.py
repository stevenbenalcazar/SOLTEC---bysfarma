from flask import Blueprint, request, jsonify
from database import db
from models import Producto, Alerta

inventario_bp = Blueprint("inventario", __name__)


@inventario_bp.route("/productos", methods=["GET"])
def obtener_productos():
    productos = Producto.query.all()
    data = []

    for p in productos:
        data.append({
            "id": p.id_producto,
            "nombre": p.nombre,
            "categoria": p.categoria,
            "stock": p.stock,
            "stock_minimo": p.stock_minimo,
            "fecha_caducidad": str(p.fecha_caducidad),
            "lote": p.lote
        })

    return jsonify(data)


@inventario_bp.route("/productos", methods=["POST"])
def crear_producto():
    data = request.json

    producto = Producto(
        nombre=data["nombre"],
        categoria=data.get("categoria"),
        stock=data["stock"],
        stock_minimo=data["stock_minimo"],
        fecha_caducidad=data["fecha_caducidad"],
        lote=data.get("lote")
    )

    db.session.add(producto)
    db.session.commit()

    return jsonify({"message": "Producto creado correctamente"}), 201

@inventario_bp.route("/dashboard", methods=["GET"])
def dashboard_data():
    total_productos = Producto.query.count()
    stock_bajo = Producto.query.filter(Producto.stock <= 5).count()
    alertas_activas = Alerta.query.filter(Alerta.estado == "activa").count()

    return {
        "total_productos": total_productos,
        "stock_bajo": stock_bajo,
        "alertas_activas": alertas_activas
    }
