from src import db
from sqlalchemy import Column, Integer, ForeignKey, Text


class Comentario(db.Model):
    __tablename__ = "comentario"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    texto = Column(Text, nullable=False)