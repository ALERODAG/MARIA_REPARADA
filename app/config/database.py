from multiprocessing import connection
import os 
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()


# Contruir la URL de conexión a la base de datos MySQL usando variables de entorno

DATABASE_URL = os.getenv(
    "DATABASE_URL",  
    f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")


#Motor de SQLAlchemy para conectarse a la base de datos MySQL
engine = create_engine(
    DATABASE_URL, 
    pool_recycle=3600,  # Reciclamos la conexión cada hora
    pool_size=10, # Mantiene 10 conexiones abiertas en el pool
    max_overflow=20,  # Permitir hasta 20 conexiones adicionales si el pool está lleno
    pool_pre_ping=True  # Habilitamos el ping para verificar la conexión antes de usarla
)

# Configuramos la fabrica de declaraciones de sesiones
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

# definir la clase base para modelos declarativos
Base = declarative_base()


# Generadord de dependencias para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


try:
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))  # Ejecutamos una consulta simple para verificar la conexión
        print(f"Conexión a la base de datos {os.getenv('DB_NAME')} exitosa.")

        
except Exception as e:
    print(f"Error al conectar a la base de datos {os.getenv('DB_NAME')}: {e}")

