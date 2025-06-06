from pydantic import BaseModel


class UserBase(BaseModel):
    userName: str
    Email: str
    password: str
    NumCel: str

class UserUpdate(BaseModel):
    ID: int
    userName: str
    NumCel: str

class UserUpdateADM(BaseModel):
    ID: int
    userName: str
    NumCel: str
    role: str

class UserResponse(BaseModel):
    ID: int
    userName: str
    Email: str
    role: str
    NumCel: str
    Ativo: bool

    class Config:
        orm_mode = True

