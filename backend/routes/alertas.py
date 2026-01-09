from flask import Blueprint, jsonify
from database import db
from models import Producto, Alerta
from datetime import date

alertas_bp = Blueprint("alertas", __name__)

@alertas_bp.route("/alertas", methods=["GET"])
def obtener_alertas():
    alertas = Alerta.query.all()
    data = []

    for a in alertas:
        data.append({
            "id": a.id_alerta,
            "tipo": a.tipo,
            "descripcion": a.descripcion,
            "estado": a.estado,
            "fecha": str(a.fecha)
        })

    return jsonify(data)


@alertas_bp.route("/alertas/generar", methods=["GET"])
def generar_alertas():
    productos = Producto.query.all()

    for p in productos:
        if p.stock <= 2:
            alerta = Alerta(
                tipo="Stock Bajo",
                descripcion=f"El producto {p.nombre} tiene stock bajo",
                estado="activa"
            )
            db.session.add(alerta)

        if p.fecha_caducidad and p.fecha_caducidad <= date.today():
            alerta = Alerta(
                tipo="Producto Caducado",
                descripcion=f"El producto {p.nombre} está caducado",
                estado="activa"
            )
            db.session.add(alerta)

    db.session.commit()
    return jsonify({"message": "Alertas generadas correctamente"})
