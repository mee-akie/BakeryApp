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
from kivymd.uix.label import MDLabel
from kivy.uix.popup import Popup
from utils.connectionDatabase import ConnectionDatabase


# define um tamanho de tela padrao quando rodamos o main.py
Window.size = (400, 650)


# variaveis globais
CPF_FUNCIONARIO = ''
NOME_FUNC = ''
COD_ESTABELECIMENTO = ''
COD_BARRAS = ''
NOME_PROD = ''
CATEGORIA_PROD = ''
NOME_FABRIC = ''
CNPJ_FORNECEDOR = ''
NOME_FORNECEDOR = '' 
NOME_ESTABELECIMENTO = ''


KV = '''
#:include FuncionarioScreen.kv
#:include HomeScreen.kv
#:include EstoqueScreen.kv
#:include Login.kv
#:include FornecedoresScreen.kv
#:include EstabelecimentoScreen.kv

#:import get_color_from_hex kivy.utils.get_color_from_hex
#:set toolbarColor get_color_from_hex("#DF6710")


ScreenManager:
    LoginPage:
    HomePage:
    FuncionarioPage:
    CadastrarFuncionario:
    BuscarFuncionario:
    TabelaBuscaFuncionario:
    RemoverFuncionario:
    AlterarFuncionario:
    AlterarFuncionario2:
    EstoquePage:
    CadastrarProduto:
    RemoverProduto:
    ConsultarEstoque:
    TabelaBuscaEstoque:
    AtualizarEstoque:
    AtualizarEstoque_2:
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
    ConsultarEstabelecimento:
    TabelaBuscaEStabelecimento:
    RemoverEstabelecimento:
    ConsultaContasAtivas:
    ConsultarContasPassadas:
    RemoverConta:
    CadastrarConta:
    AlterarConta:
    AlterarConta2:

'''

class LoginPage(Screen):
    
    def validaLogin(self, *args):

        ##recebendo o cpf e a senha do usuario
        cpfUsuario = self.ids.cpf.text.replace('.','').replace('-','')
        senhaUsuario = self.ids.senha.text
        
        #iniciando conexao, criando o cursor
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()
        
        #executando o select que verifica se o login esta correto ou nao
        c.execute("SET search_path TO PADARIA;")
        c.execute(f"SELECT COUNT(1) AS LOGIN FROM FUNCIONARIO WHERE CPF = '{cpfUsuario}' AND SENHA = '{senhaUsuario}';")
        output = c.fetchall()
        c.close()
        
        #recebendo o resultado do select
        for row in output:
            result = row[0]
        
        if result == 1:
            self.parent.current = 'home'
        else:
            self.add_widget(
                MDLabel(
                    text="CPF ou Senha incorretos",
                    halign="center",
                    pos_hint= { "y": -0.35},
                    theme_text_color="Error",
                )
            )

#thata
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



class CadastrarFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def cadastrar(self):
        conn = ConnectionDatabase.getConnection()
        
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
        global NOME_FUNC
        NOME_FUNC = self.ids.nome.text
        print(CPF_FUNCIONARIO)
        print(COD_ESTABELECIMENTO)


