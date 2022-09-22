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
    telefone = Column(String)
    endereco_id = Column(Integer, ForeignKey('enderecos.id'), nullable=True)

    livros = relationship("Livros", back_populates="dono")
    enderecos = relationship("Enderecos", back_populates="endereco_usuario")


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


class Enderecos(Base):
    __tablename__ = "enderecos"
    id = Column(Integer, primary_key=True, index=True)
    endereco1 = Column(String)
    endereco2 = Column(String)
    cidade = Column(String)
    estado = Column(String)
    pais = Column(String)
    codigo_postal = Column(String)
    num_residencial = Column(Integer)

    endereco_usuario= relationship('Usuarios', back_populates="enderecos")