from re import A
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.utils import get_color_from_hex
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
from utils.connectionDatabase import ConnectionDatabase

# define um tamanho de tela padrao
Window.size = (400, 650)


# variaveis globais
CPF_FUNCIONARIO = ''
COD_ESTABELECIMENTO = ''
COD_BARRAS = ''
CNPJ_FORNECEDOR = ''
NOME_FORNECEDOR = ''

KV = '''
#:include FuncionarioScreen.kv
#:include HomeScreen.kv
#:include EstoqueScreen.kv
#:include FornecedoresScreen.kv
#:include EstabelecimentoScreen.kv
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:set toolbarColor get_color_from_hex("#DF6710")


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
    FornecedoresPage:
    CadastrarFornecedor:
    ConsultarFornecedor:
    TabelaBuscaFornecedor:
    RemoverFornecedor:
    AlterarFornecedor:
    AlterarFornecedor2: 
    EstabelecimentoPage:
    CadastrarEstabelecimento:
    AlterarEstabelecimento:   
    AlterarEstabelecimento2: 


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
                text: "Início"
                on_release:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "home"

            OneLineListItem:
                text: "Fornecedores"
                on_release:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "fornecedores"

            OneLineListItem:
                text: "Estabelecimentos"
                on_release:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "estabelecimento"

            OneLineListItem:
                text: "Historico"
                on_press:
                    root.nav_drawer.set_state("close")
                    root.screen_manager.current = "historico"

'''


