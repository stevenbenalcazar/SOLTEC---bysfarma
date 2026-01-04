from database import db
from datetime import datetime

class Alerta(db.Model):
    __tablename__ = "alertas"

    id_alerta = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(50), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)
    estado = db.Column(db.String(20), default="activa")
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Alerta {self.tipo}>"
