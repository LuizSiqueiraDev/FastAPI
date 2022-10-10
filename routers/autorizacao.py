import sys
sys.path.append(".. ")

from starlette.responses import RedirectResponse
from fastapi import Depends, HTTPException, status, APIRouter, Request, Response, Form
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


async def obter_usuario_atual(request: Request):
    try:
        token = request.cookies.get("criar_acesso_token")
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        apelido: str = payload.get("sub")
        usuario_id: int = payload.get("id")
        if apelido is None or usuario_id is None:
            logout(request)
        return {"apelido": apelido, "id": usuario_id}
    except JWTError:
        raise HTTPException(status_code=404, detail="Não encontrado.")


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


@router.get("/logout")
async def logout(request: Request):
    mensagem = "Logout realizado com sucesso"
    response = templates.TemplateResponse("login.html", {"request": request, "mensagem": mensagem})
    response.delete_cookie(key="criar_acesso_token")
    return response


@router.get("/registrar", response_class=HTMLResponse)
async def registrar(request: Request):
    return templates.TemplateResponse("registrar.html", {"request": request})


@router.post("/registrar", response_class=HTMLResponse)
async def registrar_usuario(request: Request, email: str = Form(), apelido: str = Form(), nome: str = Form(), sobrenome: str = Form(), 
                                senha: str = Form(), senha2: str = Form(), db: Session = Depends(obter_db)):
    
    validacao1 = db.query(models.Usuarios).filter(models.Usuarios.apelido == apelido).first()
    
    validacao2 = db.query(models.Usuarios).filter(models.Usuarios.email == email).first()

    if senha != senha2 or validacao1 is not None or validacao2 is not None:
        mensagem = "Requisição de registro inválida!"
        return templates.TemplateResponse("registrar.html", {"request": request, "mensagem": mensagem})

    modelo = models.Usuarios()
    modelo.apelido = apelido
    modelo.email = email
    modelo.nome = nome
    modelo.sobrenome = sobrenome
    senha_hash = obter_senha_hash(senha)
    modelo.senha_hashed = senha_hash
    modelo.ativo = True

    db.add(modelo)
    db.commit()

    mensagem = "Registro cruado com sucesso!"
    return templates.TemplateResponse("login.html", {"request": request, "mensagem": mensagem})