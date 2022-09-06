from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class Usuarios(Base):
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    apelido = Column(String, unique=True, index=True)
    nome = Column(String)
    sobrenome = Column(String)
    senha_hashed = Column(String)
    ativo =Column(Boolean, default=True)

    livros = relationship("Livros", back_populates="dono")


class Livros(Base):
    __tablename__ = "livros"
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String)
    autor = Column(String)
    descricao = Column(String)
    prioridade = Column(Integer)
    lido = Column(Boolean, default=False)
    dono_id = Column(Integer, ForeignKey("usuarios.id"))

    dono = relationship("Usuarios", back_populates="livros")