from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Query
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
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

@router.post('/create/', status_code=status.HTTP_201_CREATED)
async def create_Item(pedido: PedidoBase, itens: list[ItemAdd], db: db_dependency):
    db_Pedido = Pedido(**pedido.model_dump())
    db.add(db_Pedido)
    db.commit()
    for add in itens:
        PedidoHasItensController.postHasItem(idPedido=db_Pedido.ID, idItem=add.ID, quantidade=add.quantidade, db=db) #needs further item validation, this is only an MVP
    
