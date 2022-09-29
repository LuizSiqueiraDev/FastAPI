import sys
sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Depends, APIRouter, Request, Form
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import Field
import models
from routers.autorizacao import obter_excecao_do_usuario, obter_usuario_atual
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/livros",
    tags=["Livros"],
    responses={404: {"descrição": "Não encontrado"}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")


def obter_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get("/", response_class=HTMLResponse)
async def mostrar_usuarios(request: Request, db: Session = Depends(obter_db)):
    livros = db.query(models.Livros).filter(models.Livros.dono_id == 1).all()

    return templates.TemplateResponse("home.html", {"request": request, "livros": livros})


@router.get("/adicionar-livro", response_class=HTMLResponse)
async def adicionar_novo_livro(request: Request):
    return templates.TemplateResponse("adicionar-livro.html", {"request": request})


@router.post("/adicionar-livro", response_class=HTMLResponse)
async def adicionar_livro(request: Request, titulo: str = Form(), autor: str = Form(), descricao: str = Form(), prioridade: int = Form(), db: Session = Depends(obter_db)):
    livro_modelo = models.Livros()
    livro_modelo.titulo = titulo
    livro_modelo.autor = autor
    livro_modelo.descricao = descricao
    livro_modelo.prioridade = prioridade
    livro_modelo.lido = False
    livro_modelo.dono_id = 1

    db.add(livro_modelo)
    db.commit()

    return RedirectResponse(url="/livros", status_code=status.HTTP_302_FOUND)


@router.get("/editar-livro/{livro_id}", response_class=HTMLResponse)
async def editar_livro(request: Request, livro_id: int, db: Session = Depends(obter_db)):
    livro = db.query(models.Livros).filter(models.Livros.id == livro_id).first()

    return templates.TemplateResponse("editar-livro.html", {"request": request, "livro": livro})


@router.post("/editar-livro/{livro_id}", response_class=HTMLResponse)
async def editar_livro_commit(livro_id: int, titulo: str = Form(), autor: str = Form(), descricao: str = Form(), prioridade: int = Form(), db: Session = Depends(obter_db)):
    modelo_livro = db.query(models.Livros).filter(models.Livros.id == livro_id).first()

    modelo_livro.titulo = titulo
    modelo_livro.autor = autor
    modelo_livro.descricao = descricao
    modelo_livro.prioridade = prioridade

    db.add(modelo_livro)
    db.commit()

    return RedirectResponse(url="/livros", status_code=status.HTTP_302_FOUND)


@router.get("/deletar/{livro_id}")
async def deletar_livro(livro_id: int, db: Session = Depends(obter_db)):
    modelo = db.query(models.Livros).filter(models.Livros.id == livro_id).filter(models.Livros.dono_id == 1).first()

    if modelo is None:
        return RedirectResponse(url="/livros", status_code=status.HTTP_302_FOUND)
    
    db.query(models.Livros).filter(models.Livros.id == livro_id).delete()
    db.commit()

    return RedirectResponse(url="/livros", status_code=status.HTTP_302_FOUND)


@router.get("/lido/{livro_id}", response_class=HTMLResponse)
async def livro_lido(livro_id: int, db: Session = Depends(obter_db)):
    livro = db.query(models.Livros).filter(models.Livros.id == livro_id).first()

    livro.lido = not livro.lido

    db.add(livro)
    db.commit()

    return RedirectResponse(url="/livros", status_code=status.HTTP_302_FOUND)