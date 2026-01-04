import os

class Config:
    # Reemplaza 'root' y 'tu_contraseña' con tus credenciales de MySQL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:7733@localhost/soltec_inventario'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'clave_secreta_para_sesiones'