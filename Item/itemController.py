from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from User.userBase import UserBase, UserResponse
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import models 
from Item.itemBase import ItemBase 
from DataBase import engine, SessionLocal

router = APIRouter(
    prefix='/item',
    tags=['item']
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.post('/create/', status_code=status.HTTP_201_CREATED)
async def create_Item(item: ItemBase, db: db_dependency):
    db_Item = models.Item(**item.dict())
    db.add(db_Item)
    db.commit()


@router.get("/{item_id}", status_code=status.HTTP_200_OK)
async def read_item(item_id: int, db: db_dependency):
    user = db.query(models.Item).filter(models.Item.id == item_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return user