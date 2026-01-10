import os

class Config:
    # Reemplaza 'root' y 'tu_contraseña' con tus credenciales de MySQL
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:7733@localhost/soltec_inventario'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'clave_secreta_para_sesiones'

    # --- Configuración de correo ---
MAIL_SERVER = "smtp.gmail.com"
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = "tucorreo@gmail.com"
MAIL_PASSWORD = "CLAVE_DE_APLICACION"
MAIL_DEFAULT_SENDER = "SOLTEC <tucorreo@gmail.com>"
