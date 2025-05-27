from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, UploadFile, Form
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func
from DataBase import engine, SessionLocal
from keys import link
import models

router = APIRouter(
    prefix='/dash',
    tags=['dash']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/get/receita", status_code=status.HTTP_200_OK)
async def get_Receita(db: db_dependency):
    total = db.query(func.sum(models.Pedido.Preço)).filter(models.Pedido.Status == "Pagamento").scalar()
    return total
