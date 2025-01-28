from flet import Page, TextField, ElevatedButton, DataTable, DataRow, DataColumn, DataCell, Text, icons, IconButton
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

Base = declarative_base()


class Produto(Base):
    __tablename__ = 'produtos'


    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(Integer, nullable=False)
    preco_entrada = Column(Float, nullable=False)
    preco_saida = Column(Float)
    quantidade = Column(Integer, nullable=False)