from pydantic import BaseModel


class Pedido_Has_ItemBase(BaseModel):
    ID_Pedido: int
    ID_Item: int
    Quantidade: int
    Ativo: bool

class ItemAdd(BaseModel):
    ID: int
    quantidade: int
