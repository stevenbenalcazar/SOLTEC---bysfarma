from flask import Blueprint, request, jsonify
from database import db
from models.usuario import Usuario

usuarios_bp = Blueprint("usuarios", __name__)


@usuarios_bp.route("/usuarios", methods=["GET"])
def listar_usuarios():
    usuarios = Usuario.query.all()

    data = []
    for u in usuarios:
        data.append({
            "id": u.id_usuario,
            "nombre": u.nombre,
            "correo": u.correo,
            "rol": u.rol,
            "estado": u.estado
        })

    return jsonify(data)


@usuarios_bp.route("/usuarios", methods=["POST"])
def crear_usuario():
    data = request.json

    if not data:
        return jsonify({"message": "Datos no enviados"}), 400

    if Usuario.query.filter_by(correo=data["correo"]).first():
        return jsonify({"message": "Correo ya registrado"}), 400

    usuario = Usuario(
        nombre=data["nombre"],
        correo=data["correo"],
        password=data["password"],
        rol=data.get("rol", "empleado"),
        estado=True
    )
    usuario.set_password(data["password"])  # guardar hash
    db.session.add(usuario)
    db.session.commit()

    return jsonify({"message": "Usuario creado correctamente"}), 201


@usuarios_bp.route("/usuarios/<int:id>/estado", methods=["PUT"])
def cambiar_estado_usuario(id):
    usuario = Usuario.query.get_or_404(id)
    usuario.estado = not usuario.estado
    db.session.commit()

    return jsonify({
        "message": "Estado actualizado",
        "estado": usuario.estado
    })
