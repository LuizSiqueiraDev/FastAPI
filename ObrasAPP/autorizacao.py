from fastapi import FastAPI
from pydantic import BaseModel
from passlib.context import CryptContext
import models

app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CriarUsuario(BaseModel):
    apelido: str
    email: str|None = None
    nome: str
    sobrenome: str
    senha: str


def obter_senha_hash(senha):
    return bcrypt_context.hash(senha)


@app.post("/criar/usuario")
async def criar_usuario(criar_usuario: CriarUsuario):
    modelo = models.Usuarios()
    modelo.email = criar_usuario.email
    modelo.apelido = criar_usuario.apelido
    modelo.nome = criar_usuario.nome
    modelo.sobrenome = criar_usuario.sobrenome

    senha_hash = obter_senha_hash(criar_usuario.senha)
    modelo.senha_hashed = senha_hash
    
    modelo.ativo = True

    return modelo