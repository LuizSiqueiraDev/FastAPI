import sys
sys.path.append("...")

from fastapi import APIRouter, Depends, HTTPException
import models
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from pydantic import BaseModel
from .autorizacao import obter_usuario_atual

router = APIRouter(
    prefix="/enderecos",
    tags=["Endereços"],
    responses={404: {"descrição": "Não encontrado"}}
)


def obter_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class Endereco(BaseModel):
    endereco1: str
    endereco2: str|None
    cidade: str
    estado: str
    pais: str
    codico_postal: str
    num_residencial: int|None
    

@router.post("/")
async def adicionar_endereco(endereco: Endereco, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(obter_db)):
    if usuario is None:
        raise HTTPException(status_code=404, detail="Não encontrado.")
    
    modelo = models.Enderecos()
    modelo.endereco1 = endereco.endereco1
    modelo.endereco2 = endereco.endereco2
    modelo.cidade = endereco.cidade
    modelo.estado = endereco.estado
    modelo.pais = endereco.pais
    modelo.codigo_postal = endereco.codico_postal
    modelo.num_residensial = endereco.num_residencial

    db.add(modelo)
    db.flush()

    m_usuario = db.query(models.Usuarios).filter(models.Usuarios.id == usuario.get("id")).first()
    m_usuario.endereco_id = modelo.id

    db.add(m_usuario)
    db.commit()