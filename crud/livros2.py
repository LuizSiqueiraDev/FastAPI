from fastapi import FastAPI, HTTPException, Request, status, Form, Header
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse

app = FastAPI()


class ExcecaoDeNumeroNegativo(Exception):
    def __init__(self, qtd_negativa):
        self.qtd_negativa = qtd_negativa


class Livro(BaseModel):
    id: UUID
    titulo: str = Field(min_length=1)
    autor: str = Field(min_length=1, max_length=100)
    descricao: None|str = Field(title="Descrição do livro", min_length=1, max_length=100)
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


class LivroSemAvaliacao(BaseModel):
    id: UUID
    titulo: str = Field(min_length=1, max_length=100)
    autor: str
    descricao: None|str = Field(None, title="Descrição", min_length=1, max_length=100)


LIVROS = []


@app.exception_handler(ExcecaoDeNumeroNegativo)
async def excecao_de_numero_negativo(reques: Request, excecao: ExcecaoDeNumeroNegativo):
    return JSONResponse(
        status_code=420,
        content={"mensagem": f"O valor {excecao.qtd_negativa} é inválido, só valores positivos."}
    )


@app.get("/header")
async def ler_header(header: None|str = Header(None)):
    return {"Header": header}


@app.get("/livro/{livro_id}")
async def encontrar_livro(livro_id: UUID):
    for livro in LIVROS:
        if livro.id == livro_id:
            return livro
    raise excecao_de_livro_nao_encontrado()


@app.get("/livro/avaliacao/{livro_id}", response_model=LivroSemAvaliacao)
async def encontrar_livro_sem_avaliacao(livro_id: UUID):
    for livro in LIVROS:
        if livro.id == livro_id:
            return livro
    raise excecao_de_livro_nao_encontrado()


@app.get("/")
async def mostrar_livros(retornar_qtd: int|None = None):
    if retornar_qtd and retornar_qtd < 0:
        raise ExcecaoDeNumeroNegativo(qtd_negativa=retornar_qtd)
    
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


@app.post("/", status_code=status.HTTP_201_CREATED)
async def adicionar_livro(livro: Livro):
    LIVROS.append(livro)
    return livro


@app.post("/livros/login")
async def login(livro_id: int, nome_usuario: None|str = Header(None), senha: None|str = Header(None)):
    if nome_usuario == "FastAPIUser" and senha == "test1234!":
        return LIVROS[livro_id]
    return "Usuário inválido!"


@app.put("/{livro_id}")
async def atualizar_livro(livro_id: UUID, livro: Livro):
    indice = 0

    for l in LIVROS:
        indice += 1
        if l.id == livro_id:
            LIVROS[indice - 1] = livro
            return LIVROS[indice - 1]
    raise excecao_de_livro_nao_encontrado()


@app.delete("/{livro_id}")
async def deletar_livro(livro_id: UUID):
    indice = 0
    for livro in LIVROS:
        indice += 1
        if livro.id == livro_id:
            del LIVROS[indice - 1]
            return f'ID: {livro_id} deletado.'
    raise excecao_de_livro_nao_encontrado()


def excecao_de_livro_nao_encontrado():
    return HTTPException(
        status_code=404,
        detail="Livro não encontrado.",
        headers={"X-Header-Error": "UUID não contrado."}
    )


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