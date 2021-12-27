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
    CadastrarADM_AtenCaixa:
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
        if self.ids.nome.text == '' or self.ids.cpf.text == '' or self.ids.salario.text == '' or self.ids.codigo_estabelecimento.text == '':
            popup = Popup(title='ERR0 - CADASTRAR FUNCIONÁRIO',
                            content=Label(text='Não foi possível realizar o cadastro.\nAlguns dados obrigatórios não foram\npreenchidos.'),
                            size_hint=(None, None),
                            size=(300, 150),
                            background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return

        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        
        c = conn.cursor()

        # Add dados na tabela de Funcionario
        sql_command = "INSERT INTO FUNCIONARIO (NOME, CPF, SALARIO, FERIAS, CODIGO_ESTABELECIMENTO, SENHA) VALUES(%s, %s, %s, %s, %s, %s)"
        values = (self.ids.nome.text,
                  self.ids.cpf.text,
                  self.ids.salario.text,
                  self.ids.ferias.text,
                  self.ids.codigo_estabelecimento.text,
                  self.ids.senha.text)

        c.execute(sql_command, (values))	
        conn.commit()
        conn.close()

        # valores auxiliares para cadastrar ADM/Atendente de caixa
        global CPF_FUNCIONARIO
        CPF_FUNCIONARIO = self.ids.cpf.text
        global COD_ESTABELECIMENTO
        COD_ESTABELECIMENTO = self.ids.codigo_estabelecimento.text

        self.ids.nome.text = ''
        self.ids.cpf.text = ''
        self.ids.salario.text = ''
        self.ids.ferias.text = ''
        self.ids.codigo_estabelecimento.text = ''
        self.ids.senha.text = ''

        self.parent.current = 'cadastrarADM_AtendCaixa'


class CadastrarADM_AtenCaixa(Screen):
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

        if (self.ids.adm.text).lower() == 'sim':
            search = f"select codigo_func from funcionario where cpf='{CPF_FUNCIONARIO}' and codigo_estabelecimento={COD_ESTABELECIMENTO}"
            c.execute(search)
            output = c.fetchall()

            sql_command = "INSERT INTO ADMINISTRADOR (FCODIGO_FUNCIONARIO, ESPECIALIDADE) VALUES(%s, %s)"
            values = (output[0], self.ids.especialidade.text)
            print('==============')
            print(values)
            c.execute(sql_command, (values))	
            conn.commit()

        if (self.ids.atendente.text).lower() == 'sim':
            search = f"select codigo_func from funcionario where cpf='{CPF_FUNCIONARIO}' and codigo_estabelecimento={COD_ESTABELECIMENTO}"
            c.execute(search)
            output = c.fetchall()

            sql_command = "INSERT INTO ATENDENTE_CAIXA (FCODIGO_FUNCIONARIO, NIVEL_ESCOLARIDADE) VALUES(%s, %s)"
            values = (output[0], self.ids.escolaridade.text)
            c.execute(sql_command, (values))	
            conn.commit()

        conn.close()

        self.ids.especialidade.text = ''
        self.ids.escolaridade.text = ''
        self.ids.adm.text = ''
        self.ids.atendente.text = ''

        popup = Popup(title='CADASTRAR FUNCIONÁRIO',
                content=Label(text='Funcionario cadastrado com sucesso'),
                size_hint=(None, None),
                size=(300, 150),
                background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()


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
        self.ids.cpf.text = ''
        self.ids.codigo_estabelecimento.text = ''
        self.ids.nome.text = ''


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

        lista_atributos = [NOME_FUNC,
                           CPF_FUNCIONARIO,
                           COD_ESTABELECIMENTO]
        sql_command = ''
        lista_values = []
        comValor = 0
        lista_atributos_query = []
        aux = 0

        for atributo in lista_atributos:
            if atributo != '':
                comValor += 1
                if aux == 0:
                    lista_atributos_query.append("nome")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 1:
                    lista_atributos_query.append("cpf")
                    lista_values.append(atributo)

                if aux == 2:
                    lista_atributos_query.append("codigo_estabelecimento")
                    lista_values.append(atributo)

            aux += 1


        if comValor == 0:
            popup = Popup(title='ERRO - BUSCA DE FUNCIONARIO',
                    content=Label(text='Não foi informado nenhum dado\npara realizar a busca'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return

        sql_command = CriaQuery_SELECT("funcionario", lista_atributos_query)
        c.execute(sql_command, tuple(lista_values))
        output = c.fetchall()

        if len(output) == 0:
            popup = Popup(title='ERRO - BUSCA DE FUNCIONARIO',
                    content=Label(text='Não foi possível encontrar\nnenhum funcionário com os\ndados fornecidos.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return

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
        if self.ids.cpf.text == '' or self.ids.codigo_estabelecimento.text == '':
            popup = Popup(title='ERR0 - REMOVER FUNCIONÁRIO',
                            content=Label(text='Não foi possível remover o funcionário.\nAlguns dados não foram preenchidos.'),
                            size_hint=(None, None),
                            size=(300, 150),
                            background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return

        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
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

    def recolherDados(self):	
        global CPF_FUNCIONARIO
        CPF_FUNCIONARIO = self.ids.cpf.text

        if self.ids.cpf.text == '':
            popup = Popup(title='ERRO - ATUALIZAR FUNCIONARIO',
                    content=Label(text='Não foi informado nenhum dado\npara realizar a busca'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return

        self.ids.cpf.text = ''
        self.parent.current = 'alterar_funcionario_2'


class AlterarFuncionario2(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def alterar(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        c = conn.cursor()

        lista_atributos = [self.ids.nome.text,
                            self.ids.cpf.text,
                            self.ids.salario.text,
                            self.ids.ferias.text,
                            self.ids.codigo_estabelecimento.text]
        sql_command = ''
        lista_values = []

        comAlteracoes = 0
        lista_comAlteracoes = []
        aux = 0

        for atributo in lista_atributos:
            if atributo != '':
                comAlteracoes += 1
                if aux == 0:
                    lista_comAlteracoes.append("nome")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 1:
                    lista_comAlteracoes.append("cpf")

                if aux == 2:
                    lista_comAlteracoes.append("salario")
                    lista_values.append(f"{FormataFloat(atributo)}")

                if aux == 3:
                    lista_comAlteracoes.append("ferias")
                    lista_values.append(f"{ConversorData(atributo)}")

                if aux == 4:
                    lista_comAlteracoes.append("codigo_estabelecimento")
            aux += 1

        lista_values.append(f"{CPF_FUNCIONARIO}")

        if(comAlteracoes == 0):
            popup = Popup(title='ATUALIZAR DADOS DO FUNCIONARIO',
                    content=Label(text='NENHUMA alteração dos dados\ndo funcionário foi feita.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return

        sql_command = CriaQuery_UPDATE("funcionario", lista_comAlteracoes, "cpf")

        c.execute(sql_command, tuple(lista_values))

        conn.commit()
        conn.close()

        popup = Popup(title='ATUALIZAR DADOS DE FUNCIONARIO',
                      content=Label(text='Funcionario atualizado com SUCESSO.'),
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
        if self.ids.fabricacao.text == '' or self.ids.vencimento.text == '' or self.ids.cod_barras.text == ''or self.ids.nome.text == '' or self.ids.preco.text == '' or self.ids.categoria.text == '' or self.ids.qtd_estoque.text == '' or self.ids.fabricante.text == '':
            popup = Popup(title='ERR0 - CADASTRAR PRODUTO',
                            content=Label(text='Não foi possível realizar o cadastro.\nAlguns dados obrigatórios não foram\npreenchidos.'),
                            size_hint=(None, None),
                            size=(300, 150),
                            background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return

        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        
        c = conn.cursor()

        fabricacao = ConversorData(self.ids.fabricacao.text)
        vencimento = ConversorData(self.ids.vencimento.text)
        cod_barras = self.ids.cod_barras.text
        nome = (self.ids.nome.text).lower()
        preco = FormataFloat(self.ids.preco.text)
        categoria = (self.ids.categoria.text).lower()
        qts_estoque = self.ids.qtd_estoque.text
        fabricante = (self.ids.fabricante.text).lower()


        if fabricacao == '' or vencimento == '' or cod_barras == '' or nome == '' or preco == '' or categoria == '' or qts_estoque == '' or fabricante == '':

            popup = Popup(title='ERRO - CADASTRAR PRODUTO',
                    content=Label(text='Alguns campos não foram\npreenchidos. Por favor, preencha\n todos os dados.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return   

        sql_command = "INSERT INTO PRODUTO (COD_BARRAS, NOME, NOME_FABRICANTE, PRECO, DATA_FABRICACAO, CATEGORIA, QTD_ESTOQUE, DATA_VENCIMENTO) VALUES(%s, %s, %s, %s, %s, %s, %s, %s)"

        values = (cod_barras,
                  nome,
                  fabricante,
                  preco,
                  fabricacao,
                  categoria,
                  qts_estoque,
                  vencimento)

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
                      content=Label(text='Produto cadastrado com sucesso.'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()
        self.parent.current = 'estoque'


class RemoverProduto(Screen):
    def remover(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        
        c = conn.cursor()

        if (self.ids.cod_barras.text != ''):
            sql_command = f"delete from produto WHERE cod_barras='{self.ids.cod_barras.text}';"
        
        else:
            popup = Popup(title='ERRO - EXCLUSÃO DO PRODUTO',
                    content=Label(text='Não foi informado nenhum código\n de barras para realizar a remoção\ndo produto.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return

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
        self.ids.cod_barras.text = ''
        self.ids.nome.text = ''
        self.ids.categoria.text = ''
        self.ids.nome_fabricante.text = ''
    

class TabelaBuscaEstoque(Screen):
    def switchEstoque(self):
        self.parent.current = 'estoque'
        
    def tabela(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        c = conn.cursor()

        sql_command = ''

        lista_atributos = [COD_BARRAS,
                           NOME_PROD,
                           CATEGORIA_PROD,
                           NOME_FABRIC]
        sql_command = ''
        lista_values = []
        comValor = 0
        lista_atributos_query = []
        aux = 0

        for atributo in lista_atributos:
            if atributo != '':
                comValor += 1
                if aux == 0:
                    lista_atributos_query.append("cod_barras")
                    lista_values.append(atributo)

                if aux == 1:
                    lista_atributos_query.append("nome")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 2:
                    lista_atributos_query.append("categoria")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 3:
                    lista_atributos_query.append("nome_fabricante")
                    lista_values.append(f"{(atributo).lower()}")

            aux += 1

        if comValor == 0:
            popup = Popup(title='ERRO - BUSCAR PRODUTO',
                    content=Label(text='Não foi informado nenhum dado\npara realizar a busca'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return

        sql_command = CriaQuery_SELECT("produto", lista_atributos_query)
        c.execute(sql_command, tuple(lista_values))
        output = c.fetchall()

        if len(output) == 0:
            popup = Popup(title='ERRO - BUSCAR PRODUTO',
                    content=Label(text='Não foi possível encontrar\nnenhum produto com os\ndados fornecidos.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return

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
                ("NOME FABRICANTE", dp(40)),
                ("PREÇO", dp(30)),
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

        if self.ids.cod_barras.text == '':
            popup = Popup(title='ERRO - ATUALIZAR PRODUTO',
                    content=Label(text='Não foi informado nenhum dado\npara realizar a busca'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return

        self.ids.cod_barras.text = ''
        self.parent.current = 'atualizar_estoque_2'
        
    
    def switchAtualiza(self):
        self.parent.current = 'atualizar_estoque_2'
    
    def switchEstoque(self):
        self.parent.current = 'estoque'



class AtualizarEstoque_2(Screen):
    def switchEstoque(self):
        self.parent.current = 'estoque'

    def atualizar(self):
        conn = psycopg2.connect(
            host = "localhost",
            database = "padaria", 
            user = "postgre2",
            password = "123",
            port = "5432"
        )
        c = conn.cursor()

        lista_atributos = [self.ids.fabricacao.text,
                           self.ids.vencimento.text,
                           self.ids.cod_barras.text,
                           self.ids.nome.text,
                           self.ids.preco.text,
                           self.ids.categoria.text,
                           self.ids.qtd_estoque.text,
                           self.ids.fabricante.text]
        sql_command = ''
        lista_values = []

        comAlteracoes = 0
        lista_comAlteracoes = []
        aux = 0

        for atributo in lista_atributos:
            if atributo != '':
                comAlteracoes += 1
                if aux == 0:
                    lista_comAlteracoes.append("data_fabricacao")
                    lista_values.append(f"{ConversorData(atributo)}")

                if aux == 1:
                    lista_comAlteracoes.append("data_vencimento")
                    lista_values.append(f"{ConversorData(atributo)}")

                if aux == 2: lista_comAlteracoes.append("cod_barras")

                if aux == 3:
                    lista_comAlteracoes.append("nome")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 4:
                    lista_comAlteracoes.append("preco")
                    lista_values.append(f"{FormataFloat(atributo)}")

                if aux == 5:
                    lista_comAlteracoes.append("categoria")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 6: lista_comAlteracoes.append("qtd_estoque")

                if aux == 7:
                    lista_comAlteracoes.append("nome_fabricante")
                    lista_values.append(f"{(atributo).lower()}")
            aux += 1

        lista_values.append(f"{COD_BARRAS}")

        if(comAlteracoes == 0):
            popup = Popup(title='ATUALIZAR PRODUTO',
                    content=Label(text='Nenhuma alteração do produto foi feita.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return

        sql_command = CriaQuery_UPDATE("produto", lista_comAlteracoes, "cod_barras")

        c.execute(sql_command, tuple(lista_values))
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


    
############ METODOS AUXIARES ####################

def CriaQuery_SELECT(tabela, atributos):
    sql_command = f"select * from {tabela} where "

    while(len(atributos)):
        if len(atributos) == 1:
            sql_command += f" {atributos[0]}=%s;"
            atributos.pop(0)
        else:
            sql_command += f" {atributos[0]}=%s and "
            atributos.pop(0)

    return sql_command


def CriaQuery_UPDATE(tabela, atributos, atributoReferencia):
    sql_command = f"update {tabela} set"

    while(len(atributos)):
        if len(atributos) == 1:
            sql_command += f" {atributos[0]}=%s "
            atributos.pop(0)
        else:
            sql_command += f" {atributos[0]}=%s,"
            atributos.pop(0)

    sql_command += f"where {atributoReferencia}=%s;"
    return sql_command

# Converte 'dd-mm-aaaa' para 'aaaa-mm-dd' (padrao do Postgresql)
def ConversorData(dataDesformatada):
    if dataDesformatada == '': return dataDesformatada 
    return str(dataDesformatada[len(dataDesformatada)-4:len(dataDesformatada)] + '-' + dataDesformatada[3:5] + '-' + dataDesformatada[0:2])

# Troca o caracter ',' por '.' (padrao do Postgresql)
def FormataFloat(num):
    numFormatado = num
    if ',' in num:
        numFormatado = numFormatado.replace(',', '.') 
    return numFormatado



# Gerenciador de paginas
sm = ScreenManager()
sm.add_widget(HomePage(name='home'))
sm.add_widget(FuncionarioPage(name='funcionario'))
sm.add_widget(CadastrarFuncionario(name='cadastrar_funcionario'))
sm.add_widget(CadastrarADM_AtenCaixa(name='cadastrarADM_AtendCaixa'))
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
