from flask import Blueprint, jsonify
from database import db
from models import Producto
from datetime import datetime
from zeropos_client import get_zeropos_connection

zeropos_bp = Blueprint("zeropos", __name__)

@zeropos_bp.route("/zeropos/sync-ventas", methods=["POST"])
def sync_ventas():
    # 1) traer ventas nuevas desde Zero POS
    conn = get_zeropos_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT id_venta, codigo_barra, cantidad, fecha
            FROM TABLA_VENTAS
            WHERE fecha >= NOW() - INTERVAL 1 DAY
        """)
        ventas = cur.fetchall()

    conn.close()

    actualizados = 0

    # 2) descontar stock en tu tabla productos
    for v in ventas:
        codigo = str(v["codigo_barra"]).strip()
        cantidad = int(v["cantidad"])

        # Buscar producto por codigo_barra si lo tienes,
        # si no, por nombre o por campo que uses.
        producto = Producto.query.filter_by(codigo_barra=codigo).first()
        if not producto:
            continue

        producto.stock = max(0, (producto.stock or 0) - cantidad)
        actualizados += 1

    db.session.commit()

    return jsonify({"message": "Sync ventas OK", "productos_actualizados": actualizados})