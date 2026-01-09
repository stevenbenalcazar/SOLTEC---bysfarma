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
            "lote": p.lote,
            "precio": p.precio
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
        lote=data.get("lote"),
        precio=data.get("precio")
    )

    db.session.add(producto)
    db.session.commit()

    return jsonify({"message": "Producto creado correctamente"}), 201

@inventario_bp.route("/dashboard", methods=["GET"])
def dashboard_data():
    total_productos = Producto.query.count()
    stock_bajo = Producto.query.filter(Producto.stock <= 3).count()
    alertas_activas = Alerta.query.filter(Alerta.estado == "activa").count()

    return {
        "total_productos": total_productos,
        "stock_bajo": stock_bajo,
        "alertas_activas": alertas_activas
    }

@inventario_bp.route("/sync-productos", methods=["POST"])
def sync_productos():
    from models import Producto, ProductoFarmacia

    productos_farmacia = ProductoFarmacia.query.filter_by(
        estado_producto="ACTIVO"
    ).all()

    creados = 0
    actualizados = 0

    for pf in productos_farmacia:
        nombre_pf = pf.pro_nompro.strip().lower()
        lote_pf = (pf.lote or "").strip()

        producto = Producto.query.filter(
            db.func.lower(Producto.nombre) == nombre_pf,
            Producto.lote == lote_pf
        ).first()

        if producto:
            producto.stock = pf.cantidad_stock
            producto.fecha_caducidad = pf.fecha_caducidad
            producto.precio = pf.precio
            actualizados += 1
        else:
            nuevo = Producto(
                nombre=pf.pro_nompro.strip(),
                categoria=pf.age_nombre,
                stock=pf.cantidad_stock,
                stock_minimo=10,
                fecha_caducidad=pf.fecha_caducidad,
                lote=pf.lote,
                precio=pf.precio
            )
            db.session.add(nuevo)
            creados += 1

    db.session.commit()

    return jsonify({
        "message": "Sincronización completada",
        "creados": creados,
        "actualizados": actualizados
    })
