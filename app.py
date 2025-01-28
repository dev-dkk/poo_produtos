#Importacao de bibliotecas

from flet import Page, ProgressBar,TextField,Container, Row, ElevatedButton, DataTable, DataRow, DataColumn, DataCell, Text, icons, IconButton, Column as Diabo,alignment
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base
import time

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
        self.nome_ipt = TextField(label='Nome do Produto', width=800)
        self.preco_entrada_ipt = TextField(label='Preço de Entrada do Produto', keyboard_type='number', width=800)
        self.taxa_aumento_ipt = TextField(label='Taxa para Preço Saída(%)', keyboard_type='number', width=800)
        self.quantidade_ipt = TextField(label='Quantidade', keyboard_type='number', width=800)
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
            ],
            
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

    #Titulo da janela
    page.title = "DK - Gerenciamento Produtos"

    #Para impedir que alterem o tamanho da janela e definir tamamnho da janela
    page.window.resizable = False
    page.window.width = 800
    
    #Variaveis de iniciação para adicionar uma barra de progresso enquanto a janela carrega
    barra = ProgressBar(width = 200)
    texto = Text("Carregando ...")
    gambiarra1 = Diabo([barra, texto], alignment="center", horizontal_alignment="center") #Cria uma coluna com a barra e o texto
    gambiarra2 = Container(content=gambiarra1, alignment=alignment.center, expand=True)#Encapsula em um container que alinha ao centro
    page.add(gambiarra2)

    #Fazer com que a barra de progresso avance de acordo com o tempo de carregamento definido
    for i in range(10):
        barra.value = (i+1)*10
        page.update()
        time.sleep(0.3)

    #Deixa a janela visivel apos acabar o tempo
    page.window.visible = True

    #Adciona um icone a janela  ///////SÓ FUNCIONA NO WINDOWS
    page.window.icon = "img/logo.ico"

    #Limpa a barra de progresso apos o carregamento
    page.clean()

    App(page)

if __name__ == "__main__":
    import flet as funciona
    funciona.app(target=main, view=funciona.AppView.FLET_APP_HIDDEN)