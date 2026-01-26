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
    from models import Producto
    from datetime import date, timedelta

    hoy = date.today()
    limite = hoy + timedelta(days=30)

    productos = Producto.query.all()

    total_productos = len(productos)
    stock_critico = 0
    stock_bajo = 0
    por_caducar = 0
    caducados = 0

    for p in productos:
        stock_min = p.stock_minimo or 0

        # 🔴 Crítico
        if p.stock <= 2:
            stock_critico += 1

        # 🟠 Bajo (pero no crítico)
        if 2 < p.stock <= stock_min:
            stock_bajo += 1

        # 🔥 Caducado
        if p.fecha_caducidad and p.fecha_caducidad <= hoy:
            caducados += 1

        # 🟡 Próximo a caducar
        if p.fecha_caducidad and hoy < p.fecha_caducidad <= limite:
            por_caducar += 1

    alertas_activas = stock_critico + stock_bajo + por_caducar + caducados

    return {
        "total_productos": total_productos,
        "stock_critico": stock_critico,
        "stock_bajo": stock_bajo,
        "por_caducar": por_caducar,
        "caducados": caducados,
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
            producto.codigo_barra = pf.pro_codbar

            actualizados += 1
        else:
            nuevo = Producto(
                nombre=pf.pro_nompro.strip(),
                categoria=pf.age_nombre,
                stock=pf.cantidad_stock,
                stock_minimo=10,
                fecha_caducidad=pf.fecha_caducidad,
                lote=pf.lote,
                precio=pf.precio,
                codigo_barra=pf.pro_codbar
            )
            db.session.add(nuevo)
            creados += 1

    db.session.commit()

    return jsonify({
        "message": "Sincronización completada",
        "creados": creados,
        "actualizados": actualizados
    })

@inventario_bp.route("/productos/<int:id>", methods=["PUT"])
def actualizar_producto(id):
    from models import Producto, Movimiento
    data = request.json

    producto = Producto.query.get_or_404(id)

    # Actualizar campos
    stock_anterior = producto.stock or 0

    if "stock" in data:
        producto.stock = int(data["stock"])

    if "stock_minimo" in data:
        producto.stock_minimo = int(data["stock_minimo"])

    if "fecha_caducidad" in data:
        producto.fecha_caducidad = data["fecha_caducidad"]

    if "precio" in data:
        producto.precio = float(data["precio"])

        # Registrar movimiento (entrada/salida) basado en diferencia de stock
    if "stock" in data and "usuario_id" in data:
        stock_anterior = producto.stock or 0
        stock_nuevo = int(data["stock"])
        delta = stock_nuevo - stock_anterior

        if delta != 0:
            movimiento = Movimiento(
                id_producto=id,
                tipo="entrada" if delta > 0 else "salida",
                cantidad=abs(delta),
                fecha=db.func.now()
            )
            db.session.add(movimiento)

    db.session.commit()

    return jsonify({"message": "Producto actualizado correctamente"})

@inventario_bp.route("/stock-minimo/recalcular", methods=["POST"])
def recalcular_stock_minimo():
    from models import Producto, Movimiento
    from datetime import datetime, timedelta

    # Parámetros TOC (puedes moverlos a config.py luego)
    TR = 7   # tiempo de reposición (días)
    TP = 1   # tiempo de procesamiento (días)
    TT = 1   # tiempo de transporte (días)
    INC = 0.20  # 20% incertidumbre

    VENTANA_DIAS = 7  # demanda semanal (últimos 7 días)

    # Top (tiempo óptimo en días)
    TOP = (TR + TP + TT) * (1 + INC)

    desde = datetime.now() - timedelta(days=VENTANA_DIAS)

    productos = Producto.query.all()
    actualizados = 0

    for p in productos:
        # sumatoria de salidas del producto en la ventana
        total_salidas = db.session.query(db.func.sum(Movimiento.cantidad)).filter(
            Movimiento.id_producto == p.id_producto,
            Movimiento.tipo == "salida",
            Movimiento.fecha >= desde
        ).scalar()

        total_salidas = total_salidas or 0

        # venta diaria promedio
        venta_diaria = total_salidas / VENTANA_DIAS

        # Inventario óptimo (stock mínimo sugerido)
        stock_minimo_calculado = int(round(venta_diaria * TOP))
        if stock_minimo_calculado < 0:
            stock_minimo_calculado = 0

        p.stock_minimo = stock_minimo_calculado
        actualizados += 1

    db.session.commit()

    return jsonify({
        "message": "Stock mínimo recalculado correctamente",
        "top_dias": TOP,
        "ventana_dias": VENTANA_DIAS,
        "productos_actualizados": actualizados
    })