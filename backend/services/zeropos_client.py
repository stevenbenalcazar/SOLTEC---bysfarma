import pymysql
from config import Config

def get_zeropos_connection():
    return pymysql.connect(
        host=Config.ZEROPOS_DB_HOST,
        user=Config.ZEROPOS_DB_USER,
        password=Config.ZEROPOS_DB_PASS,
        database=Config.ZEROPOS_DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )
