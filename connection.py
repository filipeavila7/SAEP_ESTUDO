from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine


HOST='127.0.0.1'
PORT='3306'
USER='root'
DB='petamigos'
SQLALCHEMY_DATABASE_URI =f"mysql+pymysql://{USER}@{HOST}/{DB}"
SQLALCHEMY_TRACK_MODIFICATIONS = False




engine = create_engine(
    SQLALCHEMY_DATABASE_URI
)

try:
    connection = engine.connect()
    print("banco conectado")

except Exception as e:
    print(f"falha ao conectar {e}")