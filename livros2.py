from fastapi import FastAPI

app = FastAPI()

LIVROS = []


@app.get("/")
async def mostrar_livros():
    return LIVROS