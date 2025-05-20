from pydantic import BaseModel


class UserBase(BaseModel):
    userName: str
    Email: str
    password: str
    role: str
    NumCel: str


class UserResponse(BaseModel):
    id: int
    userName: str
    Email: str
    role: str
    NumCel: str

    class Config:
        orm_mode = True
