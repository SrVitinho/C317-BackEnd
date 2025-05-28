from pydantic import BaseModel


class PedidoBase(BaseModel):
    ID_Comprador: int
    Num_Convidado: int
    Nome_Evento: str
    Horario_Inicio: str
    Horario_Fim: str
    Data_Evento: str
    Data_Compra: str
    Status: str

class PedidoResponse(BaseModel):
    Preço: float 

class PackageBase(BaseModel):
    id_pacote: int 
    Nome_Evento: str
    Horario_Inicio: str
    Horario_Fim: str
    Data_Evento: str

class PackageResponse(BaseModel):
    id_item: int
    quantidade: int
    nome: str
    categoria: str
