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

    class Config:
        schema_extra = {
            "example": {
                "id": "78187ea0-6730-4e4b-a5cc-aad1622c7e06",
                "titulo": "Título do livro",
                "autor": "Nome do autor",
                "descricao": "Uma descrição qualquer",
                "avaliacao": 0
            }
        }


LIVROS = []


@app.get("/")
async def mostrar_livros(qtd_livros: int|None = None):
    if len(LIVROS) < 1:
        cadastrar_livros_sem_api()
    
    if qtd_livros and len(LIVROS) >= qtd_livros > 0:
        posicao = 1
        nova_lista = []
        while posicao <= qtd_livros:
            nova_lista.append(LIVROS[posicao - 1])
            posicao = posicao + 1
        return nova_lista
    return LIVROS


@app.post("/")
async def adicionar_livro(livro: Livro):
    LIVROS.append(livro)
    return livro


def cadastrar_livros_sem_api():
    livro_1 = Livro(
        id="78187ea0-6730-4e4b-a5cc-aad1622c7e01", 
        titulo="Título Um", 
        autor="Autor Um", 
        descricao="Descrição Um", 
        avaliacao=10
        )
    livro_2 = Livro(
        id="78187ea0-6730-4e4b-a5cc-aad1622c7e02", 
        titulo="Título Dois", 
        autor="Autor Dois", 
        descricao="Descrição Dois", 
        avaliacao=20
        )
    livro_3 = Livro(
        id="78187ea0-6730-4e4b-a5cc-aad1622c7e03", 
        titulo="Título Três", 
        autor="Autor Três", 
        descricao="Descrição Três", 
        avaliacao=30
        )
    livro_4 = Livro(
        id="78187ea0-6730-4e4b-a5cc-aad1622c7e04", 
        titulo="Título Quatro", 
        autor="Autor Quatro", 
        descricao="Descrição Quatro", 
        avaliacao=40
        )
    livro_5 = Livro(
        id="78187ea0-6730-4e4b-a5cc-aad1622c7e05", 
        titulo="Título Cinco", 
        autor="Autor Cinco", 
        descricao="Descrição Cinco", 
        avaliacao=50
        )
    LIVROS.append(livro_1)
    LIVROS.append(livro_2)
    LIVROS.append(livro_3)
    LIVROS.append(livro_4)
    LIVROS.append(livro_5)