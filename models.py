from sqlalchemy import Boolean, Column, Integer, String, Date, Time, Double
from DataBase import Base


class User(Base):
    __tablename__ = 'user'

    ID = Column(Integer, primary_key=True, index=True)
    userName = Column(String)
    Email = Column(String, index=True)
    password = Column(String)
    role = Column(String)
    NumCel = Column(String)
    Ativo = Column(Boolean, index=True)


class Pedido(Base):
    __tablename__ = 'Pedido'
    ID = Column(Integer, primary_key=True, index=True)
    ID_Comprador = Column(Integer, index=True)
    Num_Convidado = Column(Integer)
    Nome_Evento = Column(String, index=True)
    Horario_Inicio = Column(Time)
    Horario_Fim = Column(Time)
    Preço = Column(Double)  # Needs further refactoring
    Status = Column(String)
    Ativo = Column(Boolean, index=True)
    Data_Evento = Column(Date)
    Data_Compra = Column(Date)


class Item(Base):
    __tablename__ = 'Item'
    ID = Column(Integer, primary_key=True, index=True)
    Nome = Column(String)
    Descricao = Column(String)
    Categoria = Column(String)
    Preco = Column(Double)
    Ativo = Column(Boolean, index=True)


class Pedido_Has_Item(Base):
    __tablename__ = 'Pedido_Has_Item'
    ID = Column(Integer, primary_key=True, index=True)
    ID_Pedido = Column(Integer, index=True)
    ID_Item = Column(Integer, index=True)
    Quantidade = Column(Integer, index=True)
    Ativo = Column(Boolean, index=True)
