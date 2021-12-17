from re import A
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.checkbox import CheckBox
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDFloatingLabel, MDRaisedButton
from kivy.uix.label import Label
from kivymd.uix.behaviors import FocusBehavior
import psycopg2
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.uix.popup import Popup


# define um tamanho de tela padrao quando rodamos o main.py
Window.size = (400, 650)


# variaveis globais
CPF_FUNCIONARIO = ''
COD_ESTABELECIMENTO = ''
COD_BARRAS = ''

DADOS_PRODUTO = ()


KV = '''
#:include FuncionarioScreen.kv
#:include HomeScreen.kv
#:include EstoqueScreen.kv
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:set toolbarColor get_color_from_hex("#854442")


ScreenManager:
    HomePage:
    FuncionarioPage:
    CadastrarFuncionario:
    BuscarFuncionario:
    TabelaBuscaFuncionario:
    RemoverFuncionario:
    AlterarFuncionario:
    EstoquePage:
    CadastrarProduto:
    ConsultarEstoque:
    TabelaBuscaEstoque:
    AtualizarEstoque:
    AtualizarEstoque_2:


<NavigationDrawer>
    orientation: "vertical"
    padding: "8dp"
    spacing: "8dp"

    AnchorLayout:
        anchor_x: "left"
        size_hint_y: None
        height: avatar.height

        Image:
            id: avatar
            size_hint: None, None
            size: "56dp", "56dp"
            source: "user.png"

    MDLabel:
        text: "USERNAME"
        font_style: "Button"
        size_hint_y: None
        height: self.texture_size[1]

    MDLabel:
        text: "userEmail@gmail.com"
        font_style: "Caption"
        size_hint_y: None
        height: self.texture_size[1]


    ScrollView:
        MDList:
            OneLineListItem:
                text: "Pagina 1"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "item 1"

            OneLineListItem:
                text: "Pagina 2"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "item 2"

            OneLineListItem:
                text: "Pagina 3"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "item 3"

'''


