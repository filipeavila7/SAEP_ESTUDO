from src import db
from sqlalchemy import Column, Integer, String, Boolean
from flask_login import UserMixin

class Usuario(db.Model, UserMixin):
    __tablename__ = 'usuario'

    id = Column(Integer, primary_key=True, autoincrement=True )
    nome = Column(String(120), nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    senha = Column(String(120), nullable=False)

    