from sqlalchemy import Boolean, Column, Integer, String, Date, Time, Float
from DataBase import Base

class User(Base):
    __tablename__ = 'user'

    ID = Column(Integer, primary_key=True, index=True)
    userName = Column(String(128))
    Email = Column(String(128), index=True, unique=True)
    password = Column(String(300))
    role = Column(String(300))
    NumCel = Column(String(15))
    Ativo = Column(Boolean, index=True)

class Pedido(Base):
    __tablename__ = 'Pedido'
    ID = Column(Integer, primary_key=True, index=True)
    ID_Comprador = Column(Integer, index=True)
    Num_Convidado = Column(Integer)
    Nome_Evento = Column(String(255), index=True)
    Horario_Inicio = Column(Time)
    Horario_Fim = Column(Time)
    Preço = Column(Float)
    Status = Column(String(255))
    Ativo = Column(Boolean, index=True)
    Data_Evento = Column(Date)
    Data_Compra = Column(Date)

class Item(Base):
    __tablename__ = 'Item'
    ID = Column(Integer, primary_key=True, index=True)
    Nome = Column(String(255))
    Descricao = Column(String(500))
    Categoria = Column(String(255))
    Preco = Column(Float)
    Ativo = Column(Boolean, index=True)

class Pedido_Has_Item(Base):
    __tablename__ = 'Pedido_Has_Item'
    ID = Column(Integer, primary_key=True, index=True)
    ID_Pedido = Column(Integer, index=True)
    ID_Item = Column(Integer, index=True)
    Quantidade = Column(Integer, index=True)
    Ativo = Column(Boolean, index=True)
