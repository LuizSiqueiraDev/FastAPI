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


@app.post("/adicionar")
async def adicionar_livro(titulo: str, autor: str):
    id_atual = 0

    if len(LIVROS) > 0:
        for livro in LIVROS:
            proximo_id = int(livro.split("_")[-1])
            if proximo_id > id_atual:
                id_atual = proximo_id
    
    LIVROS[f'livro_{id_atual + 1}'] = {'titulo': titulo, 'autor': autor}
    return LIVROS[f'livro_{id_atual + 1}']


@app.put("/atualizar")
async def atualizar_livro(nome_livro: str, titulo: str, autor: str):
    novos_dados = {'titulo': titulo, 'autor': autor}
    LIVROS[nome_livro] = novos_dados
    return novos_dados