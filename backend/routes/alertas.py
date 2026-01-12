from flask import Blueprint, jsonify
from models import Producto
from datetime import date, timedelta

alertas_bp = Blueprint("alertas", __name__)

@alertas_bp.route("/alertas", methods=["GET"])
def obtener_alertas():
    hoy = date.today()
    limite = hoy + timedelta(days=30)

    productos = Producto.query.all()
    data = []

    for p in productos:
        fecha = str(p.fecha_caducidad) if p.fecha_caducidad else "-"
        # 🔥 Caducado
        if p.fecha_caducidad and p.fecha_caducidad <= hoy:
            data.append({
                "producto_id": p.id_producto,
                "producto": p.nombre,
                "fecha_caducidad": fecha,
                "stock": p.stock,
                "estado": "CADUCADO"
            })
            continue

        # 🟡 Próximo a caducar (30 días)
        if p.fecha_caducidad and hoy < p.fecha_caducidad <= limite:
            data.append({
                "producto_id": p.id_producto,
                "producto": p.nombre,
                "fecha_caducidad": fecha,
                "stock": p.stock,
                "estado": "PRÓXIMO A CADUCAR"
            })
            continue

        # 🔴 Stock crítico
        if p.stock == 0:
            data.append({
                "producto_id": p.id_producto,
                "producto": p.nombre,
                "fecha_caducidad": fecha,
                "stock": p.stock,
                "estado": "CRÍTICO"
            })
            continue

        # 🟠 Stock bajo
        if p.stock_minimo is not None and p.stock <= p.stock_minimo:
            data.append({
                "producto_id": p.id_producto,
                "producto": p.nombre,
                "fecha_caducidad": fecha,
                "stock": p.stock,
                "estado": "BAJO"
            })

    return jsonify(data)
