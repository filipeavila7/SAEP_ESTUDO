from src import db
from sqlalchemy import Column, Integer, String

class Post(db.Model):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome_post = Column(String(120), nullable=False)

