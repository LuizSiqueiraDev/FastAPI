from fastapi import FastAPI
from database import engine
import models
from routers import autorizacao, livros, usuarios, enderecos
from starlette.staticfiles import StaticFiles
from starlette import status
from starlette.responses import RedirectResponse

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return RedirectResponse(url="/livros", status_code=status.HTTP_302_FOUND)


app.include_router(autorizacao.router)
app.include_router(usuarios.router)
app.include_router(enderecos.router)
app.include_router(livros.router)