class TabelaBuscaFuncionario(Screen):
    def tabela(self):
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        sql_command = ''
        
        if CPF_FUNCIONARIO != '' and COD_ESTABELECIMENTO != '' and NOME_FUNC != '':
            sql_command = f"select * from funcionario WHERE cpf='{CPF_FUNCIONARIO}' and codigo_estabelecimento={COD_ESTABELECIMENTO} and nome={NOME_FUNC};"

        elif CPF_FUNCIONARIO != '' and COD_ESTABELECIMENTO != '' and NOME_FUNC == '':
            sql_command = f"select * from funcionario WHERE cpf='{CPF_FUNCIONARIO}' and codigo_estabelecimento={COD_ESTABELECIMENTO};"
        
        elif CPF_FUNCIONARIO != '' and COD_ESTABELECIMENTO == '' and NOME_FUNC == '':
            sql_command = f"select * from funcionario WHERE cpf='{CPF_FUNCIONARIO}';"

        elif CPF_FUNCIONARIO == '' and COD_ESTABELECIMENTO != '' and NOME_FUNC == '':
            sql_command = f"select * from funcionario WHERE codigo_estabelecimento='{COD_ESTABELECIMENTO}';"

        elif CPF_FUNCIONARIO == '' and COD_ESTABELECIMENTO == '' and NOME_FUNC != '':
            sql_command = f"select * from funcionario WHERE nome='{NOME_FUNC}';"
        
        else:
            popup = Popup(title='ERRO - BUSCA DE FUNCIONARIO',
                    content=Label(text='Não foi informado nenhum dado\npara realizar a busca'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return

        c.execute(sql_command)	
        output = c.fetchall()
        output.append(['', '', '', '', '', '' ,'', ''])

        conn.close()

        screen = AnchorLayout()

        self.table = MDDataTable(
            pos_hint={'center_x': .5, 'center_y': .5},
            use_pagination=True,
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
        conn = ConnectionDatabase.getConnection()
        
        c = conn.cursor()

        sql_command = f"delete from funcionario WHERE cpf='{self.ids.cpf.text}' and codigo_estabelecimento={self.ids.codigo_estabelecimento.text};"

        c.execute(sql_command)	
        conn.commit()
        conn.close()


class AlterarFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def recolherDados(self):	
        global CPF_FUNCIONARIO
        CPF_FUNCIONARIO = self.ids.cpf.text
        self.parent.current = 'alterar_funcionario_2'


class AlterarFuncionario2(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def alterar(self):
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        sql_command = f"""update funcionario
                            set nome=%s,
                                cpf=%s,
                                salario=%s,
                                ferias=%s,
                                codigo_estabelecimento=%s
                            where cpf=%s;"""

        values = (self.ids.nome.text,
                  self.ids.cpf.text,
                  self.ids.salario.text,
                  self.ids.ferias.text,
                  self.ids.codigo_estabelecimento.text,
                  CPF_FUNCIONARIO)

        c.execute(sql_command, values)
        conn.commit()
        conn.close()

        popup = Popup(title='ATUALIZAR DADOS DE FUNCIONARIO',
                      content=Label(text='Funcionario atualizado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'funcionario'


class EstoquePage(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'
    
    def switchCadastrar(self):
        self.parent.current = 'cadastrar_produto'

    def switchRemover(self):
        self.parent.current = 'remover_produto'

    def switchConsultar(self):
        self.parent.current = 'consultar_estoque'

    def switchAtualizar(self):
        self.parent.current = 'atualizar_estoque'


class CadastrarProduto(Screen):
    def switchEstoque(self):
        self.parent.current = 'estoque'

    def cadastrar(self):
        conn = ConnectionDatabase.getConnection()
        
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

        
class RemoverProduto(Screen):
    def remover(self):
        conn = ConnectionDatabase.getConnection()
        
        c = conn.cursor()

        sql_command = f"delete from produto WHERE cod_barras='{self.ids.cod_barras.text}';"

        c.execute(sql_command)	
        conn.commit()
        conn.close()

        popup = Popup(title='REMOVER PRODUTO',
                      content=Label(text='Produto removido com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()
        
        self.parent.current = 'estoque'

    
    def switchEstoque(self):
        self.parent.current = 'estoque'


class ConsultarEstoque(Screen):
    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchTabelaEstoque(self):
        self.parent.current = 'tabela_busca_estoque'

    def buscar(self):
        global COD_BARRAS
        COD_BARRAS = self.ids.cod_barras.text
        global NOME_PROD
        NOME_PROD = self.ids.nome.text
        global CATEGORIA_PROD
        CATEGORIA_PROD = self.ids.categoria.text
        global NOME_FABRIC
        NOME_FABRIC = self.ids.nome_fabricante.text
    

class TabelaBuscaEstoque(Screen):
    def tabela(self):
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        sql_command = ''
        
        if COD_BARRAS != '' and NOME_PROD != '' and CATEGORIA_PROD != '' and NOME_FABRIC != '':
            sql_command = f"select * from produto WHERE cod_barras='{COD_BARRAS}' and nome='{NOME_PROD}' and categoria='{CATEGORIA_PROD}' and nome_fabricante='{NOME_FABRIC}';"

        elif COD_BARRAS != '' and NOME_PROD != '' and CATEGORIA_PROD != '' and NOME_FABRIC == '':
            sql_command = f"select * from produto WHERE cod_barras='{COD_BARRAS}' and nome='{NOME_PROD}' and categoria='{CATEGORIA_PROD}';"
        
        elif COD_BARRAS != '' and NOME_PROD != '' and CATEGORIA_PROD == '' and NOME_FABRIC != '':
            sql_command = f"select * from produto WHERE cod_barras='{COD_BARRAS}' and nome='{NOME_PROD}' and nome_fabricante='{NOME_FABRIC}';"

        elif COD_BARRAS == '' and NOME_PROD == '' and CATEGORIA_PROD != '' and NOME_FABRIC != '':
            sql_command = f"select * from produto WHERE cod_barras='{COD_BARRAS}' and categoria='{CATEGORIA_PROD}' and nome_fabricante='{NOME_FABRIC}';"

        elif COD_BARRAS == '' and NOME_PROD != '' and CATEGORIA_PROD != '' and NOME_FABRIC != '':
            sql_command = f"select * from produto WHERE nome='{NOME_PROD}' and categoria='{CATEGORIA_PROD}' and nome_fabricante='{NOME_FABRIC}';"

        elif COD_BARRAS != '' and NOME_PROD != '' and CATEGORIA_PROD == '' and NOME_FABRIC == '':
            sql_command = f"select * from produto WHERE cod_barras='{COD_BARRAS}' and nome='{NOME_PROD}';"

        elif COD_BARRAS == '' and NOME_PROD == '' and CATEGORIA_PROD != '' and NOME_FABRIC != '':
            sql_command = f"select * from produto WHERE categoria='{CATEGORIA_PROD}' and nome_fabricante='{NOME_FABRIC}';"

        elif COD_BARRAS != '' and NOME_PROD == '' and CATEGORIA_PROD == '' and NOME_FABRIC != '':
            sql_command = f"select * from produto WHERE cod_barras='{COD_BARRAS}' and nome_fabricante='{NOME_FABRIC}';"

        elif COD_BARRAS == '' and NOME_PROD != '' and CATEGORIA_PROD != '' and NOME_FABRIC == '':
            sql_command = f"select * from produto WHERE nome='{NOME_PROD}' and categoria='{CATEGORIA_PROD}';"

        elif COD_BARRAS != '' and NOME_PROD == '' and CATEGORIA_PROD == '' and NOME_FABRIC == '':
            sql_command = f"select * from produto WHERE cod_barras='{COD_BARRAS}';"

        elif COD_BARRAS == '' and NOME_PROD != '' and CATEGORIA_PROD == '' and NOME_FABRIC == '':
            sql_command = f"select * from produto WHERE nome='{NOME_PROD}';"

        elif COD_BARRAS == '' and NOME_PROD == '' and CATEGORIA_PROD != '' and NOME_FABRIC == '':
            sql_command = f"select * from produto WHERE categoria='{CATEGORIA_PROD}';"

        elif COD_BARRAS == '' and NOME_PROD == '' and CATEGORIA_PROD == '' and NOME_FABRIC != '':
            sql_command = f"select * from produto WHERE nome_fabricante='{NOME_FABRIC}';"

        else:
            popup = Popup(title='ERRO - CONSULTAR ESTOQUE',
                    content=Label(text='Não foi informado nenhum dado\npara realizar a busca'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return

        c.execute(sql_command)	
        output = c.fetchall()
        output.append(['', '', '', '', '', '' ,'', ''])
        conn.close()
        screen = AnchorLayout()

        self.table = MDDataTable(
            pos_hint={'center_x': .5, 'center_y': .5},
            use_pagination=True,
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
        conn = ConnectionDatabase.getConnection()
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
                  self.ids.vencimento.text,
                  COD_BARRAS)

        c.execute(sql_command, values)
        conn.commit()
        conn.close()

        popup = Popup(title='ATUALIZAR DADOS DO PRODUTO',
                      content=Label(text='Produto atualizado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'estoque'
            
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

        sql_command = f"select * from fornecedor WHERE cnpj='{CNPJ_FORNECEDOR}' and nome='{NOME_FORNECEDOR}';"

        c.execute(sql_command)  
        output = c.fetchall()
        output.append(['', '', '', '', '', '' ,'', ''])
        print(output)
        conn.close()
        screen = AnchorLayout()

        self.table = MDDataTable(
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
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

        popup = Popup(title='DELETAR FORNECEDOR',
                      content=Label(text='Fornecedor deletado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

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
        self.parent.current = 'cadastrar_conta'

    def switchAlterar(self):
        self.parent.current = 'alterar_estabelecimento'

    def switchConsultar(self):
        self.parent.current = 'consultar_estabelecimento'

    def switchModificar(self):
        self.parent.current = 'alterar_conta'

    def switchRemover(self):
        self.parent.current = 'remover_estabelecimento'

    def switchExcluir(self):
        self.parent.current = 'remover_conta'

    def switchAtivas(self):
        self.parent.current = 'consultar_contas_ativas'

    def switchPassadas(self):
        self.parent.current = 'consultar_contas_passadas'

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

class ConsultarEstabelecimento(Screen):
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
        self.parent.current = 'tabela_busca_estabelecimento'

    def buscar(self):
        global COD_ESTABELECIMENTO
        COD_ESTABELECIMENTO = self.ids.codigo.text
        global NOME_ESTABELECIMENTO
        NOME_ESTABELECIMENTO = self.ids.nome.text


class TabelaBuscaEStabelecimento(Screen):

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

        sql_command = f"select * from estabelecimento WHERE codigo='{COD_ESTABELECIMENTO}' AND nome='{NOME_ESTABELECIMENTO}';"

        c.execute(sql_command)  
        output = c.fetchall()
        output.append(['', '', '', '', '', '' ,''])
        print(output)
        conn.close()
        screen = AnchorLayout()

        self.table = MDDataTable(
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("CODIGO", dp(30)),
                ("NOME", dp(40)),
                ("BAIRRO", dp(40)),
                ("RUA", dp(30)),
                ("CEP", dp(30)),
                ("CIDADE", dp(30)),
                ("NUMERO", dp(25))
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


class RemoverEstabelecimento(Screen):
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

        sql_command = f"delete from estabelecimento WHERE codigo='{self.ids.codigo.text}' and nome='{self.ids.nome.text}';"

        c.execute(sql_command)  
        conn.commit()
        conn.close()

        popup = Popup(title='DELETAR ESTABELECIMENTO',
                      content=Label(text='Estabelecimento deletado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()


class ConsultaContasAtivas(Screen):
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

        sql_command = f"SELECT * FROM CONTA WHERE (conta.DATA_VENCIMENTO - current_date) >= 0;"

        c.execute(sql_command)  
        output = c.fetchall()
        output.append(['', '', '', '', '', '' ,''])
        print(output)
        conn.close()
        screen = AnchorLayout()

        self.table = MDDataTable(
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("COD_BARRAS", dp(60)),
                ("TIPO", dp(40)),
                ("VALOR", dp(30)),
                ("DATA_VENCIMENTO", dp(32)),
                ("DATA_PAGAMENTO", dp(32)),
                ("PAGO", dp(30)),
                ("CODIGO_ESTABELECIMENTO", dp(25))
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

class ConsultarContasPassadas(Screen):
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

        sql_command = f"SELECT * FROM CONTA WHERE (conta.DATA_VENCIMENTO - current_date) < 0;"

        c.execute(sql_command)  
        output = c.fetchall()
        output.append(['', '', '', '', '', '' ,''])
        print(output)
        conn.close()
        screen = AnchorLayout()

        self.table = MDDataTable(
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("COD_BARRAS", dp(60)),
                ("TIPO", dp(40)),
                ("VALOR", dp(30)),
                ("DATA_VENCIMENTO", dp(32)),
                ("DATA_PAGAMENTO", dp(32)),
                ("PAGO", dp(30)),
                ("CODIGO_ESTABELECIMENTO", dp(25))
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

class RemoverConta(Screen):
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

        sql_command = f"delete from conta WHERE cod_barras='{self.ids.cod_barras.text}';"

        c.execute(sql_command)  
        conn.commit()
        conn.close()

        popup = Popup(title='DELETAR CONTA',
                      content=Label(text='Conta deletada com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

class CadastrarConta(Screen):
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

        if(self.ids.pago.text == 's'):
            self.ids.pago.text = 'true'
        else:
            self.ids.pago.text = 'false'
  
        if(self.ids.data_pagamento.text != ''):
            sql_command = "INSERT INTO conta (cod_barras, tipo, valor, data_vencimento, data_pagamento, pago, codigo_estabelecimento) VALUES(%s, %s, %s, %s, %s,%s,%s)"
            values = (self.ids.cod_barras.text,
                      self.ids.tipo.text,
                      self.ids.valor.text,
                      self.ids.data_vencimento.text,
                      self.ids.data_pagamento.text,
                      self.ids.pago.text,
                      self.ids.codigo_estabelecimento.text)
        else:
            sql_command = "INSERT INTO conta (cod_barras, tipo, valor, data_vencimento, pago, codigo_estabelecimento) VALUES(%s, %s, %s, %s, %s,%s)"
            values = (self.ids.cod_barras.text,
                      self.ids.tipo.text,
                      self.ids.valor.text,
                      self.ids.data_vencimento.text,
                      self.ids.pago.text,
                      self.ids.codigo_estabelecimento.text)

        c.execute(sql_command, (values))    
        conn.commit()
        conn.close()

        self.ids.cod_barras.text = ''
        self.ids.tipo.text = ''
        self.ids.valor.text = ''
        self.ids.data_vencimento.text = ''
        self.ids.data_pagamento.text = ''
        self.ids.pago.text = ''
        self.ids.codigo_estabelecimento.text = ''        

        popup = Popup(title='CADASTRAR CONTA',
                      content=Label(text='Conta cadastrada com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'fornecedores'

class AlterarConta(Screen):
    def recolherDados(self):    
        global COD_BARRAS
        COD_BARRAS = self.ids.cod_barras.text
    
    def switchAtualiza(self):
        self.parent.current = 'alterar_conta2'
    
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

class AlterarConta2(Screen):

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

        if(self.ids.pago.text == 's'):
            self.ids.pago.text = 'true'
        else:
            self.ids.pago.text = 'false'
  
        if(self.ids.data_pagamento.text != ''):
            sql_command = f"""update conta
                            set cod_barras=%s,
                                tipo=%s,
                                valor=%s,
                                data_vencimento=%s,
                                data_pagamento=%s,
                                pago=%s,
                                codigo_estabelecimento=%s
                            where cod_barras=%s;"""

            values = (self.ids.cod_barras.text,
                      self.ids.tipo.text,
                      self.ids.valor.text,
                      self.ids.data_vencimento.text,
                      self.ids.data_pagamento.text,
                      self.ids.pago.text,
                      self.ids.codigo_estabelecimento.text,
                      COD_BARRAS)
        else:
            sql_command = f"""update conta 
                            set cod_barras=%s,
                                tipo=%s,
                                valor=%s,
                                data_vencimento=%s,
                                data_pagamento=null,
                                pago=%s,
                                codigo_estabelecimento=%s
                            where cod_barras=%s;;"""
            values = (self.ids.cod_barras.text,
                      self.ids.tipo.text,
                      self.ids.valor.text,
                      self.ids.data_vencimento.text,
                      self.ids.pago.text,
                      self.ids.codigo_estabelecimento.text,
                      COD_BARRAS)

        c.execute(sql_command, values)
        conn.commit()
        conn.close()

        popup = Popup(title='ATUALIZAR DADOS DA CONTA',
                      content=Label(text='CONTA atualizada com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'fornecedores'


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
sm.add_widget(AlterarFuncionario2(name='alterar_funcionario_2'))
sm.add_widget(EstoquePage(name='estoque'))
sm.add_widget(CadastrarProduto(name='cadastrar_produto'))
sm.add_widget(ConsultarEstoque(name='consultar_estoque'))
sm.add_widget(AtualizarEstoque(name='atualizar_estoque'))
sm.add_widget(AtualizarEstoque_2(name='atualizar_estoque_2'))
sm.add_widget(TabelaBuscaEstoque(name='tabela_busca_estoque'))
sm.add_widget(RemoverProduto(name='remover_produto'))
sm.add_widget(LoginPage(name='login'))
sm.add_widget(FornecedoresPage(name='fornecedores'))
sm.add_widget(CadastrarFornecedor(name='cadastrar_fornecedor'))
sm.add_widget(ConsultarFornecedor(name='consultar_fornecedor'))
sm.add_widget(AlterarFornecedor(name='alterar_fornecedor'))
sm.add_widget(RemoverFornecedor(name='remover_fornecedor'))
sm.add_widget(EstabelecimentoPage(name='estabelecimento'))
sm.add_widget(CadastrarEstabelecimento(name='CadastrarEstabelecimento'))
sm.add_widget(AlterarEstabelecimento(name='alterar_estabelecimento'))
sm.add_widget(AlterarEstabelecimento2(name='alterar_estabelecimento2'))
sm.add_widget(ConsultarEstabelecimento(name='consultar_estabelecimento'))
sm.add_widget(TabelaBuscaEStabelecimento(name='tabela_busca_estabelecimento'))
sm.add_widget(RemoverEstabelecimento(name='remover_estabelecimento'))
sm.add_widget(ConsultaContasAtivas(name='consultar_contas_ativas'))
sm.add_widget(ConsultarContasPassadas(name='consultar_contas_passadas'))
sm.add_widget(RemoverConta(name='remover_conta'))
sm.add_widget(CadastrarConta(name='cadastrar_conta'))
sm.add_widget(AlterarConta(name='alterar_conta'))
sm.add_widget(AlterarConta2(name='alterar_conta2'))

class Main(MDApp):
    def build(self):
        
        ####################
        ###EXEMPLO DE USO###
        ####################

        ##conn = ConnectionDatabase.getConnection()
        ##c = conn.cursor()
        ##conn.close()
        
        return Builder.load_string(KV)


Main().run()
