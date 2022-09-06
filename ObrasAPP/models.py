from email.policy import default
from sqlalchemy import Boolean, Column, Integer, String
from database import Base


class Livros(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)
    descricao = Column(String)
    prioridade = Column(Integer)
    lido = Column(Boolean, default=False)