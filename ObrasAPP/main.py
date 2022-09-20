from fastapi import FastAPI
from database import engine
import models
from routers import autorizacao, livros, usuarios
from compania import companiasapi

app = FastAPI()

models.Base.metadata.create_all(bind=engine)

app.include_router(autorizacao.router)
app.include_router(usuarios.router)
app.include_router(livros.router)
app.include_router(companiasapi.router)