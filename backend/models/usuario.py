from database import db
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

class Usuario(db.Model):
    __tablename__ = "usuarios"

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    estado = db.Column(db.Boolean, default=True)

    # Guardar contraseña hasheada
    def set_password(self, plain_password):
        self.password = bcrypt.generate_password_hash(plain_password).decode('utf-8')

    # Verificar contraseña
    def check_password(self, plain_password):
        return bcrypt.check_password_hash(self.password, plain_password)
