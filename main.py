from fastapi import FastAPI, HTTPException, Depends, status
import pymysql
from pydantic import BaseModel
from typing import Annotated
import auth
import Item.itemController as itemController
import User.userController as userController
import Pedido.pedidoController as pedidoController
import Dashboard.dashboardController as dashController
import models
from Item.itemBase import ItemBase
from User.userBase import UserBase, UserResponse
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
    allow_methods=["*"],  # for debug reasons, pending correction
    allow_headers=["*"],
)

models.Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(itemController.router)
app.include_router(userController.router)
app.include_router(pedidoController.router)
app.include_router(dashController.router)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
async def root():
    return {"message": "Hello World"}
