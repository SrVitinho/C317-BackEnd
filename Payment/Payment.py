import requests
from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, UploadFile, Form
from Payment.PaymentBase import itemPayment
import models
from DataBase import engine, SessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
from auth import get_current_user
from keys import MercadoPagoKey
import mercadopago

from models import User

router = APIRouter(
    prefix='/payment',
    tags=['payment']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@router.get("/getPayment", status_code=status.HTTP_200_OK)
async def get_payment(id: int, db: db_dependency, current_user: User = Depends(get_current_user)):
    pedido = db.query(models.Pedido).filter(models.Pedido.ID == id).first()

    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido not found")

    if pedido.ID_Comprador != current_user.ID:
        raise HTTPException(status_code=403, detail="No id found for this user")

    if pedido.Status != "Pagamento":
        raise HTTPException(status_code=403, detail="The payment is not allowed for this Pedido")

    listItens = []

    itens = db.query(models.Pedido_Has_Item).filter(models.Pedido_Has_Item.ID_Pedido == id).all()

    for item in itens:
        db_Item = db.query(models.Item).filter(models.Item.ID == item.ID_Item).first()
        listItens.append({"id": db_Item.ID, "title": db_Item.Nome, "quantity": item.Quantidade, "currency": "BRL",
                          "unit_price": (db_Item.Preco * 1.4)})

    sdk = mercadopago.SDK(MercadoPagoKey)

    payment_data = {
        "items": listItens,
        "external_reference": str(pedido.ID),
        "back_urls": {
            "success": "https://elodrinks.confianopai.com/pagamento/aprovado",
            "failure": "https://elodrinks.confianopai.com/pagamento/reprovado",
            "pending": "https://elodrinks.confianopai.com/pagamento/pendente"
        },
        "auto_return": "all"
    }

    result = sdk.preference().create(payment_data)
    payment = result["response"]
    print(payment)
    link = payment["init_point"]
    return {"payment_url": link}


@router.put("/status", status_code=status.HTTP_200_OK)
async def update_Status_Pagamento(id: int):
    sdk = mercadopago.SDK(MercadoPagoKey)
    payment_info = sdk.payment().get(id)
    status = payment_info["response"]["status"]
    print(payment_info["response"])
    if status == "approved":
        print("a")
    return payment_info["response"]["status"]


def busca_pagamento_por_external_reference(external_reference: str, db: db_dependency):
    sdk = mercadopago.SDK(MercadoPagoKey)
    search_result = sdk.payment().search({"external_reference": external_reference})
    print(search_result["response"]["results"])
    try:
        status = search_result["response"]["results"][0]["status"]
    except Exception as err:
        return 0
    else:
        if status == "approved":
            pedido = db.query(models.Pedido).filter(models.Pedido.ID == int(external_reference)).first()
            pedido.Status = "Aprovado"
            db.add(pedido)
            db.commit()
            return 1
        return 0
