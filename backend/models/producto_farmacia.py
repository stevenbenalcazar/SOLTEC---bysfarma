from database import db

class ProductoFarmacia(db.Model):
    __tablename__ = "productos_farmacia"

    id = db.Column(db.Integer, primary_key=True)
    age_codigo = db.Column(db.String(20))
    age_nombre = db.Column(db.String(100))
    pro_nompro = db.Column(db.String(150))
    pro_codbar = db.Column(db.String(50))
    pro_coulco = db.Column(db.String(50))
    cantidad_stock = db.Column(db.Integer)
    fecha_elaboracion = db.Column(db.Date)
    fecha_caducidad = db.Column(db.Date)
    lote = db.Column(db.String(50))
    proveedor = db.Column(db.String(100))
    estado_producto = db.Column(db.String(30))
    percha = db.Column(db.String(50))
    precio = db.Column(db.Numeric(10, 2))