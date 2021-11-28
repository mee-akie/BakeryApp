from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.behaviors import FocusBehavior
import psycopg2
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp


KV = '''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:set toolbarColor get_color_from_hex("#854442")


ScreenManager:
    HomePage:
    FuncionarioPage:
    CadastrarFuncionario:
    BuscarFuncionario:


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


<HomePage>:
    name: 'home'
    MDScreen:
        MDToolbar:
            id: toolbar
            pos_hint: {"top": 1}
            elevation: 10
            title: "Bakery ABC"
            left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]
            md_bg_color: toolbarColor

        MDNavigationLayout:
            x: toolbar.height
            ScreenManager:
                id: screen_manager
                MDScreen:
                    name: "item 1"
                    MDLabel:
                        text: "Screen 1"
                        halign: "center"
                MDScreen:
                    name: "item 2"
                    MDLabel:
                        text: "Screen 2"
                        halign: "center"
                MDScreen:
                    name: "item 3"
                    MDLabel:
                        text: "Screen 3"
                        halign: "center"
            MDNavigationDrawer:
                id: nav_drawer
                NavigationDrawer:
                    screen_manager: screen_manager
                    nav_drawer: nav_drawer

        MDBottomNavigation:
            size_hint_y: .09
            panel_color: get_color_from_hex("#854442")
            text_color_active: get_color_from_hex("#fff4e6")
            
            MDBottomNavigationItem:
                name: 'screen 1'
                text: 'home'
                icon: 'home-circle'
                on_enter: root.switchHome()

            MDBottomNavigationItem:
                name: 'screen 2'
                text: 'botao 2'
                icon: 'barcode'

            MDBottomNavigationItem:
                name: 'screen 3'
                text: 'Funcionarios'
                icon: 'account-group'
                on_enter: root.switchFuncionario()
                
 
<FuncionarioPage>:
    name: 'funcionario'

    MDScreen:
        MDToolbar:
            id: toolbar
            pos_hint: {"top": 1}
            elevation: 10
            title: "Bakery ABC"
            md_bg_color: toolbarColor

        MDBottomNavigation:
            size_hint_y: .09
            panel_color: get_color_from_hex("#854442")
            text_color_active: get_color_from_hex("#fff4e6")
            
            MDBottomNavigationItem:
                name: 'screen 1'
                text: 'home'
                icon: 'home-circle'
                on_enter: root.switchHome()

            MDBottomNavigationItem:
                name: 'screen 2'
                text: 'botao 2'
                icon: 'barcode'

            MDBottomNavigationItem:
                name: 'screen 3'
                text: 'Funcionarios'
                icon: 'account-group'
                on_enter: root.switchFuncionario()

        MDFillRoundFlatIconButton:
            text : 'Buscar um funcionario'
            icon : "account-search"
            pos_hint : {"center_x":.5,"center_y":.65}
            text_color : get_color_from_hex("#7E6B73")
            md_bg_color : get_color_from_hex("#FCE18E")
            font_size : 20
            user_font_size: "64sp"
            on_press: root.switchBuscar()

        MDFillRoundFlatIconButton :
            text : 'Cadastrar um novo funcionario'
            icon : "account-plus"
            pos_hint : {"center_x":.5,"center_y":.55}
            text_color : get_color_from_hex("#7E6B73")
            md_bg_color : get_color_from_hex("#FCE18E")
            font_size : 20
            user_font_size: "64sp"
            on_press: root.switchCadastro()

        MDFillRoundFlatIconButton :
            text : 'Remover um funcionario'
            icon : "account-minus"
            pos_hint : {"center_x":.5,"center_y":.45}
            text_color : get_color_from_hex("#7E6B73")
            md_bg_color : get_color_from_hex("#FCE18E")
            font_size : 20
            on_press : app.callback()

        MDFillRoundFlatIconButton :
            text : 'Alterar dados de um funcionario'
            icon : "account-edit"
            pos_hint : {"center_x":.5,"center_y":.35}
            text_color : get_color_from_hex("#7E6B73")
            md_bg_color : get_color_from_hex("#FCE18E")
            font_size : 20
            on_press : root.s


<CadastrarFuncionario>:
    name: 'cadastrar_funcionario'

    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "NOVO FUNCIONARIO"
        md_bg_color: get_color_from_hex("#854442")


    MDFloatLayout:
        BoxLayout:
            orientation: "vertical"
            size_hint_x: .9
            size_hint_y: .8
            pos_hint: {'center_x': .5, 'center_y': .75}

            MDTextField:
                id: nome
                multiline: False
                size_hint_x: .8
                hint_text: 'Nome:'
                pos_hint: {'center_x': .5, 'center_y': .7}
                text_color: get_color_from_hex("#000000")

            MDTextField:
                id: cpf
                multiline: False
                size_hint_x: .8
                hint_text: 'CPF:'
                pos_hint: {'center_x': .5, 'center_y': .7}
                text_color: get_color_from_hex("#000000")
            
            MDTextField:
                id: salario
                multiline: False
                size_hint_x: .8
                hint_text: 'Salario:'
                pos_hint: {'center_x': .5, 'center_y': .8}
                text_color: get_color_from_hex("#000000")

            MDTextField:
                id: ferias
                multiline: False
                size_hint_x: .8
                hint_text: 'Ferias:'
                pos_hint: {'center_x': .5, 'center_y': .6}
                text_color: get_color_from_hex("#000000")
    
            MDTextField:
                id: codigo_estabelecimento
                multiline: False
                size_hint_x: .8
                hint_text: 'Codigo do estabelecimento:'
                pos_hint: {'center_x': .5, 'center_y': .4}
                text_color: get_color_from_hex("#000000")
                    
        ButtonFocus:
            size_hint_x: .35
            pos_hint: {'center_x': .3, 'center_y': .15}
            focus_color: get_color_from_hex("#e54c37")
            unfocus_color: get_color_from_hex("#854442")
            text: 'CADASTRAR'
            on_press: root.cadastrar()

        ButtonFocus:
            size_hint_x: .35
            pos_hint: {'center_x': .7, 'center_y': .15}
            focus_color: get_color_from_hex("#e54c37")
            unfocus_color: get_color_from_hex("#854442")
            text: 'CANCELAR'
            on_press: root.switchFuncionario()


<BuscarFuncionario>:
    name: 'buscar_funcionario'

    MDToolbar:
        id: toolbar
        pos_hint: {"top": 1}
        elevation: 10
        title: "DADOS DE FUNCIONARIO"
        md_bg_color: get_color_from_hex("#854442")
        
    MDFloatLayout:
        BoxLayout:
            orientation: "vertical"
            size_hint_x: .9
            size_hint_y: .8
            pos_hint: {'center_x': .5, 'center_y': .9}

            MDTextField:
                id: codigo_estabelecimento
                multiline: False
                size_hint_x: .8
                hint_text: 'Número do estabelecimento: '
                pos_hint: {'center_x': .5, 'center_y': .8}
                text_color: get_color_from_hex("#000000")

            MDTextField:
                id: cpf
                multiline: False
                size_hint_x: .8
                hint_text: 'CPF do funcionário: '
                pos_hint: {'center_x': .5, 'center_y': .7}
                text_color: get_color_from_hex("#000000")

        ButtonFocus:
            size_hint_x: .35
            pos_hint: {'center_x': .3, 'center_y': .45}
            focus_color: get_color_from_hex("#e54c37")
            unfocus_color: get_color_from_hex("#854442")
            text: 'BUSCAR'
            on_press:
                root.buscar()


        ButtonFocus:
            size_hint_x: .35
            pos_hint: {'center_x': .7, 'center_y': .45}
            focus_color: get_color_from_hex("#e54c37")
            unfocus_color: get_color_from_hex("#854442")
            text: 'CANCELAR'
            on_press: root.switchFuncionario()


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
        # Create A Cursor
        c = conn.cursor()

        # Add dados na tabela de Funcionario
        sql_command = "INSERT INTO FUNCIONARIO (NOME, CPF, SALARIO, FERIAS, CODIGO_ESTABELECIMENTO) VALUES(%s, %s, %s, %s, %s)"
        values = (self.ids.nome.text,
                  self.ids.cpf.text,
                  self.ids.salario.text,
                  self.ids.ferias.text,
                  self.ids.codigo_estabelecimento.text)

        # Execute SQL Command
        c.execute(sql_command, (values))	

        # Commit our changes in Heroku
        conn.commit()

        # Close our connection
        conn.close()

        self.ids.nome.text = ''
        self.ids.cpf.text = ''
        self.ids.salario.text = ''
        self.ids.ferias.text = ''
        self.ids.codigo_estabelecimento.text = ''

        self.parent.current = 'funcionario'


class BuscarFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def buscar(self):

        conn = psycopg2.connect(
            host = "ec2-44-198-211-34.compute-1.amazonaws.com",
            database = "ddj7ffdunshjqf", 
            user = "vuxxgxylynkvnk",
            password = "e7f1713e3c7c4907b83a8e412f5373c52e1bf5e7a741e6667957bb41bcbecd69",
            port = "5432"
        )
        c = conn.cursor()

        # Add dados na tabela de Funcionario
        sql_command = f"select * from funcionario WHERE cpf='{self.ids.cpf.text}' and codigo_estabelecimento={self.ids.codigo_estabelecimento.text};"

        # Execute SQL Command
        c.execute(sql_command)	

        output = c.fetchall()

        self.ids.cpf.text = ''
        self.ids.codigo_estabelecimento.text = ''
        conn.close()

        screen = Screen()

        table = MDDataTable(
            size_hint=(0.7, 0.6),
            use_pagination=True,
            column_data=[
                ("cod_func", dp(30)),
                ("Name", dp(30)),
                ("cpf", dp(30)),
                ("salario", dp(30)),
                ("ferias", dp(30)),
                ("departa", dp(30))
            ],
            row_data=output
        )

        screen.add_widget(table)

        return screen

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



class Main(MDApp):
    def build(self):
        conn = psycopg2.connect(
            host = "ec2-44-198-211-34.compute-1.amazonaws.com",
            database = "ddj7ffdunshjqf", 
            user = "vuxxgxylynkvnk",
            password = "e7f1713e3c7c4907b83a8e412f5373c52e1bf5e7a741e6667957bb41bcbecd69",
            port = "5432"
        )
        # Create A Cursor
        c = conn.cursor()

        # Create the tables

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
    
        sql_command = "INSERT INTO ESTABELECIMENTO(nome, rua, numero, bairro, cep, cidade) VALUES(%s, %s, %s, %s, %s, %s)"
        values = ('Panificadora Alfa','Rua Projetada', '1', 'Ouro Verde','78135616','Várzea Grande')
        sql_command2 = "INSERT INTO FUNCIONARIO (NOME, CPF, SALARIO, FERIAS, CODIGO_ESTABELECIMENTO) VALUES(%s, %s, %s, NULL, %s)"
        values2 = ('MARIA AAAAAA', '23472712356', "3000", "1")

        # Execute SQL Command

        c.execute(sql_command, (values))
        c.execute(sql_command2, (values2))	
	


        # Commit our changes in Heroku
        conn.commit()

        # Close our connection
        conn.close()

        return Builder.load_string(KV)


Main().run()