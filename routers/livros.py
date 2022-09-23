import sys
sys.path.append("..")

from fastapi import Depends, HTTPException, APIRouter, Request
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
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


class Livro(BaseModel):
    titulo: str
    autor: str
    descricao: str|None = None
    prioridade: int = Field(gt=0, lt=6, description="Prioridade entre 1-5")
    lido: bool = Field(default=False)


def excecao_http():
    return HTTPException(status_code=404, detail="Livro não encontrado.")


def status_de_confirmacao():
    return {'status': 200, 'operação': 'Sucedida'}


@router.get("/test")
async def test(request: Request):
    return templates.TemplateResponse('editar-livro.html', {"request": request})


@router.get("/")
async def mostrar_livros(db: Session = Depends(obter_db)):
    return db.query(models.Livros).all()


@router.get("/usuario")
async def mostrar_lista_do_usuario(usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(obter_db)):
    if usuario is None:
        raise obter_excecao_do_usuario()
    return db.query(models.Livros).filter(models.Livros.dono_id == usuario.get("id")).all()



@router.get("/{livro_id}")
async def consultar_livro(livro_id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(obter_db)):
    if usuario is None:
        raise obter_excecao_do_usuario()
    
    modelo = db.query(models.Livros).filter(models.Livros.id == livro_id).filter(models.Livros.dono_id == usuario.get("id")).first()

    if modelo is not None:
        return modelo
    raise excecao_http()


@router.post("/")
async def adicionar_livro(livro: Livro, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(obter_db)):
    if usuario is None: 
        raise obter_excecao_do_usuario()
    
    modelo = models.Livros()
    modelo.titulo = livro.titulo
    modelo.autor = livro.autor
    modelo.descricao = livro.descricao
    modelo.prioridade = livro.prioridade
    modelo.lido = livro.lido
    modelo.dono_id = usuario.get("id")

    db.add(modelo)
    db.commit()

    return status_de_confirmacao()


@router.put("/{livro_id}")
async def atualizar_livro(livro_id: int, livro: Livro, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(obter_db)):
    if usuario is None:
        raise obter_excecao_do_usuario()

    modelo = db.query(models.Livros).filter(models.Livros.id == livro_id).filter(models.Livros.dono_id == usuario.get("id")).first()

    if modelo is None:
        raise excecao_http()
    
    modelo.titulo = livro.titulo
    modelo.autor = livro.autor
    modelo.descricao = livro.descricao
    modelo.prioridade = livro.prioridade
    modelo.lido = livro.lido

    db.add(modelo)
    db.commit()

    return status_de_confirmacao()


@router.delete("/{livro_id}")
async def deletar_livro(livro_id: int, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(obter_db)):
    if usuario is None:
        raise obter_excecao_do_usuario()

    modelo = db.query(models.Livros).filter(models.Livros.id == livro_id).filter(models.Livros.dono_id == usuario.get("id")).first()

    if modelo is None:
        raise excecao_http()
    
    db.query(models.Livros).filter(models.Livros.id == livro_id).delete()

    db.commit()

    return status_de_confirmacao()