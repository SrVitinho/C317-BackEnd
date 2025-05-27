from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, Query
from typing import Annotated
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from auth import get_current_user
import models
from Pedido.pedidoBase import PedidoBase, PackageBase, PedidoResponse
from DataBase import engine, SessionLocal
from HasItens.hasItensBase import ItemAdd
from HasItens.hasItensController import PedidoHasItensController
from models import *
from datetime import datetime


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


@router.post('/create/', status_code=status.HTTP_201_CREATED, response_model=PedidoResponse)
def create_Pedido(pedido: PedidoBase, itens: list[ItemAdd], db: db_dependency):
    db_Pedido = Pedido(**pedido.model_dump())
    db_Pedido.Status = "Orcado"
    db_Pedido.Ativo = 1

    orcamentoPreco = getOrcamento(itens, db)

    if orcamentoPreco == -1:
        raise HTTPException(status_code=406, detail="Invalid itens")

    db_Pedido.Preço = orcamentoPreco
    db.add(db_Pedido)
    db.commit()

    for add in itens:
        PedidoHasItensController.postHasItem(idPedido=db_Pedido.ID, idItem=add.ID, quantidade=add.quantidade, db=db)

    return db_Pedido

@router.post('/update/packages/', status_code=status.HTTP_201_CREATED)
async def create_Package(db: db_dependency, Package: PackageBase, current_user: User = Depends(get_current_user)):
    day = datetime.today().strftime('%Y-%m-%d')
    if Package.id_pacote == 1:
        pedido_data = {
            "ID_Comprador": current_user.ID,
            "Num_Convidado": 100,
            "Nome_Evento": Package.Nome_Evento,
            "Horario_Inicio": Package.Horario_Inicio,
            "Horario_Fim": Package.Horario_Fim,
            "Data_Evento": Package.Data_Evento,
            "Data_Compra": day,
        }
    itens = [  # needs changes after db auto population
        ItemAdd(ID=1,quantidade=2)
    ]
    pedido = PedidoBase(**pedido_data)
    pedido = create_Pedido(pedido=(pedido), itens=itens, db=db)
    return pedido


@router.get("/all", status_code=status.HTTP_200_OK)
async def get_pedidos(db: db_dependency, current_user: User = Depends(get_current_user)):
    if current_user.role == "Cliente":
        orcamentos = db.query(models.Pedido).filter(models.Pedido.ID_Comprador == current_user.ID).all()
        return orcamentos
    
    elif current_user.role == "Administrador":
        orcamentos = db.query(models.Pedido).filter().all()
        return orcamentos
    
    raise HTTPException(status_code=404, detail="Invalid user")