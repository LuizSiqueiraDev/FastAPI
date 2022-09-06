from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def obter_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Livro(BaseModel):
    titulo: str
    autor: str
    descricao: str|None = None
    prioridade: int = Field(gt=0, lt=6, description="Prioridade entre 1-5")
    lido: bool = Field(default=False)


def excecao_http():
    return HTTPException(status_code=404, detail="Livro não encontrado.")


def status_de_confirmacao():
    return {'status': 200, 'operação': 'Sucedido'}


@app.get("/")
async def mostrar_livros(db: Session = Depends(obter_db)):
    return db.query(models.Livros).all()


@app.get("/livros/{livro_id}")
async def consultar_livro(livro_id: int, db: Session = Depends(obter_db)):
    modelo = db.query(models.Livros).filter(models.Livros.id == livro_id).first()

    if modelo is not None:
        return modelo
    raise excecao_http()


@app.post("/")
async def adicionar_livro(livro: Livro, db: Session = Depends(obter_db)):
    modelo = models.Livros()
    modelo.titulo = livro.titulo
    modelo.autor = livro.autor
    modelo.descricao = livro.descricao
    modelo.prioridade = livro.prioridade
    modelo.lido = livro.lido

    db.add(modelo)
    db.commit()

    return status_de_confirmacao()