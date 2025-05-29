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
        "back_urls": {
            "success": "https://confianopai.com/login",
            "failure": "http://127.0.0.1:8000/",
            "pending": "http://127.0.0.1:8000/"
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
    status = payment_info = sdk.payment().get(id)

    return status

