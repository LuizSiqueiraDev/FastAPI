from fastapi import FastAPI
from pydantic import BaseModel
import models

app = FastAPI()


class CriarUsuario(BaseModel):
    apelido: str
    email: str|None = None
    nome: str
    sobrenome: str
    senha: str


@app.post("/criar/usuario")
async def criar_usuario(criar_usuario: CriarUsuario):
    modelo = models.Usuarios()
    modelo.email = criar_usuario.email
    modelo.apelido = criar_usuario.apelido
    modelo.nome = criar_usuario.nome
    modelo.sobrenome = criar_usuario.sobrenome
    modelo.senha_hashed = criar_usuario.senha
    modelo.ativo = True

    return modelo