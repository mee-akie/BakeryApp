from re import A
from kivy.lang import Builder
from kivy.properties import ObjectProperty
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


# define um tamanho de tela padrao
Window.size = (400, 650)


# variaveis globais
CPF_FUNCIONARIO = ''
COD_ESTABELECIMENTO = ''


KV = '''
#:include FuncionarioScreen.kv
#:include HomeScreen.kv
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:set toolbarColor get_color_from_hex("#854442")


ScreenManager:
    HomePage:
    FuncionarioPage:
    CadastrarFuncionario:
    BuscarFuncionario:
    TabelaBusca:
    RemoverFuncionario:
    AlterarFuncionario:


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


class FuncionarioPage(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchCadastro(self):
        self.parent.current = 'cadastrar_funcionario'

    def switchBuscar(self):
        self.parent.current = 'buscar_funcionario'

    def switchRemover(self):
        self.parent.current = 'remover_funcionario'

    def switchAlterar(self):
        self.parent.current = 'alterar_funcionario'

    def mensagemPopup(self):
         self.parent.current = 'mensagem'


class CadastrarFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

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

        popup = Popup(title='CADASTRAR FUNCIONÁRIO', content=Label(text='Funcionario cadastrado com sucesso'), size_hint=(None, None), size=(300, 150))
        popup.open()

        self.parent.current = 'funcionario'


class BuscarFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchTabela(self):
        self.parent.current = 'tabela_busca'

    def buscar(self):
        global CPF_FUNCIONARIO
        CPF_FUNCIONARIO = self.ids.cpf.text
        global COD_ESTABELECIMENTO
        COD_ESTABELECIMENTO = self.ids.codigo_estabelecimento.text


class TabelaBusca(Screen):
    def tabela(self):
        conn = psycopg2.connect(
            host = "ec2-44-198-211-34.compute-1.amazonaws.com",
            database = "ddj7ffdunshjqf", 
            user = "vuxxgxylynkvnk",
            password = "e7f1713e3c7c4907b83a8e412f5373c52e1bf5e7a741e6667957bb41bcbecd69",
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
sm.add_widget(TabelaBusca(name='tabela_busca'))
sm.add_widget(RemoverFuncionario(name='remover_funcionario'))
sm.add_widget(AlterarFuncionario(name='alterar_funcionario'))


class Main(MDApp):
    def build(self):

        self.theme_cls.primary_palette = "DeepOrange"

        conn = psycopg2.connect(
            host = "ec2-44-198-211-34.compute-1.amazonaws.com",
            database = "ddj7ffdunshjqf", 
            user = "vuxxgxylynkvnk",
            password = "e7f1713e3c7c4907b83a8e412f5373c52e1bf5e7a741e6667957bb41bcbecd69",
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
                        FOREIGN KEY (CPF  ) REFERENCES CLIENTE(CPF),
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