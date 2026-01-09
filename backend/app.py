from flask import Flask
from flask_cors import CORS

from config import Config
from database import db

# Importar modelos para que SQLAlchemy los registre
from models import Usuario, Producto, Movimiento, Alerta, ConsultaChatbot

# Importar rutas
from routes.inventario import inventario_bp
from routes.alertas import alertas_bp
from routes.chatbot import chatbot_bp
from routes.auth import auth_bp
from routes.usuarios import usuarios_bp
from flask_mail import Mail



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mail.init_app(app)

    # Inicializar extensiones
    db.init_app(app)
    CORS(app)

    mail = Mail()
    # Registrar blueprints
    app.register_blueprint(inventario_bp, url_prefix="/api")
    app.register_blueprint(alertas_bp, url_prefix="/api")
    app.register_blueprint(chatbot_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api")
    app.register_blueprint(usuarios_bp, url_prefix="/api")
    # Crear tablas
    with app.app_context():
        db.create_all()

    # Endpoint de salud
    @app.route("/api/health")
    def health():
        return {"status": "OK", "message": "API SOLTEC funcionando"}

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
