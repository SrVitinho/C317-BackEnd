from pydantic import BaseModel

class ItemBase(BaseModel):
    Nome: str
    Descricao: str
    Categoria: str
    Preco: float
    Ativo: bool


class ItemBase(BaseModel):
    Nome: str
    Descricao: str
    Categoria: str
    Preco: float
    Ativo: bool