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

