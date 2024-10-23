from pymongo import MongoClient
import mysql.connector
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde .env
load_dotenv()

# Configuración de MongoDB
def get_mongo_connection():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://root:password@localhost:27017/")
    client = MongoClient(mongo_uri)
    db = client["Escuela"]  # Conexión a la base de datos "escuela"
    return db

# Configuración de MySQL
def get_mysql_connection():
    db_connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=os.getenv("MYSQL_PORT", 3306),  # Asegúrate de usar el puerto correcto (3306)
        user=os.getenv("MYSQL_USER", "root"),  # Usuario root
        password=os.getenv("MYSQL_PASSWORD", "root"),  # Contraseña vacía
        database=os.getenv("MYSQL_DB", "distributed_db")  # Base de datos correcta
    )
    return db_connection