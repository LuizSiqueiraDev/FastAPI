import sys
from urllib import response
sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Depends, APIRouter, Request, Form
import models
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
from .autorizacao import obter_usuario_atual, verificar_senha, obter_senha_hash
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
    responses={404: {"descrição": "Não encontrado."}}
)

models.Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

def obter_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class VerificarUsuario(BaseModel):
    apelido: str
    senha: str
    nova_senha: str


@router.get("/editar-senha", response_class=HTMLResponse)
async def editar_usuario(request: Request):
    usuario = await obter_usuario_atual(request)
    if usuario is None:
        return RedirectResponse(url="/autorizacao", status_code=status.HTTP_302_FOUND)
    
    return templates.TemplateResponse("editar-usuario-senha.html", {"request": request, "usuario": usuario})


@router.post("/editar-senha", response_class=HTMLResponse)
async def trocar_senha(request: Request, apelido: str = Form(), senha1: str = Form(), senha2: str = Form(), db: Session = Depends(obter_db)):
    usuario = await obter_usuario_atual(request)

    if usuario is None:
        return RedirectResponse(url="/autorizacao", status_code=status.HTTP_302_FOUND)
    
    dados_usuario = db.query(models.Usuarios).filter(models.Usuarios.apelido == apelido).first()

    mensagem = "Usuario ou senha inválido."

    if dados_usuario is not None:
        if apelido == dados_usuario.apelido and verificar_senha(senha1, dados_usuario.senha_hashed):
            dados_usuario.senha_hashed = obter_senha_hash(senha2)
            db.add(dados_usuario)
            db.commit()
            mensagem = "Senha atualizada."

        return templates.TemplateResponse("editar-usuario-senha.html", {"request": request, "usuario": usuario, "mensagem": mensagem})  