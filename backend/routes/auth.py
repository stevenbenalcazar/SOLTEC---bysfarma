from flask import Blueprint, request, jsonify
from models.usuario import Usuario

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    usuario = Usuario.query.filter_by(
        correo=data.get("correo"),
        password=data.get("password")
    ).first()

    if usuario:
        return jsonify({
            "message": "Login exitoso",
            "usuario": {
                "id": usuario.id_usuario,
                "nombre": usuario.nombre,
                "rol": usuario.rol
            }
        })

    return jsonify({"message": "Credenciales incorrectas"}), 401
