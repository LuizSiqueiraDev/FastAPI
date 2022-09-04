from fastapi import FastAPI
from database import engine
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


@app.get("/")
async def criar_database():
    return {"Database": "Criada"}