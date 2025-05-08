from pydantic import BaseModel


class Pedido_Has_ItemBase(BaseModel):
    ID_Pedido: int
    ID_Item: int
    Quantidade: int
    Ativo: bool


class ItemBase(BaseModel):
    ID: int
    Nome: str
    Descricao: str
    Categoria: str
    Preco: float
    Ativo: bool
