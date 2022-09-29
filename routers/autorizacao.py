import sys
sys.path.append(".. ")

from starlette.responses import RedirectResponse
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response
from pydantic import BaseModel
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal, engine
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
import models
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

SECRET_KEY = "klgh6azydegwd288to79i3vtht8wp7"
ALGORITHM = "HS256"

templates = Jinja2Templates(directory="templates")


class CriarUsuario(BaseModel):
    apelido: str
    email: str|None = None
    nome: str
    sobrenome: str
    senha: str
    telefone: str|None


router = APIRouter(
    prefix="/autorizacao",
    tags=["Autorização"],
    responses={401: {"usuario": "Não autorizado"}}
)


class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: str|None
        self.password: str|None
    
    async def autorizacao_form(self):
        form = await self.request.form()
        self.username = form.get("email")
        self.password = form.get("senha")


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
            raise obter_excecao_do_usuario()
        return {"apelido": apelido, "id": usuario_id}
    except JWTError:
        raise obter_excecao_do_usuario() 


@router.post("/criar/usuario")
async def criar_usuario(criar_usuario: CriarUsuario, db: Session = Depends(obter_db)):
    modelo = models.Usuarios()
    modelo.email = criar_usuario.email
    modelo.apelido = criar_usuario.apelido
    modelo.nome = criar_usuario.nome
    modelo.sobrenome = criar_usuario.sobrenome
    modelo.telefone = criar_usuario.telefone

    senha_hash = obter_senha_hash(criar_usuario.senha)
    modelo.senha_hashed = senha_hash
    
    modelo.ativo = True

    db.add(modelo)
    db.commit()


@router.post("/token")
async def login_para_acesso_de_token(response: Response, dados_form: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(obter_db)):
    usuario = autenticar_usuario(dados_form.username, dados_form.password, db)

    if not usuario:
        return False
    expirar_token = timedelta(minutes=60)
    token = criar_acesso_token(usuario.apelido, usuario.id)

    response.set_cookie(key="criar_acesso_token", value=token, httponly=True)

    return True


@router.get("/", response_class=HTMLResponse)
async def pagina_de_autenticacao(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: Session = Depends(obter_db)):
    try:
        formulario = LoginForm(request)
        await formulario.autorizacao_form()
        response = RedirectResponse(url="/livros", status_code=status.HTTP_302_FOUND)

        validar_cookie = await login_para_acesso_de_token(response=response, dados_form=formulario, db=db)

        if not validar_cookie:
            mensagem = "Apelido ou senha incorreto"
            return templates.TemplateResponse("login.html", {"request": request, "mensagem": mensagem})
        return response
    except HTTPException:
        mensagem = "Erro desconhecido"
        return templates.TemplateResponse("login.html", {"request": request, "mensagem": mensagem})

@router.get("/registrar", response_class=HTMLResponse)
async def registrar(request: Request):
    return templates.TemplateResponse("registrar.html", {"request": request})


#Exeções

def obter_excecao_do_usuario():
    excecao_de_credencial = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return excecao_de_credencial


def token_de_excecao():
    resposta_de_token_de_excecao = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Usuário ou senha incorreto",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return resposta_de_token_de_excecao