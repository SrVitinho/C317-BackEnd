from fastapi import FastAPI, HTTPException, Depends, status, APIRouter, UploadFile, Form
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from DataBase import engine, SessionLocal
from keys import link
import models
from sqlalchemy import extract
from datetime import datetime, timedelta

router = APIRouter(
    prefix='/dash',
    tags=['dash']
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/get/receita", status_code=status.HTTP_200_OK)
async def get_Receita(db: db_dependency):
    total = db.query(func.sum(models.Pedido.Preço)).filter(models.Pedido.Status == "Pagamento").scalar()
    return total

@router.get("/get/ativos")
async def get_Pedidos(db: db_dependency):
    total = db.query(models.Pedido).filter(models.Pedido.Status == "Pagamento").count()
    return total

@router.get("/get/pendentes")
async def get_Pendentes(db: db_dependency):
    total = db.query(models.Pedido).filter(or_(models.Pedido.Status == "Pendente", models.Pedido.Status == "Aprovado")).count()
    return total

@router.get("/get/thisMonth")
async def get_pedidos_mes_atual(db: db_dependency):
    current_year = datetime.now().year
    current_month = datetime.now().month

    total_pedidos = db.query(models.Pedido).filter(
        extract('year', models.Pedido.Data_Evento) == current_year,
        extract('month', models.Pedido.Data_Evento) == current_month
    ).count()

    return {total_pedidos}


@router.get("/get/eventosPorMes")
async def get_eventos_por_mes(db: db_dependency):
    hoje = datetime.now()
    data_limite = hoje - timedelta(days=365)

    resultados = db.query(
        extract('year', models.Pedido.Data_Compra).label('ano'),
        extract('month', models.Pedido.Data_Compra).label('mes'),
        func.count(models.Pedido.ID).label('total_eventos')
    ).filter(
        models.Pedido.Data_Compra >= data_limite,
        or_(
            models.Pedido.Status == "Pagamento",
            models.Pedido.Status == "Concluido"
        )
    ).group_by(
        extract('year', models.Pedido.Data_Compra),
        extract('month', models.Pedido.Data_Compra)
    ).order_by(
        extract('year', models.Pedido.Data_Compra),
        extract('month', models.Pedido.Data_Compra)
    ).all()

    resposta = []
    for ano, mes, total in resultados:
        resposta.append({
            "ano": int(ano),
            "mes": int(mes),
            "total_eventos": total
        })

    return resposta

from sqlalchemy import extract, func, or_, and_
from datetime import datetime, timedelta

@router.get("/get/completados_vs_pendentes")
async def get_completados_vs_pendentes(db: db_dependency):
    hoje = datetime.now()
    data_limite = hoje - timedelta(days=365)

    # Eventos Completados (Status == "Pagamento" ou "Concluido")
    completados = db.query(
        extract('year', models.Pedido.Data_Compra).label('ano'),
        extract('month', models.Pedido.Data_Compra).label('mes'),
        func.count(models.Pedido.ID).label('total_completados')
    ).filter(
        models.Pedido.Data_Compra >= data_limite,
        or_(
            models.Pedido.Status == "Aprovados",
            models.Pedido.Status == "Concluido"
        )
    ).group_by(
        extract('year', models.Pedido.Data_Compra),
        extract('month', models.Pedido.Data_Compra)
    ).order_by(
        extract('year', models.Pedido.Data_Compra),
        extract('month', models.Pedido.Data_Compra)
    ).all()

    # Eventos Pendentes ou Orcados
    pendentes = db.query(
        extract('year', models.Pedido.Data_Compra).label('ano'),
        extract('month', models.Pedido.Data_Compra).label('mes'),
        func.count(models.Pedido.ID).label('total_pendentes')
    ).filter(
        models.Pedido.Data_Compra >= data_limite,
        or_(
            models.Pedido.Status == "Pendente"
        )
    ).group_by(
        extract('year', models.Pedido.Data_Compra),
        extract('month', models.Pedido.Data_Compra)
    ).order_by(
        extract('year', models.Pedido.Data_Compra),
        extract('month', models.Pedido.Data_Compra)
    ).all()

    # Formatar resposta como dicionário de listas
    resposta = {
        "completados": [
            {"ano": int(ano), "mes": int(mes), "total": total} for ano, mes, total in completados
        ],
        "pendentes_ou_orcados": [
            {"ano": int(ano), "mes": int(mes), "total": total} for ano, mes, total in pendentes
        ]
    }

    return resposta
