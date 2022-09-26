from fastapi import APIRouter, Depends
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models
from .autorizacao import obter_excecao_do_usuario, obter_usuario_atual, verificar_senha, obter_senha_hash

router = APIRouter(
    prefix="/usuarios",
    tags=["Usuários"],
    responses={404: {"descrição": "Não encontrado"}}
)

models.Base.metadata.create_all(bind=engine)

def obter_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


class VerificacaoDoUsuario(BaseModel):
    apelido: str
    senha: str
    nova_senha: str


@router.get("/")
async def mostrar_usuarios(db: Session = Depends(obter_db)):
    return db.query(models.Usuarios).all()


@router.get("/{usuario_id}")
async def pesquisar_usuario(usuario_id: int, db: Session = Depends(obter_db)):
    modelo = db.query(models.Usuarios).filter(models.Usuarios.id == usuario_id).first()

    if modelo is not None:
        return modelo
    return "ID do usuário inválido!"


@router.put("/senha")
async def mudar_senha(verificacao_do_usuario: VerificacaoDoUsuario, usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(obter_db)):
    if usuario is None:
        raise obter_excecao_do_usuario()
    
    modelo = db.query(models.Usuarios).filter(models.Usuarios.id == usuario.get("id")).first()

    if modelo is not None:
        if verificacao_do_usuario.apelido == modelo.apelido and verificar_senha(verificacao_do_usuario.senha, modelo.senha_hashed):
            modelo.senha_hashed = obter_senha_hash(verificacao_do_usuario.nova_senha)
            db.add(modelo)
            db.commit()
            return "Sucesso"
    return "Usuário ou requisição inválida"


@router.delete("/deletar")
async def deletar_usuario(usuario: dict = Depends(obter_usuario_atual), db: Session = Depends(obter_db)):
    if usuario is None:
        raise obter_excecao_do_usuario()
    
    modelo = db.query(models.Usuarios).filter(models.Usuarios.id == usuario.get("id")).first()

    if modelo is None:
        return "Usuario ou requisição inválida"

    db.query(models.Usuarios).filter(models.Usuarios.id == usuario.get("id")).delete()
    db.commit()
    return "Deletado com sucesso"    