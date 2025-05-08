from pydantic import BaseModel


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
