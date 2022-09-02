from fastapi import FastAPI
from pydantic import BaseModel, Field
from uuid import UUID

app = FastAPI()


class Livro(BaseModel):
    id: UUID
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1, max_length=100)
    descricao: str|None = Field(title="Descrição do livro", min_length=1, max_length=100)
    avaliacao: int = Field(gt=-1, lt=101)


LIVROS = []


@app.get("/")
async def mostrar_livros():
    return LIVROS


@app.post("/")
async def adicionar_livro(livro: Livro):
    LIVROS.append(livro)
    return livro