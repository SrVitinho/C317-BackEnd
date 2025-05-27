from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, UploadFile, Form
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from DataBase import engine, SessionLocal
from keys import link
import models
from sqlalchemy import extract
from datetime import datetime

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

@router.get("/get/ativos")
async def get_Pedidos(db: db_dependency):
    total = db.query(models.Pedido).filter(models.Pedido.Status == "Pagamento").count()
    return total

@router.get("/get/pendentes")
async def get_Pendentes(db: db_dependency):
    total = db.query(models.Pedido).filter(or_(models.Pedido.Status == "Pendente", models.Pedido.Status == "Aprovado")).count()
    return total

@router.get("/get/thisMonth")
async def get_pedidos_mes_atual(db: db_dependency):
    current_year = datetime.now().year
    current_month = datetime.now().month

    total_pedidos = db.query(models.Pedido).filter(
        extract('year', models.Pedido.Data_Evento) == current_year,
        extract('month', models.Pedido.Data_Evento) == current_month
    ).count()

    return {total_pedidos}


