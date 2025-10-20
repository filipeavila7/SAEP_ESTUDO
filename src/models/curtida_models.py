from src import db
from sqlalchemy import Integer, ForeignKey, Column, Boolean


class Curtida(db.Model):
    __tablename__ = "curtida"
    id = Column(Integer, primary_key=True, autoincrement=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id"), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id"), nullable=False)
    curtida = Column(Boolean, default=False) 