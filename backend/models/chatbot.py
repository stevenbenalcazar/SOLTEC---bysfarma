from database import db
from datetime import datetime

class ConsultaChatbot(db.Model):
    __tablename__ = "consultas_chatbot"

    id_consulta = db.Column(db.Integer, primary_key=True)
    pregunta = db.Column(db.Text, nullable=False)
    respuesta = db.Column(db.Text, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<ConsultaChatbot>"
