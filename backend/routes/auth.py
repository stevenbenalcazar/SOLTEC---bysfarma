from flask import Blueprint, request, jsonify
from models.usuario import Usuario, bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json

    if not data:
        return jsonify({"message": "Datos no enviados"}), 400

    correo = data.get("correo")
    password = data.get("password")

    if not correo or not password:
        return jsonify({"message": "Correo y contraseña requeridos"}), 400

    # Buscar usuario por correo
    usuario = Usuario.query.filter_by(correo=correo, estado=True).first()

    # Validar contraseña con hash
    if not usuario or usuario.password != password:
        return jsonify({"message": "Credenciales incorrectas"}), 401

    return jsonify({
        "message": "Login exitoso",
        "usuario": {
            "id": usuario.id_usuario,
            "nombre": usuario.nombre,
            "correo": usuario.correo,
            "rol": usuario.rol
        }
    })