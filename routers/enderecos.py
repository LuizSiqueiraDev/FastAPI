import sys
sys.path.append("..")

from starlette import status
from starlette.responses import RedirectResponse
from fastapi import Depends, APIRouter, Request, Form
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models
from routers.autorizacao import obter_usuario_atual
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/endereco",
    tags=["Endereço"],
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


@router.get("/visualizar", response_class=HTMLResponse)
async def dados_do_usuario(request: Request, db: Session = Depends(obter_db)):
    usuario = await obter_usuario_atual(request)
    if usuario is None:
        return RedirectResponse(url="/autorizacao", status_code=status.HTTP_302_FOUND)

    enderecos = db.query(models.Enderecos).filter(models.Enderecos.id == models.Usuarios.endereco_id).first() # não é usuario.get('id'), então, o quê é?

    return templates.TemplateResponse("visualizar-endereco.html", {"request": request, "usuario": usuario, "enderecos": enderecos})


@router.get("/editar-endereco/{endereco_id}", response_class=HTMLResponse)
async def editar_endereco(request: Request, endereco_id: int, db: Session = Depends(obter_db)):
    usuario = await obter_usuario_atual (request)
    if usuario is None:
        return RedirectResponse(url="/autorizacao", status_code=status.HTTP_302_FOUND)
    
    endereco = db.query(models.Enderecos).filter(models.Enderecos.id == endereco_id).first()

    return templates.TemplateResponse("editar-endereco.html", {"request": request, "endereco": endereco})


@router.post("/editar-endereco/{endereco_id}", response_class=HTMLResponse)
async def editar_endereco_commit(request: Request, endereco_id: int, 
                                                    endereco1: str = Form(), 
                                                    endereco2: str = Form(), 
                                                    cidade: str = Form(),
                                                    estado: str = Form(),
                                                    pais: str = Form(),
                                                    codigo_postal: str = Form(),
                                                    num_residencial: str = Form(),
                                                    db: Session = Depends(obter_db)):
    usuario = await obter_usuario_atual(request)
    if usuario is None:
        return RedirectResponse(url="/autorizacao", status_code=status.HTTP_302_FOUND)
    

    modelo_endereco = db.query(models.Enderecos).filter(models.Enderecos.id == endereco_id).first()

    modelo_endereco.endereco1 = endereco1
    modelo_endereco.endereco2 = endereco2
    modelo_endereco.cidade = cidade
    modelo_endereco.estado = estado
    modelo_endereco.pais = pais
    modelo_endereco.codigo_postal = codigo_postal
    modelo_endereco.num_residencial = num_residencial

    db.add(modelo_endereco)
    db.commit()

    return RedirectResponse(url="/visualizar-endereco", status_code=status.HTTP_302_FOUND)