#Importacao de bibliotecas

from flet import Page, TextField, ElevatedButton, DataTable, DataRow, DataColumn, DataCell, Text, icons, IconButton
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

#Configuracao do Banco de dados

Base = declarative_base()


class Produto(Base):
    __tablename__ = 'produtos'


    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(Integer, nullable=False)
    preco_entrada = Column(Float, nullable=False)
    preco_saida = Column(Float)
    taxa_aumento = Column(Float, nullable=False)
    quantidade = Column(Integer, nullable=False)

#Classe gerenciamento banco de dados

class ProdutoDB:
    #Metodo construtor
    def __init__(self):
        self.engine = create_engine('sqlite:///produto.db')
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
    
    #Metodo adicionar Protudos
    def adc(self, nome, preco_entrada, preco_saida, taxa_aumento, quantidade):
        session = self.Session()
        produto = Produto(nome = nome, preco_entrada = preco_entrada, preco_saida = preco_saida, taxa_aumento = taxa_aumento, quantidade =
                          quantidade)
        session.add(produto)
        session.commit()
        session.close()
    
    #Metodo Listar Produtos
    def lst(self):
        session = self.Session()
        produtos = session.query(Produto).all()
        session.close()
        return produtos
    
    #Metodo Deletar Produtos
    def dele(self, produto_id):
        session = self.Session()
        produto = session.query(Produto).get(produto_id)
        if produto:
            session.delete(produto)
            session.commit()
        session.close()

    