from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
import models

SECRET_KEY = "klgh6azydegwd288to79i3vtht8wp7"
ALGORITHM = "HS256"


class CriarUsuario(BaseModel):
    apelido: str
    email: str|None = None
    nome: str
    sobrenome: str
    senha: str


app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

models.Base.metadata.create_all(bind=engine)

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="token")


def obter_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def obter_senha_hash(senha):
    return bcrypt_context.hash(senha)


def verificar_senha(senha_simples, senha_hashed):
    return bcrypt_context.verify(senha_simples, senha_hashed)


def autenticar_usuario(alcunha: str, senha: str, db):
    usuario = db.query(models.Usuarios).filter(models.Usuarios.apelido == alcunha).first()

    if not usuario:
        return False
    if not verificar_senha(senha, usuario.senha_hashed):
        return False
    return usuario


def criar_acesso_token(apelido: str, usuario_id: int, expirar_delta: timedelta|None = None):
    codificar = {"sub": apelido, "id": usuario_id}

    if expirar_delta:
        expirar = datetime.utcnow() + expirar_delta
    else:
        expirar = datetime.utcnow() + timedelta(minutes=30)
    codificar.update({"exp": expirar})
    return jwt.encode(codificar, SECRET_KEY, algorithm=ALGORITHM)


async def obter_usuario_atual(token: str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        apelido: str = payload.get("sub")
        usuario_id: int = payload.get("id")
        if apelido is None or usuario_id is None:
            raise excecao_http()
        return {"apelido": apelido, "id": usuario_id}
    except JWTError:
        raise excecao_http() 


def excecao_http():
    return HTTPException(status_code=404, detail="Usuário'' não encontrado.")


@app.post("/criar/usuario")
async def criar_usuario(criar_usuario: CriarUsuario, db: Session = Depends(obter_db)):
    modelo = models.Usuarios()
    modelo.email = criar_usuario.email
    modelo.apelido = criar_usuario.apelido
    modelo.nome = criar_usuario.nome
    modelo.sobrenome = criar_usuario.sobrenome

    senha_hash = obter_senha_hash(criar_usuario.senha)
    modelo.senha_hashed = senha_hash
    
    modelo.ativo = True

    db.add(modelo)
    db.commit()


@app.post("/token")
async def login_para_acesso_de_token(dados_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(obter_db)):
    usuario = autenticar_usuario(dados_form.username, dados_form.password, db)

    if not usuario:
        raise excecao_http()
    expirar_token = timedelta(minutes=30)
    token = criar_acesso_token(usuario.apelido, usuario.id)

    return {"token": token}