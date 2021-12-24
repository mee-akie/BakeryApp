from re import A
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.checkbox import CheckBox
from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton
from kivy.uix.label import Label
from kivymd.uix.behaviors import FocusBehavior
import psycopg2
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.datatables import MDDataTable
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp
from kivy.core.window import Window
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivy.uix.popup import Popup
from kivymd.uix.menu import MDDropdownMenu
from utils.connectionDatabase import ConnectionDatabase
from kivymd.uix.dropdownitem import MDDropDownItem
from datetime import date


# define um tamanho de tela padrao quando rodamos o main.py
Window.size = (400, 650)


# variaveis globais
CPF_FUNCIONARIO = ''
COD_ESTABELECIMENTO = ''
COD_BARRAS = ''
CPF_FUNCIONARIO_LOGADO = ''

DADOS_PRODUTO = ()


KV = '''
#:include FuncionarioScreen.kv
#:include HomeScreen.kv
#:include EstoqueScreen.kv
#:include Login.kv
#:include VendaScreen.kv
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:set toolbarColor get_color_from_hex("#854442")


ScreenManager:
    LoginPage:
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
    VendaPage:
    CadastroVenda:


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

class VendaPage(Screen):

    pagina = 1

    def __init__(self, **kwargs):
        super(Screen,self).__init__(**kwargs)
        self.criaTabela()
      
    def pagina_anterior(self, *args):
        self.pagina-=1
        self.criaTabela()
    
    def pagina_posterior(self, *args):
        self.pagina+=1
        self.criaTabela()

    def criaTabela(self):

        #prevenindo que a pagina solicitada seja negativa, evitando erros
        if self.pagina <= 0:
            self.pagina = 1
        
        #iniciando conexao, criando o cursor
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()
    
        c.execute("SET search_path TO padaria;")
        string_busca = "select vende.dt_venda, vende.valor_total, cliente.nome from vende "
        string_busca += "left join cliente on cliente.cpf = vende.cpf "
        string_busca += "order by vende.dt_venda desc limit 5 offset (" + str(self.pagina) + "-1)*5"
        c.execute(string_busca)
        output = c.fetchall()

        #caso a pagina solicitada nao possua dados, volta para a pagina anterior
        if c.rowcount == 0:
            self.pagina-=1
            c.close()
            self.criaTabela()
        #caso geral, prrenchimento da tabela com os dados requisitados
        else:
            c.close()
            self.table = MDDataTable(
                pos_hint={'center_x': .5, 'center_y': .5},
                size_hint=(0.9, 0.6),
                column_data=[
                    ("Data de Venda", dp(40)),
                    ("Valor Total", dp(40)),
                    ("Nome Cliente", dp(30))
                ],
                sorted_on="Data de Venda",
                sorted_order="DSC",
                elevation=2,
                row_data=output
            )

            #inserindo tabela na tela
            self.add_widget(self.table)

        

    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchCadastroVenda(self):
        self.parent.current = 'cadastro_venda'

class CadastroVenda(Screen):

    posicaoProduto = 0

    def __init__(self, **kwargs):
        super(Screen,self).__init__(**kwargs)

    def switchVendas(self):
        self.parent.transition.direction = 'right'
        self.parent.current = 'venda'

    def registrar_venda(self):
        
        self.ids.lbl_success.text = ""

        if self.valida_produtos() and self.valida_cliente():
            self.ids.lbl_error.text = ""

            #armazenando valores em variaves locais
            valor_total = str(self.ids.valor_total.text).replace(",", ".").replace("R$ ", "")
            global CPF_FUNCIONARIO_LOGADO
            cpfCliente = str(self.ids.cpf_cliente.text).replace("-", "").replace(".", "")

            #inserindo venda
            conn2 = ConnectionDatabase.getConnection()
            c2 = conn2.cursor()
            c2.execute("SET search_path TO padaria;")
            c2.execute(f"insert into vende (dt_venda, valor_total, fcodigo_funcionario, cpf) "+
	                    f"values (now(), {valor_total}, " + 
                        f"(select codigo_func from funcionario where cpf = '{CPF_FUNCIONARIO_LOGADO}'), '{cpfCliente}')")
            conn2.commit()
            #buscando valor da primary key da venda gerada
            c2.execute(f"select cod_venda from vende where cpf = '{cpfCliente}' " +
	                    f"and fcodigo_funcionario = " +
                        f" (select codigo_func from funcionario where cpf = '{CPF_FUNCIONARIO_LOGADO}') " +
                        f" order by dt_venda desc limit 1")

            output = c2.fetchall()
            conn2.close()
            
            #armazenando cod_venda gerado
            for row in output:
                cod_venda = row[0]
	                    
            #buscando produtos vendidos
            for numProduto in range(1, self.posicaoProduto+1):
                #armazenando o codigo do produto 
                codigoProduto = eval("self.produto" + str(numProduto) + ".text")
                #armazenando a quantidade solicitada do produto            
                qtdProduto = int(eval("self.quantidadeProduto" + str(numProduto) + ".text"))
                
                #inserindo produto e sua quantidade na tabela produto_vendido
                conn3 = ConnectionDatabase.getConnection()
                c3 = conn3.cursor()
                c3.execute("SET search_path TO padaria;")
                c3.execute(f"insert into produto_vendido (quantidade, cod_venda, cod_barras) " +
	                        f"values ({qtdProduto}, {cod_venda}, {codigoProduto})")

                # diminuindo a quantidade do produto no estoque
                c3.execute(f"update produto set qtd_estoque = " +
                            f"((select qtd_estoque from produto where cod_barras = '{codigoProduto}') - {qtdProduto}) " +
                            f"where cod_barras = '{codigoProduto}'")
                conn3.commit()
                conn3.close()

            self.ids.lbl_success.text = "Venda Registrada com Sucesso"
              
    def adicionaProduto(self):
        #posicao variavel do textBox
        posicaoTextBox = 0.25 - (self.posicaoProduto/10)
        #atualizando o numero de produtos na tela
        self.posicaoProduto+=1

        #criando um textField de codigo de produto
        exec("self.produto"+ str(self.posicaoProduto) + " = MDTextField(mode='rectangle')")
        exec("self.produto"+ str(self.posicaoProduto) + ".hint_text = 'Produto "+ str(self.posicaoProduto) + "'")
        exec("self.produto"+ str(self.posicaoProduto) + ".size_hint = (0.6, None)")
        exec("self.produto"+ str(self.posicaoProduto) + ".pos_hint = {'x': .1, 'y': posicaoTextBox}")

        #criando um textField de quantidade de produto
        exec("self.quantidadeProduto"+ str(self.posicaoProduto) + " = MDTextField(mode='rectangle')")
        exec("self.quantidadeProduto"+ str(self.posicaoProduto) + ".hint_text = 'Qtd'")
        exec("self.quantidadeProduto"+ str(self.posicaoProduto) + ".size_hint = (0.1, None)")
        exec("self.quantidadeProduto"+ str(self.posicaoProduto) + ".pos_hint = {'x': .8, 'y': posicaoTextBox}")

        #reposicionando o botado de adicioanr produto
        self.ids.btn_adiciona_produto.pos_hint = {'x': .1, 'y': posicaoTextBox - 0.1}

        #adicionando os texts de codigo e quantidade na tela
        exec("self.add_widget(self.produto"+ str(self.posicaoProduto) + ")")
        exec("self.add_widget(self.quantidadeProduto"+ str(self.posicaoProduto) + ")")

    def valida_cliente(self):
        
        #validando cpf
        cpfCliente = self.ids.cpf_cliente.text
        cpfCliente = str(cpfCliente).replace("-","").replace(".","")
        
        #verificando se ha somente numeros no cpf
        try:
            cpfInteiro = int(cpfCliente)
        except:
           self.ids.lbl_error.text = "CPF Inválido"
           return False 
        
        #verificando a quantidade de numeros do cpf
        if len(str(cpfInteiro)) != 11:
            self.ids.lbl_error.text = "CPF Inválido"
            return False 

        #verifica se cpfCliente ja nao existe na tabela de dados
        conn1 = ConnectionDatabase.getConnection()
        c1 = conn1.cursor()
        c1.execute("SET search_path TO padaria;")
        c1.execute(f"select 1 from cliente where cpf = '{cpfCliente}'")

        #se ja existir o usuario cadastrado, nao e necessario validar
        if c1.rowcount != 0:
            conn1.close()
            return True

        #valida nome cliente
        nomeCliente = self.ids.nome_cliente.text
        if len(nomeCliente) < 5:
            self.ids.lbl_error.text = "Nome do cliente curto"
            return False

        if " " not in nomeCliente:
            self.ids.lbl_error.text = "Insira o sobrenome do cliente"
            return False

        #validando data de nascimento
        dataNasc = self.ids.data_nascimento_cliente.text
        
        #valida data inteira
        if len(dataNasc) != 10:
            self.ids.lbl_error.text = "Data de Nascimento Inválida"
            return False 

        #valida mes
        mesNasc = int(dataNasc[3] + dataNasc[4])
        if mesNasc < 1 or mesNasc > 12:
            self.ids.lbl_error.text = "Mês da Data de Nascimento Inválido"
            return False 

        #dia maximo para cada mes
        switch = {
            "2" : 28,
            "4" : 30,
            "6" : 30,
            "9" : 30,
            "11": 30,
            "1" : 31,
            "3" : 31,
            "5" : 31,
            "7" : 31,
            "8" : 31,
            "10": 31, 
            "12": 31
        }

        #valida dia
        diaNasc = int(dataNasc[0] + dataNasc[1])
        diaMaximo = switch.get(str(mesNasc), 0)
        if diaNasc < 1 or diaNasc > diaMaximo:
            self.ids.lbl_error.text = "Dia da Data de Nascimento Inválido"
            return False 

        #valida ano
        anoNasc = int(dataNasc[6] + dataNasc[7] + dataNasc[8] + dataNasc[9])
        anoAtual = date.today().year
        if anoNasc < (anoAtual - 110)  or anoNasc > (anoAtual - 5):
            self.ids.lbl_error.text = "Ano da Data de Nascimento Inválido"
            return False 

        if dataNasc[2] != "/" or dataNasc[5] != "/":
            self.ids.lbl_error.text = "Barras da Data de Nascimento Inválidas"
            return False 

        dataNascBD = str(anoNasc) + "-" + str(mesNasc) + "-" + str(diaNasc)
        #cliente novo, necessario inserir na tabela cliente do bd
        c1.execute(f"insert into cliente (nome, cpf, datanasc) "+
	                f"values ('{nomeCliente}', '{cpfCliente}', '{dataNascBD}')")
        conn1.commit()
        conn1.close()

        return True

    def valida_produtos(self):
        
        somatorio = 0

        #resetando o exibidor do somatorio
        self.ids.valor_total.text = "------------------------------------"

        if self.posicaoProduto == 0:
             self.ids.lbl_error.text = "Insira ao menos um produto na venda"
             return False

        #para cada produto criado e buscado seu respectivo preco e o estoque 
        for numProduto in range(1, (self.posicaoProduto+1)):
            
            #armazenando o codigo do produto 
            codigoProduto = eval("self.produto" + str(numProduto) + ".text")
            
            #armazenando a quantidade solicitada do produto
            try:
                qtdProduto = int(eval("self.quantidadeProduto" + str(numProduto) + ".text"))
            except:
                self.ids.lbl_error.text = "Quantidade informada do Produto " + str(numProduto) + " é inválida"
                return False

            #validando se a quantidade inserida e pelo menos 1
            if qtdProduto < 1:
                self.ids.lbl_error.text = "Quantidade informada do Produto " + str(numProduto) + " é menor que 1"
                return False

            #buscando o preco e o estoque do produto
            conn = ConnectionDatabase.getConnection()
            c = conn.cursor()
            c.execute("SET search_path TO PADARIA;")
            c.execute(f"select preco, qtd_estoque from produto where cod_barras = '{codigoProduto}'")
            output = c.fetchall()
            

            if c.rowcount == 0:
                #produto nao encontrado, necessario informar o usuario
                self.ids.lbl_error.text = "Produto " + str(numProduto) + " não encontrado"
                return False

            #fechando conexao
            c.close()
            conn.close()

            for row in output:
                precoProduto = row[0]
                quantidadeProdutoNoEstoque = row[1]
                
            #verifica se ha quantidade de produtos suficientes no estoque
            if qtdProduto > quantidadeProdutoNoEstoque:
                #quantidade no estoque insuficiente, necessario informar o usuario
                self.ids.lbl_error.text = "Quantidade insuficiente do Produto " + str(numProduto) + " no estoque"
                return False
                
            #calcula preco de venda do respectivo produto e soma ao valor total
            somatorio += (precoProduto * qtdProduto)

        #mostrando o resultado ao usuario
        self.ids.valor_total.text = "R$ " + str(somatorio).replace(".", ",")

        return True

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
            global CPF_FUNCIONARIO_LOGADO 
            CPF_FUNCIONARIO_LOGADO = cpfUsuario
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
class HomePage(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchVendas(self):
        self.parent.current = 'venda'

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

    def switchVendas(self):
        self.parent.current = 'venda'




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
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        sql_command = f"select * from funcionario WHERE cpf='{CPF_FUNCIONARIO}' and codigo_estabelecimento={COD_ESTABELECIMENTO};"
        c.execute("SET search_path to padaria;")
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

    def switchVendas(self):
        self.parent.current = 'venda'



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
            host = "ec2-44-198-211-34.compute-1.amazonaws.com",
            database = "ddj7ffdunshjqf", 
            user = "vuxxgxylynkvnk",
            password = "e7f1713e3c7c4907b83a8e412f5373c52e1bf5e7a741e6667957bb41bcbecd69",
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
            host = "ec2-44-198-211-34.compute-1.amazonaws.com",
            database = "ddj7ffdunshjqf", 
            user = "vuxxgxylynkvnk",
            password = "e7f1713e3c7c4907b83a8e412f5373c52e1bf5e7a741e6667957bb41bcbecd69",
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

class Main(MDApp):
    def build(self):
        
        ####################
        ###EXEMPLO DE USO###
        ####################

        ##conn = ConnectionDatabase.getConnection()
        ##c = conn.cursor()
        ##conn.close()


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
        sm.add_widget(LoginPage(name='login'))
        sm.add_widget(VendaPage(name='venda'))
        sm.add_widget(CadastroVenda(name='cadastro_venda'))

        self.theme_cls.primary_palette = "DeepOrange"
        
        return Builder.load_string(KV)


Main().run()
