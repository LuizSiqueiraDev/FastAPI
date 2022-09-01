from fastapi import FastAPI

app = FastAPI()

LIVROS = {
    'livro_1': {'titulo': 'Título Um', 'autor': 'Autor Um'},
    'livro_2': {'titulo': 'Título Dois', 'autor': 'Autor Dois'},
    'livro_3': {'titulo': 'Título Três', 'autor': 'Autor Três'},
    'livro_4': {'titulo': 'Título Quatro', 'autor': 'Autor Quatro'},
    'livro_5': {'titulo': 'Título Cinco', 'autor': 'Autor Cinco'},
}


@app.get("/")
async def mostrar_livros():
    return LIVROS


@app.get("/pular")
async def pular_livro(pular: str):
    if pular:
        nova_lista = LIVROS.copy()
        del nova_lista[pular]
        return nova_lista
    return LIVROS