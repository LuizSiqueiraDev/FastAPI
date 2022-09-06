from fastapi import FastAPI, Depends
from database import engine, SessionLocal
from sqlalchemy.orm import Session
import models

app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def obter_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@app.get("/")
async def mostrar_obras(db: Session = Depends(obter_db)):
    return db.query(models.Obras).all()