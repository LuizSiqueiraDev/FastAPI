from fastapi import FastAPI
from pydantic import BaseModel
from uuid import UUID

app = FastAPI()


class Livro(BaseModel):
    id: UUID
    titulo: str
    autor: str
    descricao: str
    avaliacao: int


LIVROS = []


@app.get("/")
async def mostrar_livros():
    return LIVROS