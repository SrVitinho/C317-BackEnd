from fastapi import FastAPI, HTTPException, Depends, status, APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from User.userBase import UserBase, UserResponse, UserUpdate, UserUpdateADM
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from DataBase import engine, SessionLocal
from models import *
from typing import List
from auth import get_current_user


router = APIRouter(
    prefix='/users',
    tags=['users']
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

@router.get('/get/me', response_model=UserResponse, status_code=status.HTTP_200_OK)
async def get_logged_user(db: db_dependency, user: User = Depends(get_current_user)):
    return user


@router.post('/create/', status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: db_dependency):
    db_user = User(
        userName=user.userName,
        password=bcrypt_context.hash(user.password),
        Email=user.Email,
        role="Cliente",
        NumCel=user.NumCel,
        Ativo = True
    )
    db.add(db_user)
    db.commit()

    db_user.password="N/A"

    return db_user

@router.get("/all", response_model=List[UserResponse], status_code=status.HTTP_200_OK)
async def get_all_users(db: db_dependency):
    user = db.query(User).filter().all()
    if len(user) == 0:
        raise HTTPException(status_code=404, detail="No User found in DB")
    return user

@router.get("/protected-route")
def protected_route(user: User = Depends(get_current_user)):
    return f"Hello, {user.Email}"

@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK)
def read_user(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.ID == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/update/", status_code=status.HTTP_202_ACCEPTED)
async def update_user(userUPT: UserUpdate, db: db_dependency):
    
    user = read_user(userUPT.ID, db)

    user.userName = userUPT.userName
    user.NumCel = userUPT.NumCel

    db.add(user)
    db.commit()

@router.put("/update/Adm/Role", status_code=status.HTTP_202_ACCEPTED)
async def update_role(userUPT: UserUpdateADM, db: db_dependency):
    user = read_user(userUPT.ID, db)
    
    user.role = userUPT.role
    user.userName = userUPT.userName
    user.NumCel = userUPT.NumCel

    db.add(user)
    db.commit()  

@router.put("/toogle/Status", status_code=status.HTTP_202_ACCEPTED)
async def toogle_roles(user_id: int, db: db_dependency):
    user = db.query(User).filter(User.ID == user_id).first()
    print(user.Ativo)
    if user.Ativo == True:
        user.Ativo = False
        db.add(user)
        db.commit()
        return "User Ativo changed to False"
    
    elif not user.Ativo:
        user.Ativo = True
        db.add(user)
        db.commit()
        return "User Ativo changed to True"
    
    raise status.HTTP_422_UNPROCESSABLE_ENTITY



