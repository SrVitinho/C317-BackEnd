from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, UploadFile, Form
from fastapi.params import File
from fastapi.responses import FileResponse
from typing import Annotated
from sqlalchemy.orm import Session
from User.userBase import UserBase, UserResponse
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import models
from Item.itemBase import ItemBase
from DataBase import engine, SessionLocal
from PIL import Image
from keys import link

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
async def create_Item(db: Session = Depends(get_db), Nome: str = Form(...), Descricao: str = Form(...), Categoria: str = Form(...), Preco: float = Form(...), Ativo: bool = Form(...), image: UploadFile = File(...)):
    db_Item = models.Item(
        Nome=Nome,
        Descricao=Descricao,
        Categoria=Categoria,
        Preco=Preco,
        Ativo=Ativo
    )

    try:
        file = Image.open(image.file)

    except Exception as err:
        raise HTTPException(status_code=406, detail="The image file is not valid")

    db.add(db_Item)
    db.commit()
    db.refresh(db_Item)

    filePath = "imagens/" + str(db_Item.ID) + ".png"
    file.save(filePath)

    return "Item saved with success"


@router.get("/getImage/{item}", status_code=status.HTTP_201_CREATED)
async def get_image(item: int):
    image_path = "imagens/" + str(item) + ".png"
    return FileResponse(image_path, media_type="image/png")

@router.get("/all", status_code=status.HTTP_200_OK)
async def get_all_itens(db: db_dependency):
    users = db.query(models.Item).filter(models.Item.Ativo == True).all()

    if len(users) == 0:
        raise HTTPException(status_code=404, detail="No User found in DB")
    
    AllResponses = []

    for user in users:
        response = read_item(user.ID, db)
        AllResponses.append(response)

    formattedResponse = {"Itens": AllResponses}
    return formattedResponse


@router.get("/{item_id}", status_code=status.HTTP_200_OK)
def read_item(item_id: int, db: db_dependency):
    item = db.query(models.Item).filter(models.Item.ID == item_id).first()

    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    URL = link + f"item/getImage/{item_id}"

    Response = {
        "item": {
            "ID": item.ID,
            "Descricao": item.Descricao,
            "Categoria": item.Categoria,
            "Preco": item.Preco,
            "Ativo": item.Ativo
        },
        "imageURL": URL
    }

    return Response
