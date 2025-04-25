from fastapi import FastAPI, HTTPException, Depends, status
import pymysql
from pydantic import BaseModel
from typing import Annotated
import auth
import models
from models import *
from DataBase import engine, SessionLocal
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from keys import SECRET_KEY
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], #for debug reasons, pending corrrection
    allow_headers=["*"],
)

ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)

# needs further refactoring for better code practices
class UserBase(BaseModel):
    userName: str
    Email: str
    password: str
    role: str
    NumCel: str


class PedidoBase(BaseModel):
    ID_Comprador: int
    Num_Convidado: int
    Nome_Evento: str
    Horario_Inicio: str
    Horario_Fim: str
    Preco: float
    Status: str
    Ativo: bool
    Data_Evento: str
    Data_Compra: str


class Pedido_Has_ItemBase(BaseModel):
    ID_Pedido: int
    ID_Item: int
    Quantidade: int
    Ativo: bool


class UserResponse(BaseModel):
    id: int
    userName: str
    Email: str
    role: str
    NumCel: str

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    ID: int
    Nome: str
    Descricao: str
    Categoria: str
    Preco: float
    Ativo: bool


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.post('/users/create/', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = User(
        userName=user.userName,
        password=bcrypt_context.hash(user.password),
        Email=user.Email,
        role=user.role,
        NumCel=user.NumCel
    )
    db.add(db_user)
    db.commit()

@app.post('/Item/create/', status_code=status.HTTP_201_CREATED)
async def create_Item(item: ItemBase, db: db_dependency):
    db_Item = models.User(**item.dict())
    db.add(db_Item)
    db.commit()


@app.get("/users/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
async def read_user(user_id: int, db: db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/item/{item_id}", status_code=status.HTTP_200_OK)
async def read_item(item_id: int, db: db_dependency):
    user = db.query(models.Item).filter(models.Item.id == item_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return user


@app.get("/")
async def root():
    return {"message": "Hello World"}
