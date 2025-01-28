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

#Classe Principal da Interface e Logica do App
class App(ProdutoDB):
    #Metodo Construtor da classe principal
    def __init__(self, page:Page):
        self.page = page
        self.db = ProdutoDB()
        
        #Organizacao das entradas e dados dentro do app(os inputs)
        self.nome_ipt = TextField(label='Nome do Produto')
        self.preco_entrada_ipt = TextField(label='Preço de Entrada do Produto', keyboard_type='number')
        self.taxa_aumento_ipt = TextField(label='Taxa para Preço Saída(%)', keyboard_type='number')
        self.quantidade_ipt = TextField(label='Quantidade', keyboard_type='number')
        #Organizazcao as informacoes dentro do app
        self.table = DataTable(
            columns=[
                DataColumn(Text("ID")),
                DataColumn(Text("NOME")),
                DataColumn(Text("PREÇO ENTRADA")),
                DataColumn(Text("PREÇO SAÍDA")),
                DataColumn(Text("TAXA")),
                DataColumn(Text("QUANTIDADE")),
                DataColumn(Text("AÇÕES"))
            ]
        )
        self.page.add(
            self.nome_ipt,
            self.preco_entrada_ipt,
            self.taxa_aumento_ipt,
            self.quantidade_ipt,
            ElevatedButton("+", on_click=self.adc_produto),
            self.table
        )
        self.atualizar_tabela()

    #Chama metodo adicionar produto do banco e dados 
    def adc_produto(self, e):
        nome = self.nome_ipt.value
        preco_entrada = float(self.preco_entrada_ipt.value)  
        taxa_aumento = float(self.taxa_aumento_ipt.value)    
        preco_saida = preco_entrada * (taxa_aumento / 100) + preco_entrada
        quantidade = int(self.quantidade_ipt.value)          
        self.db.adc(nome, preco_entrada, preco_saida, taxa_aumento, quantidade)
        self.atualizar_tabela()

    #Metodo para atualizazr a tabela
    def atualizar_tabela(self):
        self.table.rows.clear()
        produtos = self.db.lst()
        for produto in produtos:
            self.table.rows.append(
                DataRow(
                    cells=[
                        DataCell(Text(str(produto.id))),
                        DataCell(Text(produto.nome)),
                        DataCell(Text(f"R${produto.preco_entrada:.2f}")),
                        DataCell(Text(f"R${produto.preco_saida:.2f}")),
                        DataCell(Text(f"{produto.taxa_aumento}%")),
                        DataCell(Text(str(produto.quantidade))),
                        DataCell(
                            IconButton(
                                icon=icons.DELETE,
                                on_click=lambda e, id = produto.id: self.deletar(id)
                            )
                        )
                    ]
                )
            )
        self.page.update()
    
    #Metodo para chamar o metodo eletar do banco de dados quando clicar o botao excluir
    def deletar(self, produto_id):
        self.db.dele(produto_id)
        self.atualizar_tabela()

#Execucao do app
def main(page:Page):
    page.title = "DK - Gerenciamento Produtos"
    page.window.width = 800
    App(page)

if __name__ == "__main__":
    import flet as funciona
    funciona.app(target=main)