class HomePage(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'


class FuncionarioPage(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchCadastro(self):
        self.parent.current = 'cadastrar_funcionario'

    def switchBuscar(self):
        self.parent.current = 'buscar_funcionario'

    def switchRemover(self):
        self.parent.current = 'remover_funcionario'

    def switchAlterar(self):
        self.parent.current = 'alterar_funcionario'



class CadastrarFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def cadastrar(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        
        c = conn.cursor()

        # Add dados na tabela de Funcionario
        sql_command = "INSERT INTO FUNCIONARIO (NOME, CPF, SALARIO, FERIAS, CODIGO_ESTABELECIMENTO) VALUES(%s, %s, %s, %s, %s)"
        values = (self.ids.nome.text,
                  self.ids.cpf.text,
                  self.ids.salario.text,
                  self.ids.ferias.text,
                  self.ids.codigo_estabelecimento.text)

        c.execute(sql_command, (values))	
        conn.commit()
        conn.close()

        self.ids.nome.text = ''
        self.ids.cpf.text = ''
        self.ids.salario.text = ''
        self.ids.ferias.text = ''
        self.ids.codigo_estabelecimento.text = ''

        popup = Popup(title='CADASTRAR FUNCIONÁRIO',
                      content=Label(text='Funcionario cadastrado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'funcionario'


class BuscarFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchTabela(self):
        self.parent.current = 'tabela_busca_funcionario'

    def buscar(self):
        global CPF_FUNCIONARIO
        CPF_FUNCIONARIO = self.ids.cpf.text
        global COD_ESTABELECIMENTO
        COD_ESTABELECIMENTO = self.ids.codigo_estabelecimento.text


class TabelaBuscaFuncionario(Screen):
    def tabela(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        c = conn.cursor()

        sql_command = f"select * from funcionario WHERE cpf='{CPF_FUNCIONARIO}' and codigo_estabelecimento={COD_ESTABELECIMENTO};"

        c.execute(sql_command)	
        output = c.fetchall()
        conn.close()

        screen = AnchorLayout()

        self.table = MDDataTable(
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(0.9, 0.6),
            column_data=[
                ("COD-FUNCIONARIO", dp(40)),
                ("NOME", dp(40)),
                ("CPF", dp(30)),
                ("SALÁRIO", dp(25)),
                ("FÉRIAS", dp(25)),
                ("COD-ESTABELECIMENTO", dp(40))
            ],
            sorted_on="NOME",
            sorted_order="ASC",
            elevation=2,
            row_data=output
        )

        self.add_widget(self.table)
        return screen

    def on_enter(self):
        self.tabela()


class RemoverFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def remover(self):
        conn = psycopg2.connect(
            host = "ec2-44-198-211-34.compute-1.amazonaws.com",
            database = "ddj7ffdunshjqf", 
            user = "vuxxgxylynkvnk",
            password = "e7f1713e3c7c4907b83a8e412f5373c52e1bf5e7a741e6667957bb41bcbecd69",
            port = "5432"
        )
        
        c = conn.cursor()

        sql_command = f"delete from funcionario WHERE cpf='{self.ids.cpf.text}' and codigo_estabelecimento={self.ids.codigo_estabelecimento.text};"

        c.execute(sql_command)	
        conn.commit()
        conn.close()


class AlterarFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def alterar(self):
        ...


class EstoquePage(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'
    
    def switchCadastrar(self):
        self.parent.current = 'cadastrar_produto'

    def switchConsultar(self):
        self.parent.current = 'consultar_estoque'

    def switchAtualizar(self):
        self.parent.current = 'atualizar_estoque'



class CadastrarProduto(Screen):
    def switchEstoque(self):
        self.parent.current = 'estoque'

    def cadastrar(self):
        conn = psycopg2.connect(
            host = "ec2-44-198-211-34.compute-1.amazonaws.com",
            database = "ddj7ffdunshjqf", 
            user = "vuxxgxylynkvnk",
            password = "e7f1713e3c7c4907b83a8e412f5373c52e1bf5e7a741e6667957bb41bcbecd69",
            port = "5432"
        )
        
        c = conn.cursor()

        # Add dados na tabela de Funcionario
        sql_command = "INSERT INTO PRODUTO (COD_BARRAS, NOME, NOME_FABRICANTE, PRECO, DATA_FABRICACAO, CATEGORIA, QTD_ESTOQUE, DATA_VENCIMENTO) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"
        values = (self.ids.cod_barras.text,
                  self.ids.nome.text,
                  self.ids.fabricante.text,
                  self.ids.preco.text,
                  self.ids.fabricacao.text,
                  self.ids.categoria.text,
                  self.ids.qtd_estoque.text,
                  self.ids.vencimento.text)

        c.execute(sql_command, (values))	
        conn.commit()
        conn.close()

        self.ids.cod_barras.text = ''
        self.ids.nome.text = ''
        self.ids.fabricante.text = ''
        self.ids.preco.text = ''
        self.ids.fabricacao.text = ''
        self.ids.categoria.text = ''
        self.ids.qtd_estoque.text = ''
        self.ids.vencimento.text = ''

        popup = Popup(title='CADASTRAR PRODUTO',
                      content=Label(text='Produto cadastrado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'estoque'


class ConsultarEstoque(Screen):
    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchTabelaEstoque(self):
        self.parent.current = 'tabela_busca_estoque'

    def buscar(self):
        global COD_BARRAS
        COD_BARRAS = self.ids.cod_barras.text
    

class TabelaBuscaEstoque(Screen):
    def tabela(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        c = conn.cursor()

        sql_command = f"select * from produto WHERE cod_barras='{COD_BARRAS}';"

        c.execute(sql_command)	
        output = c.fetchall()
        output.append(['', '', '', '', '', '' ,'', ''])
        print(output)
        conn.close()
        screen = AnchorLayout()

        self.table = MDDataTable(
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(0.9, 0.6),
            column_data=[
                ("COD-BARRAS", dp(40)),
                ("NOME", dp(40)),
                ("NOME FABRICANTE", dp(30)),
                ("PREÇO", dp(25)),
                ("DT FABRICAÇÃO", dp(40)),
                ("CATEGORIA", dp(35)),
                ("QTD ESTOQUE", dp(40)),
                ("DT VENCIMENTO", dp(40))
            ],
            row_data=output,
            sorted_on="NOME",
            sorted_order="ASC",
            elevation=2
        )

        self.add_widget(self.table)
        return screen

    def on_enter(self):
        self.tabela()



class AtualizarEstoque(Screen):
    def recolherDados(self):	
        global COD_BARRAS
        COD_BARRAS = self.ids.cod_barras.text
    
    def switchAtualiza(self):
        self.parent.current = 'atualizar_estoque_2'
    
    def switchEstoque(self):
        self.parent.current = 'estoque'


class AtualizarEstoque_2(Screen):

    def atualizar(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        c = conn.cursor()

        sql_command = f"""update produto

                            set cod_barras=%s,
                                nome=%s,
                                nome_fabricante=%s,
                                preco=%s,
                                data_fabricacao=%s,
                                categoria=%s,
                                qtd_estoque=%s,
                                data_vencimento=%s

                            where cod_barras=%s;"""

        values = (self.ids.cod_barras.text,
                  self.ids.nome.text,
                  self.ids.fabricante.text,
                  self.ids.preco.text,
                  self.ids.fabricacao.text,
                  self.ids.categoria.text,
                  self.ids.qtd_estoque.text,
                  self.ids.vencimento.text)

        c.execute(sql_command, values)
        conn.close()

        popup = Popup(title='ATUALIZAR DADOS DO PRODUTO',
                      content=Label(text='Produto atualizado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'estoque'



# botao do cadastro do funcionario
class ButtonFocus(MDRaisedButton, FocusBehavior):
    ...


# auxiliar para criar o "menu" do lado esquerdo da tela (botao superior esquerdo na Home)
class NavigationDrawer(MDBoxLayout):
    screen_manager = ObjectProperty()
    nav_drawer = ObjectProperty()


# Gerenciador de paginas
sm = ScreenManager()
sm.add_widget(HomePage(name='home'))
sm.add_widget(FuncionarioPage(name='funcionario'))
sm.add_widget(CadastrarFuncionario(name='cadastrar_funcionario'))
sm.add_widget(BuscarFuncionario(name='buscar_funcionario'))
sm.add_widget(TabelaBuscaFuncionario(name='tabela_busca_funcionario'))
sm.add_widget(RemoverFuncionario(name='remover_funcionario'))
sm.add_widget(AlterarFuncionario(name='alterar_funcionario'))
sm.add_widget(EstoquePage(name='estoque'))
sm.add_widget(CadastrarProduto(name='cadastrar_produto'))
sm.add_widget(ConsultarEstoque(name='consultar_estoque'))
sm.add_widget(AtualizarEstoque(name='atualizar_estoque'))
sm.add_widget(AtualizarEstoque_2(name='atualizar_estoque_2'))
sm.add_widget(TabelaBuscaEstoque(name='tabela_busca_estoque'))


class Main(MDApp):
    def build(self):

        self.theme_cls.primary_palette = "DeepOrange"

        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )

        c = conn.cursor()

        c.execute("""CREATE TABLE IF NOT EXISTS ESTABELECIMENTO (
                        CODIGO INT NOT NULL GENERATED ALWAYS AS IDENTITY,
                        NOME VARCHAR(70) NOT NULL,
                        BAIRRO VARCHAR(100),
                        RUA VARCHAR(100),
                        CEP CHAR(8),
                        CIDADE VARCHAR(100),
                        NUMERO VARCHAR(10),
                        PRIMARY KEY(CODIGO));
                """)

        c.execute("""CREATE TABLE IF NOT EXISTS FORNECEDOR (
                        CNPJ CHAR (14) NOT NULL,
                        NOME VARCHAR (70) NOT NULL,
                        RUA VARCHAR(100) NOT NULL,
                        ESTADO VARCHAR(30) NOT NULL,
                        CIDADE VARCHAR(100) NOT NULL,
                        CEP CHAR(8),
                        NUMERO VARCHAR(10),
                        BAIRRO VARCHAR(100),
                        PRIMARY KEY (CNPJ));
                """)

        c.execute("""CREATE TABLE IF NOT EXISTS CLIENTE (
                        NOME VARCHAR(70) NOT NULL,
                        CPF CHAR(11) NOT NULL,
                        DATANASC DATE,
                        PRIMARY KEY(CPF));
                """)

        c.execute("""CREATE TABLE IF NOT EXISTS PRODUTO (
                 	COD_BARRAS CHAR(15) NOT NULL,
                    NOME VARCHAR(50) NOT NULL,
                    NOME_FABRICANTE VARCHAR(100) NOT NULL,
                    PRECO DECIMAL(18,2) NOT NULL,
                    DATA_FABRICACAO DATE NOT NULL,
                    CATEGORIA VARCHAR(50) NOT NULL,
                    QTD_ESTOQUE INT NOT NULL,
                    DATA_VENCIMENTO DATE NOT NULL,
                    PRIMARY KEY (COD_BARRAS));
                """)

        c.execute("""CREATE TABLE IF NOT EXISTS CONTA (
                 		COD_BARRAS CHAR(48) NOT NULL,
                        TIPO CHAR(35) NOT NULL,
                        VALOR DECIMAL (10,2) NOT NULL,
                        DATA_VENCIMENTO DATE NOT NULL,
                        DATA_PAGAMENTO DATE NULL,
                        PAGO BOOLEAN,
                        CODIGO_ESTABELECIMENTO INT NOT NULL,
                        PRIMARY KEY(COD_BARRAS),
                        FOREIGN KEY(CODIGO_ESTABELECIMENTO) REFERENCES ESTABELECIMENTO(CODIGO));
                """)      

        c.execute("""CREATE TABLE IF NOT EXISTS FUNCIONARIO ( 
                        CODIGO_FUNC INT NOT NULL GENERATED ALWAYS AS IDENTITY,
                        NOME VARCHAR(70) NOT NULL,        	
                        CPF CHAR(11) NOT NULL,
                        SALARIO DECIMAL (10,2), 
                        FERIAS DATE,
                        CODIGO_ESTABELECIMENTO INT NOT NULL,
                        PRIMARY KEY(CODIGO_FUNC),
                        FOREIGN KEY (CODIGO_ESTABELECIMENTO) REFERENCES ESTABELECIMENTO(CODIGO));
                """)


        c.execute("""CREATE TABLE IF NOT EXISTS HISTORICO_TRABALHO (
                        DATA_REGISTRO  DATE NOT NULL,
                        HORA_ENTRADA_R TIME NOT NULL,
                        HORA_SAIDA_R TIME NOT NULL,
                        FCODIGO_FUNCIONARIO INT NOT NULL,
                        PRIMARY KEY(DATA_REGISTRO, HORA_ENTRADA_R, HORA_SAIDA_R, FCODIGO_FUNCIONARIO),
                        FOREIGN KEY(FCODIGO_FUNCIONARIO) REFERENCES FUNCIONARIO(CODIGO_FUNC));
                """)

        c.execute("""CREATE TABLE IF NOT EXISTS ADMINISTRADOR (
                        FCODIGO_FUNCIONARIO INT NOT NULL,
                        ESPECIALIDADE VARCHAR(30) NOT NULL,
                        PRIMARY KEY(FCODIGO_FUNCIONARIO),
                        FOREIGN KEY(FCODIGO_FUNCIONARIO) REFERENCES FUNCIONARIO(CODIGO_FUNC));
                """)

        c.execute("""CREATE TABLE IF NOT EXISTS ATENDENTE_CAIXA (
                        FCODIGO_FUNCIONARIO INT NOT NULL,
                        NIVEL_ESCOLARIDADE VARCHAR(30) NOT NULL,
                        PRIMARY KEY(FCODIGO_FUNCIONARIO),
                        FOREIGN KEY(FCODIGO_FUNCIONARIO) REFERENCES FUNCIONARIO(CODIGO_FUNC));
                """)

        c.execute("""CREATE TABLE IF NOT EXISTS TELEFONE_CONTATO (
                        TELEFONE VARCHAR (14) NOT NULL,
                        TCODIGO CHAR(14) NOT NULL,
                        PRIMARY KEY (TELEFONE),
                        FOREIGN KEY(TCODIGO) REFERENCES FORNECEDOR(CNPJ));
                """)

        c.execute("""CREATE TABLE IF NOT EXISTS VENDE (
                    	COD_VENDA INT NOT NULL GENERATED ALWAYS AS IDENTITY,
                        DT_VENDA TIMESTAMP NOT NULL,
                        VALOR_TOTAL DECIMAL(18,2) NOT NULL,
                        FCODIGO_FUNCIONARIO INT NOT NULL,
                        CPF CHAR(11) NOT NULL,
                        PRIMARY KEY (COD_VENDA),
                        FOREIGN KEY (CPF) REFERENCES CLIENTE(CPF),
                        FOREIGN KEY (FCODIGO_FUNCIONARIO) REFERENCES ATENDENTE_CAIXA(FCODIGO_FUNCIONARIO));
                """)
                
        c.execute("""CREATE TABLE IF NOT EXISTS VENDIDO (
                        COD_PRODUTO_VENDIDO INT NOT NULL GENERATED ALWAYS AS IDENTITY,
                        QUANTIDADE INT NOT NULL,
                        COD_VENDA INT NOT NULL,
                        COD_BARRAS CHAR(15) NOT NULL,
                        PRIMARY KEY (COD_PRODUTO_VENDIDO),
                        FOREIGN KEY (COD_VENDA ) REFERENCES VENDE(COD_VENDA),
                        FOREIGN KEY (COD_BARRAS) REFERENCES PRODUTO(COD_BARRAS));
                """)

        c.execute("""CREATE TABLE IF NOT EXISTS COMPRA (
                        COD_COMPRA INT NOT NULL GENERATED ALWAYS AS IDENTITY,
                        DT_SOLICITACAO TIMESTAMP NOT NULL,
                        DT_ENTREGA TIMESTAMP NOT NULL,
                        VALOR_TOTAL DECIMAL(18,2) NOT NULL,
                        FCODIGO_FUNCIONARIO INT NOT NULL,
                        CNPJ CHAR (14) NOT NULL,
                        PRIMARY KEY (COD_COMPRA),
                        FOREIGN KEY (FCODIGO_FUNCIONARIO ) REFERENCES ADMINISTRADOR(FCODIGO_FUNCIONARIO),
                        FOREIGN KEY (CNPJ) REFERENCES FORNECEDOR(CNPJ));
                """)

        c.execute("""CREATE TABLE IF NOT EXISTS PRODUTO_COMPRADO (
                        COD_PRODUTO_COMPRADO INT NOT NULL GENERATED ALWAYS AS IDENTITY,
                        QUANTIDADE INT NOT NULL,
                        COD_COMPRA INT NOT NULL,
                        COD_BARRAS CHAR(15) NOT NULL,
                        PRIMARY KEY (COD_PRODUTO_COMPRADO ),
                        FOREIGN KEY (COD_COMPRA  ) REFERENCES COMPRA(COD_COMPRA ),
                        FOREIGN KEY (COD_BARRAS) REFERENCES PRODUTO(COD_BARRAS));
                """)
	
        conn.commit()
        conn.close()

        return Builder.load_string(KV)


Main().run()