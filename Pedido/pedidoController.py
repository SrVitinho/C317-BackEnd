from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Query
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
from Pedido.pedidoBase import PedidoBase
from DataBase import engine, SessionLocal
from HasItens.hasItensBase import ItemAdd
from HasItens.hasItensController import PedidoHasItensController
from models import *

router = APIRouter(
    prefix='/pedido',
    tags=['pedido']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

PedidoHasItensControllerClass = PedidoHasItensController


def getOrcamento(itens: list, db: db_dependency):
    if type(itens) is not list:
        return -1
    price = 0
    for item in itens:
        aux = db.query(models.Item).filter(models.Item.ID == item.ID).first()
        price += aux.Preco * item.quantidade

    price *= 1.4  # Margem mínima de 20% de lucro. Valor completamente aleatório

    return price


@router.post('/create/', status_code=status.HTTP_201_CREATED)
async def create_Item(pedido: PedidoBase, itens: list[ItemAdd], db: db_dependency):
    db_Pedido = Pedido(**pedido.model_dump())
    db_Pedido.Status = "Pendente"
    db_Pedido.Ativo = 1

    orcamentoPreco = getOrcamento(itens, db)

    if orcamentoPreco == -1:
        raise HTTPException(status_code=406, detail="Invalid itens")

    db_Pedido.Preço = orcamentoPreco
    db.add(db_Pedido)
    db.commit()

    for add in itens:
        PedidoHasItensController.postHasItem(idPedido=db_Pedido.ID, idItem=add.ID, quantidade=add.quantidade, db=db)
