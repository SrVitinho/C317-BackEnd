from pydantic import BaseModel

class ItemBase(BaseModel):
    ID: int
    Nome: str
    Descricao: str
    Categoria: str
    Preco: float
    Ativo: bool