from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
import models 
from HasItens.hasItensBase import Pedido_Has_ItemBase 
from DataBase import engine, SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]


class PedidoHasItensController:
    def postHasItem(idPedido, idItem, quantidade, db: db_dependency):
        db_HasItem = models.Pedido_Has_Item(
                ID_Pedido = idPedido,
                ID_Item = idItem,
                Quantidade = quantidade,
                Ativo = 1
        )
        db.add(db_HasItem)
        db.commit()
        
                
        
