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


@app.get("/livro/{livro_id}")
async def encontrar_livro(livro_id: UUID):
    for livro in LIVROS:
        if livro.id == livro_id:
            return livro


@app.get("/")
async def mostrar_livros(retornar_qtd: int|None = None):
    if len(LIVROS) < 1:
        cadastrar_livros_sem_api()
    
    if retornar_qtd and len(LIVROS) >= retornar_qtd > 0:
        indice = 1
        nova_lista = []
        while indice <= retornar_qtd:
            nova_lista.append(LIVROS[indice - 1])
            indice = indice + 1
        return nova_lista
    return LIVROS


@app.post("/")
async def adicionar_livro(livro: Livro):
    LIVROS.append(livro)
    return livro


@app.put("/{livro_id}")
async def atualizar_livro(livro_id: UUID, livro: Livro):
    indice = 0

    for l in LIVROS:
        indice += 1
        if l.id == livro_id:
            LIVROS[indice - 1] = livro
            return LIVROS[indice - 1]


@app.delete("/{livro_id}")
async def deletar_livro(livro_id: UUID):
    indice = 0
    for livro in LIVROS:
        indice += 1
        if livro.id == livro_id:
            del LIVROS[indice - 1]
            return f'ID: {livro_id} deletado.'


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