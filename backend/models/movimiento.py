from database import db
from datetime import datetime

class Movimiento(db.Model):
    __tablename__ = "movimientos"

    id_movimiento = db.Column(db.Integer, primary_key=True)
    id_producto = db.Column(
        db.Integer,
        db.ForeignKey("productos.id_producto"),
        nullable=False
    )
    tipo = db.Column(db.Enum("entrada", "salida"), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Movimiento {self.tipo} - {self.cantidad}>"