class HomePage(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'
    
    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'


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
    
    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

class CadastrarFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchHome(self):
        self.parent.current = 'home'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

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

    def switchHome(self):
        self.parent.current = 'home'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

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

        sql_command = f"select * from funcionario WHERE cpf='{CPF_FUNCIONARIO}' and codigo_estabelecimento='{COD_ESTABELECIMENTO}';"

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

    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'


class RemoverFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchHome(self):
        self.parent.current = ''

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

    def remover(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        
        c = conn.cursor()

        sql_command = f"delete from funcionario WHERE cpf='{self.ids.cpf.text}' and codigo_estabelecimento='{self.ids.codigo_estabelecimento.text}';"

        c.execute(sql_command)	
        conn.commit()
        conn.close()


class AlterarFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchHome(self):
        self.parent.current = 'home'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

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

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'


class CadastrarProduto(Screen):
    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

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

    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

    def switchTabelaEstoque(self):
        self.parent.current = 'tabela_busca_estoque'

    def buscar(self):
        global COD_BARRAS
        COD_BARRAS = self.ids.cod_barras.text
    

class TabelaBuscaEstoque(Screen):

    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

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
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'
    

# botao do cadastro do funcionario
class ButtonFocus(MDRaisedButton, FocusBehavior):
    ...

class FornecedoresPage(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'
    
    def switchCadastrar(self):
        self.parent.current = 'cadastrar_fornecedor'

    def switchConsultar(self):
        self.parent.current = 'consultar_fornecedor'

    def switchAtualizar(self):
        self.parent.current = 'alterar_fornecedor'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchRemover(self):
        self.parent.current = 'remover_fornecedor'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

class CadastrarFornecedor(Screen):
    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

    def cadastrar(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        
        c = conn.cursor()

        # Add dados na tabela de fornecedor
        sql_command = "INSERT INTO fornecedor (CNPJ, NOME, RUA, ESTADO, CIDADE, CEP, NUMERO, BAIRRO) VALUES(%s, %s, %s, %s, %s,%s,%s,%s)"
        values = (self.ids.cnpj.text,
                  self.ids.nome.text,
                  self.ids.rua.text,
                  self.ids.estado.text,
                  self.ids.cidade.text,
                  self.ids.cep.text,
                  self.ids.numero.text,
                  self.ids.bairro.text)

        c.execute(sql_command, (values))	
        conn.commit()
        conn.close()

        self.ids.cnpj.text = ''
        self.ids.nome.text = ''
        self.ids.rua.text = ''
        self.ids.estado.text = ''
        self.ids.cidade.text = ''
        self.ids.cep.text = ''
        self.ids.numero.text = ''
        self.ids.bairro.text = ''        

        popup = Popup(title='CADASTRAR FORNECEDOR',
                      content=Label(text='Fornecedor cadastrado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'fornecedores'

class ConsultarFornecedor(Screen):
    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

    def switchTabela(self):
        self.parent.current = 'tabela_busca_fornecedor'

    def buscar(self):
        global CNPJ_FORNECEDOR
        CNPJ_FORNECEDOR = self.ids.cnpj.text
        global NOME_FORNECEDOR
        NOME_FORNECEDOR = self.ids.nome.text


class TabelaBuscaFornecedor(Screen):

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

    def tabela(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        c = conn.cursor()

        sql_command = f"select * from fornecedor WHERE cnpj='{CNPJ_FORNECEDOR}' or nome='{NOME_FORNECEDOR}';"

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
                ("CNPJ", dp(40)),
                ("NOME", dp(40)),
                ("RUA", dp(30)),
                ("ESTADO", dp(30)),
                ("CIDADE", dp(30)),
                ("CEP", dp(40)),
                ("NUMERO", dp(25)),
                ("BAIRRO", dp(40))
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


class RemoverFornecedor(Screen):
    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

    def remover(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        
        c = conn.cursor()

        sql_command = f"delete from fornecedor WHERE cnpj='{self.ids.cnpj.text}' and nome='{self.ids.nome.text}';"

        c.execute(sql_command)	
        conn.commit()
        conn.close()

class AlterarFornecedor(Screen):
    def recolherDados(self):    
        global CNPJ_FORNECEDOR
        CNPJ_FORNECEDOR = self.ids.cnpj.text
    
    def switchAtualiza(self):
        self.parent.current = 'alterar_fornecedor2'
    
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

class AlterarFornecedor2(Screen):

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

    def alterar(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        c = conn.cursor()

        sql_command = f"""update fornecedor
                            set cnpj=%s,
                                nome=%s,
                                rua=%s,
                                estado=%s,
                                cidade=%s,
                                cep=%s,
                                numero=%s,
                                bairro=%s
                            where cnpj=%s;"""

        values = (self.ids.cnpj.text,
                  self.ids.nome.text,
                  self.ids.rua.text,
                  self.ids.estado.text,
                  self.ids.cidade.text,
                  self.ids.cep.text,
                  self.ids.numero.text,
                  self.ids.bairro.text,
                  CNPJ_FORNECEDOR)

        c.execute(sql_command, values)
        conn.commit()
        conn.close()

        popup = Popup(title='ATUALIZAR DADOS DO FORNECEDOR',
                      content=Label(text='Fornecedor atualizado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'fornecedores'

class EstabelecimentoPage(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'
    
    def switchCadastrar(self):
        self.parent.current = 'cadastrar_estabelecimento'

    def switchInserir(self):
        self.parent.current = 'inserir_conta'

    def switchAlterar(self):
        self.parent.current = 'alterar_estabelecimento'

    def switchConsultar(self):
        self.parent.current = 'consultar_fornecedor'

    def switchModificar(self):
        self.parent.current = 'modificar_compra'

    def switchRemover(self):
        self.parent.current = 'remover_estabelecimento'

    def switchExcluir(self):
        self.parent.current = 'excluir_conta'

    def switchAtivas(self):
        self.parent.current = 'ver_ativa'

    def switchPassadas(self):
        self.parent.current = 'ver_passada'

class CadastrarEstabelecimento(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

    def cadastrar(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        
        c = conn.cursor()

        # Add dados na tabela de estabelecimento
        sql_command = "INSERT INTO estabelecimento (nome, bairro, rua, cep, cidade, numero) VALUES(%s, %s, %s, %s,%s,%s)"
        values = (self.ids.nome.text,
                  self.ids.bairro.text,
                  self.ids.rua.text,
                  self.ids.cep.text,
                  self.ids.cidade.text,
                  self.ids.numero.text)

        c.execute(sql_command, (values))    
        conn.commit()
        conn.close()

        self.ids.nome.text = ''
        self.ids.bairro.text = ''
        self.ids.rua.text = ''
        self.ids.cep.text = ''
        self.ids.cidade.text = ''
        self.ids.numero.text = ''      

        popup = Popup(title='CADASTRAR ESTABELECIMENTO',
                      content=Label(text='Estabelecimento cadastrado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'estabelecimento'


class AlterarEstabelecimento(Screen):
    def recolherDados(self):    
        global COD_ESTABELECIMENTO
        COD_ESTABELECIMENTO = self.ids.codigo.text
    
    def switchAtualiza(self):
        self.parent.current = 'alterar_estabelecimento2'
    
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

class AlterarEstabelecimento2(Screen):

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

    def alterar(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        c = conn.cursor()

        sql_command = f"""update estabelecimento
                            set nome=%s,
                                bairro=%s,
                                rua=%s,
                                cep=%s,
                                cidade=%s,
                                numero=%s
                            where codigo=%s;"""

        values = (self.ids.nome.text,
                  self.ids.bairro.text,
                  self.ids.rua.text,
                  self.ids.cep.text,
                  self.ids.cidade.text,
                  self.ids.numero.text,
                  COD_ESTABELECIMENTO)

        c.execute(sql_command, values)
        conn.commit()
        conn.close()

        popup = Popup(title='ATUALIZAR DADOS DO ESTABELECIMENTO',
                      content=Label(text='Estabelecimento atualizado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'estabelecimento'


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
sm.add_widget(TabelaBuscaEstoque(name='tabela_busca_estoque'))
sm.add_widget(FornecedoresPage(name='fornecedores'))
sm.add_widget(CadastrarFornecedor(name='cadastrar_fornecedor'))
sm.add_widget(ConsultarFornecedor(name='consultar_fornecedor'))
sm.add_widget(AlterarFornecedor(name='alterar_fornecedor'))
sm.add_widget(RemoverFornecedor(name='remover_fornecedor'))
sm.add_widget(EstabelecimentoPage(name='estabelecimento'))
sm.add_widget(CadastrarEstabelecimento(name='CadastrarEstabelecimento'))
sm.add_widget(AlterarEstabelecimento(name='alterar_estabelecimento'))
sm.add_widget(AlterarEstabelecimento2(name='alterar_estabelecimento2'))

class Main(MDApp):
    def build(self):

        self.theme_cls.primary_palette = "DeepOrange"
        conn = ConnectionDatabase.getConnection()
        # conn.executeSchema("01.01.sql") -> mudar depois quem eh qual
        # conn.executeQuery("01.01.sql")

        c = conn.cursor()
        conn.close()

        return Builder.load_string(KV)


Main().run()