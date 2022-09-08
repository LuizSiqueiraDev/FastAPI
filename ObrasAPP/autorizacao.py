from fastapi import FastAPI, Depends
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models


class CriarUsuario(BaseModel):
    apelido: str
    email: str|None = None
    nome: str
    sobrenome: str
    senha: str


app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)


def obter_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def obter_senha_hash(senha):
    return bcrypt_context.hash(senha)


@app.post("/criar/usuario")
async def criar_usuario(criar_usuario: CriarUsuario, db: Session = Depends(obter_db)):
    modelo = models.Usuarios()
    modelo.email = criar_usuario.email
    modelo.apelido = criar_usuario.apelido
    modelo.nome = criar_usuario.nome
    modelo.sobrenome = criar_usuario.sobrenome

    senha_hash = obter_senha_hash(criar_usuario.senha)
    modelo.senha_hashed = senha_hash
    
    modelo.ativo = True

    db.add(modelo)
    db.commit()