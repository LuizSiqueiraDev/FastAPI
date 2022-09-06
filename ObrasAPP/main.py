from fastapi import FastAPI, Depends, HTTPException
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def obter_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def excecao_http():
    return HTTPException(status_code=404, detail="Livro não encontrado.")


@app.get("/")
async def mostrar_livros(db: Session = Depends(obter_db)):
    return db.query(models.Livros).all()


@app.get("/livros/{livro_id}")
async def consultar_livro(livro_id: int, db: Session = Depends(obter_db)):
    modelo = db.query(models.Livros).filter(models.Livros.id == livro_id).first()

    if modelo is not None:
        return modelo
    raise excecao_http()