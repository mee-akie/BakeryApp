import time
from kivy.lang import Builder
from kivy.properties import ObjectProperty
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
NOME_FUNC = ''
COD_ESTABELECIMENTO = ''
COD_BARRAS = ''
NOME_PROD = ''
CATEGORIA_PROD = ''
NOME_FABRIC = ''
CNPJ_FORNECEDOR = ''
NOME_FORNECEDOR = '' 
NOME_ESTABELECIMENTO = ''
CPF_FUNCIONARIO_LOGADO = ''
APENAS_ATEND_CAIXA = ''
APENAS_ADM = ''
DT_ENTREGA = ''
COD_FUNC = ''
AUX = 0


KV = '''
#:include FuncionarioScreen.kv
#:include HomeScreen.kv
#:include EstoqueScreen.kv
#:include Login.kv
#:include FornecedoresScreen.kv
#:include EstabelecimentoScreen.kv
#:include VendaScreen.kv
#:include CompraFornecedorScreen.kv
#:include HistoricoTrabalho.kv

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
    VendaPage:
    CadastroVenda:
    CompraFornecedorPage:
    CadastrarCompraForn:
    SelecionarProdutos:
    ConsultarCompras:
    HistoricoTrabalhoPage:
    RegistrarHorario:
    ConsultarHistorico:
    TabelaHistoricoTrabalho:

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
        self.parent.transition.direction = 'right'
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.transition.direction = 'right'
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.transition.direction = 'right'
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

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def switchCompraFornecedor(self):
        self.parent.current = 'compraFornecedor'

    def switchEstabelecimento(self):
        self.parent.current = 'estabelecimento'

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
    
    def switchHistoricoTrabalho(self):
        self.parent.current = 'historicoTrabalho'


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

        conn = ConnectionDatabase.getConnection()
        
        c = conn.cursor()

        sql_command = f"select * from funcionario where cpf='{self.ids.cpf.text}'"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)
        output = c.fetchall()

        if len(output) != 0:
            popup = Popup(title='ERR0 - CADASTRAR FUNCIONÁRIO',
                            content=Label(text='Não foi possível realizar o cadastro.\nJá existe um funcionario com este\nCPF cadastrado.'),
                            size_hint=(None, None),
                            size=(300, 150),
                            background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return           

        sql_command = f"select * from estabelecimento where CODIGO={self.ids.codigo_estabelecimento.text}"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)
        output = c.fetchall()

        if len(output) == 0:
            popup = Popup(title='ERR0 - CADASTRAR FUNCIONÁRIO',
                            content=Label(text='Não foi possível realizar o cadastro.\nO cód. do estabelecimento informado\nnão existe.'),
                            size_hint=(None, None),
                            size=(300, 150),
                            background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return    

        sql_command = "INSERT INTO FUNCIONARIO (NOME, CPF, SALARIO, FERIAS, CODIGO_ESTABELECIMENTO, SENHA) VALUES(%s, %s, %s, %s, %s, %s)"
        values = (self.ids.nome.text,
                  self.ids.cpf.text,
                  self.ids.salario.text,
                  self.ids.ferias.text,
                  self.ids.codigo_estabelecimento.text,
                  self.ids.senha.text)

        c.execute("SET search_path TO padaria;")
        c.execute(sql_command, (values))	
        conn.commit()
        conn.close()

        # valores auxiliares para cadastrar ADM/Atendente de caixa se o funcionario em questao tiver um desses cargos
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
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        if (self.ids.adm.text).lower() == 'sim':
            search = f"select codigo_func from funcionario where cpf='{CPF_FUNCIONARIO}' and codigo_estabelecimento={COD_ESTABELECIMENTO}"
            c.execute("SET search_path TO padaria;")
            c.execute(search)
            output = c.fetchall()

            sql_command = "INSERT INTO ADMINISTRADOR (FCODIGO_FUNCIONARIO, ESPECIALIDADE) VALUES(%s, %s)"
            values = (output[0], self.ids.especialidade.text)
            c.execute(sql_command, (values))	
            conn.commit()

        if (self.ids.atendente.text).lower() == 'sim':
            search = f"select codigo_func from funcionario where cpf='{CPF_FUNCIONARIO}' and codigo_estabelecimento={COD_ESTABELECIMENTO}"
            c.execute("SET search_path TO padaria;")
            c.execute(search)
            output = c.fetchall()

            sql_command = "INSERT INTO ATENDENTE_CAIXA (FCODIGO_FUNCIONARIO, NIVEL_ESCOLARIDADE) VALUES(%s, %s)"
            values = (output[0], self.ids.escolaridade.text)
            c.execute("SET search_path TO padaria;")
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
        global APENAS_ADM
        APENAS_ADM = self.ids.adm.text
        global APENAS_ATEND_CAIXA
        APENAS_ATEND_CAIXA = self.ids.atendente.text

        self.ids.cpf.text = ''
        self.ids.codigo_estabelecimento.text = ''
        self.ids.nome.text = ''
        self.ids.adm.text = ''
        self.ids.atendente.text = ''


class TabelaBuscaFuncionario(Screen):
    def switchFuncionario(self):
        self.parent.current = 'funcionario'


    def tabela(self):
        conn = ConnectionDatabase.getConnection()
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


        if comValor == 0 and (APENAS_ADM).lower() != "sim" and (APENAS_ATEND_CAIXA).lower() != "sim":
            popup = Popup(title='ERRO - BUSCA DE FUNCIONARIO',
                    content=Label(text='Não foi informado nenhum dado\npara realizar a busca'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return

        if (APENAS_ADM).lower() != "sim" and (APENAS_ATEND_CAIXA).lower() != "sim":
            sql_command = CriaQuery_SELECT("funcionario", lista_atributos_query)
            c.execute("SET search_path TO padaria;")
            c.execute(sql_command, tuple(lista_values))
            output = c.fetchall()

        else:
            sql_command = f"select * from funcionario"
            c.execute("SET search_path TO padaria;")
            c.execute(sql_command)
            output = c.fetchall()

        if len(output) == 0 and (APENAS_ADM).lower() != "sim" and (APENAS_ATEND_CAIXA).lower() != "sim":
            popup = Popup(title='ERRO - BUSCA DE FUNCIONARIO',
                    content=Label(text='Não foi possível encontrar\nnenhum funcionário com os\ndados fornecidos.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return

        output_2 = []

        if (APENAS_ADM).lower() == 'sim' and (APENAS_ATEND_CAIXA).lower() == 'sim':

            aux = []
            for tupla in output: aux.append(list(tupla))
            for funcionario in aux:
                c.execute("SET search_path TO padaria;")
                sql_command = f'select * from administrador where FCODIGO_FUNCIONARIO={funcionario[0]}'
                c.execute(sql_command)
                output = c.fetchall()
                if len(output) == 1: output_2.append(funcionario)

            aux = []
            for tupla in output: aux.append(list(tupla))
            for funcionario in aux:
                c.execute("SET search_path TO padaria;")
                sql_command = f'select * from ATENDENTE_CAIXA where FCODIGO_FUNCIONARIO={funcionario[0]}'
                c.execute(sql_command)
                output = c.fetchall()
                if len(output) == 1: output_2.append(funcionario)

            if len(output_2) == 0:
                popup = Popup(title='BUSCA DE FUNCIONARIO',
                    content=Label(text='Não foi possível encontrar\nnenhum administrador e\n atendente de caixa.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
                popup.open()
                self.parent.current = 'funcionario'
                return

        elif (APENAS_ADM).lower() == 'sim':

            aux = []
            for tupla in output: aux.append(list(tupla))
            for funcionario in aux:
                c.execute("SET search_path TO padaria;")
                sql_command = f'select * from administrador where FCODIGO_FUNCIONARIO={funcionario[0]}'
                c.execute(sql_command)
                output = c.fetchall()
                if len(output) == 1: output_2.append(funcionario)
            
            if len(output_2) == 0:
                popup = Popup(title='BUSCA DE FUNCIONARIO',
                    content=Label(text='Não foi possível encontrar\nnenhum administrador.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
                popup.open()
                self.parent.current = 'funcionario'
                return

        elif (APENAS_ATEND_CAIXA).lower() == 'sim':
            aux = []
            for tupla in output: aux.append(list(tupla))
            for funcionario in aux:
                c.execute("SET search_path TO padaria;")
                sql_command = f'select * from ATENDENTE_CAIXA where FCODIGO_FUNCIONARIO={funcionario[0]}'
                c.execute(sql_command)
                output = c.fetchall()
                if len(output) == 1: output_2.append(funcionario)
            
            if len(output_2) == 0:
                popup = Popup(title='BUSCA DE FUNCIONARIO',
                    content=Label(text='Não foi possível encontrar\nnenhum atendente de caixa.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
                popup.open()
                self.parent.current = 'funcionario'
                return
        
        else: output_2 = output

        output_to_list = []
        for tupla in output_2: output_to_list.append(list(tupla))
        for lista in output_to_list:
            lista.pop() #remove a senha do usuario
            lista[4] = ConversorData(lista[4], False)

        output_to_list.append(['', '', '', '', '', '' ,'', ''])
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
            row_data=output_to_list
        )

        self.add_widget(self.table)
        return screen

    def on_enter(self):
        self.tabela()


class RemoverFuncionario(Screen):

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

    def switchVendas(self):
        self.parent.current = 'venda'

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

        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        sql_command = f"select * from funcionario where cpf='{self.ids.cpf.text}' and codigo_estabelecimento={self.ids.codigo_estabelecimento.text};"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)
        output = c.fetchall()
        if len(output) == 0:
            popup = Popup(title='ERR0 - REMOVER FUNCIONÁRIO',
                            content=Label(text='Não foi possível remover o funcionário.\nNão existe um funcionario com o CPF\ne cod. do estabalecimento informado.'),
                            size_hint=(None, None),
                            size=(300, 150),
                            background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return

        sql_command = f"delete from funcionario WHERE cpf='{self.ids.cpf.text}' and codigo_estabelecimento={self.ids.codigo_estabelecimento.text};"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)	
        conn.commit()
        conn.close()
        popup = Popup(title='REMOVER FUNCIONÁRIO',
                        content=Label(text='Funcionário removido com\nsucesso.'),
                        size_hint=(None, None),
                        size=(300, 150),
                        background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()
        self.parent.current = 'funcionario'


class AlterarFuncionario(Screen):
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

    def switchVendas(self):
        self.parent.current = 'venda'

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

        if self.ids.cpf.text == '' and self.ids.nome.text == '' and self.ids.salario.text == '' and self.ids.ferias.text == '' and self.ids.codigo_estabelecimento.text == '':
            popup = Popup(title='ATUALIZAR FUNCIONARIO',
                    content=Label(text='Não foi alterado nenhum dado\ndo funcionário.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'funcionario'
            return

        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        sql_command = f"select * from funcionario where cpf='{self.ids.cpf.text}';"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)
        output = c.fetchall()
        if len(output) != 0:
            popup = Popup(title='ERRO - ATUALIZAR FUNCIONARIO',
                    content=Label(text='Já existe um funcionário\ncom o CPF informado.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.ids.cpf.text = ''
            self.ids.codigo_estabelecimento.text = ''
            self.parent.current = 'funcionario'
            return

        sql_command = f"select * from funcionario where CODIGO_ESTABELECIMENTO='{self.ids.codigo_estabelecimento.text}';"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)
        output = c.fetchall()
        if len(output) == 0:
            popup = Popup(title='ERRO - ATUALIZAR FUNCIONARIO',
                    content=Label(text='O cód. do estabelecimento\ninformado não existe.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.ids.cpf.text = ''
            self.ids.codigo_estabelecimento.text = ''

            self.parent.current = 'funcionario'
            return

        lista_atributos = [self.ids.nome.text,
                            self.ids.cpf.text,
                            self.ids.salario.text,
                            self.ids.ferias.text,
                            self.ids.codigo_estabelecimento.text,
                            self.ids.senha.text]
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
                    lista_values.append(atributo)
                if aux == 2:
                    lista_comAlteracoes.append("salario")
                    lista_values.append(f"{FormataFloat(atributo)}")

                if aux == 3:
                    lista_comAlteracoes.append("ferias")
                    lista_values.append(f"{ConversorData(atributo, True)}")

                if aux == 4:
                    lista_comAlteracoes.append("codigo_estabelecimento")
                    lista_values.append(atributo)

                if aux == 5:
                    lista_comAlteracoes.append("senha")
                    lista_values.append(atributo)     
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
        c.execute("SET search_path TO padaria;")
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


class HistoricoTrabalhoPage(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchVendas(self):
        self.parent.current = 'venda'

    def switchRegistrar(self):
        self.parent.current = 'registrarHorario'

    def switchConsultar(self):
        self.parent.current = 'consultarHistorico'


class RegistrarHorario(Screen):
    def switchHistoricoTrabalho(self):
        self.parent.current = 'historicoTrabalho'

    def registrar(self):
        if self.ids.hora_entrada_r.text == '' or self.ids.hora_saida_r.text == '' or self.ids.fcodigo_funcionario.text == '':
            popup = Popup(title='ERR0 - REGISTRAR HORÁRIO DE\nTRABALHO',
                            content=Label(text='Não foi possível realizar o registro.\nAlguns dados obrigatórios não foram\npreenchidos.'),
                            size_hint=(None, None),
                            size=(300, 150),
                            background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()

            self.ids.hora_entrada_r.text = ''
            self.ids.hora_saida_r.text = ''
            self.ids.fcodigo_funcionario.text = ''
            return

        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        sql_command = f"select * from funcionario where CODIGO_FUNC='{self.ids.fcodigo_funcionario.text}';"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)
        output = c.fetchall()
        if len(output) == 0:        
            popup = Popup(title='ERR0 - REGISTRAR HORÁRIO DE\nTRABALHO',
                            content=Label(text='Não foi possível realizar o registro.\nO cód. do funcionário informado\nnão existe.'),
                            size_hint=(None, None),
                            size=(300, 150),
                            background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()

            self.ids.hora_entrada_r.text = ''
            self.ids.hora_saida_r.text = ''
            self.ids.fcodigo_funcionario.text = ''
            return

        sql_command = "INSERT INTO HISTORICO_TRABALHO (DATA_REGISTRO, HORA_ENTRADA_R, HORA_SAIDA_R, FCODIGO_FUNCIONARIO) VALUES(current_date, %s, %s, %s)"
        values = (FormataHora(self.ids.hora_entrada_r.text),
                  FormataHora(self.ids.hora_saida_r.text),
                  self.ids.fcodigo_funcionario.text)

        c.execute("SET search_path TO padaria;")
        c.execute(sql_command, (values))	
        conn.commit()
        conn.close()

        self.ids.hora_entrada_r.text = ''
        self.ids.hora_saida_r.text = ''
        self.ids.fcodigo_funcionario.text = ''

        popup = Popup(title='REGISTRO DE HORÁRIO DE\nTRABALHO',
                      content=Label(text='Registro realizado com sucesso.'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()


class ConsultarHistorico(Screen):
    def switchHistoricoTrabalho(self):
        self.parent.current = 'historicoTrabalho'

    def switchTabela(self):
        self.parent.current = 'tabela_historicoTrabalho'

    def consultar(self):
        global COD_FUNC
        COD_FUNC = self.ids.cod_func.text
        self.ids.cod_func.text = ''


class TabelaHistoricoTrabalho(Screen):
    def switchHistoricoTrabalho(self):
        self.parent.current = 'historicoTrabalho'

    def tabela(self):
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        if COD_FUNC == '':
            popup = Popup(title='ERRO - CONSULTAR HISTÓRICO DE\nTRABALHO',
                    content=Label(text='Não foi informado o código\ndo funcionário.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'historicoTrabalho'
            return

        sql_command = f"select * from funcionario where CODIGO_FUNC={COD_FUNC}"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)
        output = c.fetchall()

        if len(output) == 0:
            popup = Popup(title='ERRO - CONSULTAR HISTÓRICO DE\nTRABALHO',
                    content=Label(text='Não existe um funcionário com\no código de funcionário informado.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'historicoTrabalho'
            return            

        sql_command = f"select * from historico_trabalho where FCODIGO_FUNCIONARIO={COD_FUNC}"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)
        output = c.fetchall()

        if len(output) == 0:
            popup = Popup(title='HISTÓRICO DE TRABALHO',
                    content=Label(text='Não foi possível encontrar\nnenhum histórico de tra-\nbalho desse funcionario.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'historicoTrabalho'
            return

        output_to_list = []
        output.append(['', '', '', '', '', '' ,'', ''])

        for tupla in output: output_to_list.append(list(tupla))
        for lista in output_to_list:
            lista[0] = ConversorData(lista[0], False)

        conn.close()

        screen = AnchorLayout()

        self.table = MDDataTable(
            pos_hint={'center_x': .5, 'center_y': .5},
            use_pagination=True,
            size_hint=(0.9, 0.6),
            column_data=[
                ("DT REGISTRO", dp(30)),
                ("HORA ENTRADA", dp(30)),
                ("HORA SAIDA", dp(30)),
                ("COD-FUNCIONARIO", dp(40))
            ],
            sorted_on="DT REGISTRO",
            sorted_order="ASC",
            elevation=2,
            row_data=output_to_list
        )

        self.add_widget(self.table)
        return screen

    def on_enter(self):
        self.tabela()


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

    def switchVendas(self):
        self.parent.current = 'venda'


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

        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        sql_command = f"select * from produto where COD_BARRAS='{self.ids.cod_barras.text}'"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)
        output = c.fetchall()

        if len(output) != 0:
            popup = Popup(title='ERRO - CADASTRAR PRODUTO',
                    content=Label(text='Já existe um produto cadastrado\ncom o código de barras informado.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return   

        fabricacao = ConversorData(self.ids.fabricacao.text, True)
        vencimento = ConversorData(self.ids.vencimento.text, True)
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

        c.execute("SET search_path TO padaria;")
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

    def switchVendas(self):
        self.parent.current = 'venda'

    def remover(self):
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        if (self.ids.cod_barras.text != ''):
            sql_command = f"select * from produto where COD_BARRAS='{self.ids.cod_barras.text}'"
            c.execute("SET search_path TO padaria;")
            c.execute(sql_command)
            output = c.fetchall()

            if len(output) == 0:
                popup = Popup(title='ERRO - EXCLUSÃO DO PRODUTO',
                        content=Label(text='Não existe um produto no estoque\ncom o código de barras informado.'),
                        size_hint=(None, None),
                        size=(300, 150),
                        background ='atlas://data/images/defaulttheme/button_pressed')
                popup.open()
                self.parent.current = 'estoque'
                return
            
            sql_command = f"delete from produto WHERE cod_barras='{self.ids.cod_barras.text}';"
            c.execute("SET search_path TO padaria;")
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

        else:
            popup = Popup(title='ERRO - EXCLUSÃO DO PRODUTO',
                    content=Label(text='Não foi informado nenhum código\n de barras para realizar a remoção\ndo produto.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return

    
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
        conn = ConnectionDatabase.getConnection()
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
        c.execute("SET search_path TO padaria;")
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


        output_to_list = []
        output.append(['', '', '', '', '', '' ,'', ''])

        for tupla in output: output_to_list.append(list(tupla))
        for lista in output_to_list:
            lista[4] = ConversorData(lista[4], False)
            lista[7] = ConversorData(lista[7], False)

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
            row_data=output_to_list,
            sorted_on="NOME",
            sorted_order="ASC",
            elevation=2
        )

        self.add_widget(self.table)
        return screen

    def on_enter(self):
        self.tabela()


class AtualizarEstoque(Screen):
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

    def switchVendas(self):
        self.parent.current = 'venda'

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
        if self.ids.fabricacao.text == '' and self.ids.vencimento.text == '' and self.ids.nome.text == '' and self.ids.preco.text == '' and self.ids.categoria.text == '' and self.ids.qtd_estoque.text == '' and self.ids.fabricante.text == '':
            popup = Popup(title='ATUALIZAR PRODUTO',
                    content=Label(text='Não foi alterado nenhum dado\ndo produto.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estoque'
            return

        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        lista_atributos = [self.ids.fabricacao.text,
                           self.ids.vencimento.text,
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
                    lista_values.append(f"{ConversorData(atributo, True)}")

                if aux == 1:
                    lista_comAlteracoes.append("data_vencimento")
                    lista_values.append(f"{ConversorData(atributo, True)}")

                if aux == 2:
                    lista_comAlteracoes.append("nome")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 3:
                    lista_comAlteracoes.append("preco")
                    lista_values.append(f"{FormataFloat(atributo)}")

                if aux == 4:
                    lista_comAlteracoes.append("categoria")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 5: lista_comAlteracoes.append("qtd_estoque")

                if aux == 6:
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

        c.execute("SET search_path TO padaria;")
        c.execute(sql_command, tuple(lista_values))
        conn.commit()
        conn.close()

        popup = Popup(title='ATUALIZAR DADOS DO PRODUTO',
                      content=Label(text='Produto atualizado com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.ids.fabricacao.text = ''
        self.ids.vencimento.text = ''
        self.ids.nome.text = ''
        self.ids.preco.text = ''
        self.ids.categoria.text = ''
        self.ids.qtd_estoque.text = ''
        self.ids.fabricante.text = ''

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

    def switchVendas(self):
        self.parent.current = 'venda'


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

    def switchVendas(self):
        self.parent.current = 'venda'

    def cadastrar(self):
        conn = ConnectionDatabase.getConnection() 
        c = conn.cursor()

        if self.ids.cnpj.text == '' or self.ids.nome.text == '' or self.ids.rua.text == '' or self.ids.estado.text == '' or self.ids.cidade.text == '' or self.ids.cep.text == '' or self.ids.numero.text or self.ids.bairro.text == '':
            popup = Popup(title='ERRO - CADASTRAR FORNECEDOR',
                    content=Label(text='Alguns campos não foram preenchidos.\nPor favor, preencha todos os campos.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.ids.cnpj.text = ''
            self.ids.nome.text = ''
            self.ids.rua.text = ''
            self.ids.estado.text = ''
            self.ids.cidade.text = ''
            self.ids.cep.text = ''
            self.ids.numero.text = ''
            self.ids.bairro.text = ''  
            self.parent.current = 'fornecedores'
            return 

        sql_command = f"select * from fornecedor where cnpj='{self.ids.cnpj.text}'"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)
        output = c.fetchall()

        if len(output) != 0:
            popup = Popup(title='ERRO - CADASTRAR FORNECEDOR',
                    content=Label(text='Já existe um fornecedor cadastrado\ncom o CNPJ informado.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.ids.cnpj.text = ''
            self.parent.current = 'fornecedores'
            return 

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

        c.execute("SET search_path TO padaria;")
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

    def switchVendas(self):
        self.parent.current = 'venda'

    def switchTabela(self):
        self.parent.current = 'tabela_busca_fornecedor'

    def buscar(self):
        global CNPJ_FORNECEDOR
        CNPJ_FORNECEDOR = self.ids.cnpj.text
        global NOME_FORNECEDOR
        NOME_FORNECEDOR = (self.ids.nome.text).lower()
        self.ids.cnpj.text = ''
        self.ids.nome.text = ''


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

    def switchVendas(self):
        self.parent.current = 'venda'

    def tabela(self):
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        if CNPJ_FORNECEDOR == '' and NOME_FORNECEDOR == '':
            popup = Popup(title='ERRO - BUSCAR FORNECEDOR',
                    content=Label(text='Não foi possível realizar a busca.\nNenhum dado do fornecedor foi\ninformado.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'fornecedores'
            return             

        sql_command = ''

        if CNPJ_FORNECEDOR != '' and NOME_FORNECEDOR == '':
            sql_command = f"select * from fornecedor WHERE cnpj='{CNPJ_FORNECEDOR}'"
            c.execute("SET search_path TO padaria;")
            c.execute(sql_command)
            output = c.fetchall()

            if len(output) == 0:
                popup = Popup(title='ERRO - BUSCAR FORNECEDOR',
                        content=Label(text='Não foi possível realizar a busca.\nNenhum fornecedor com o CNPJ\ninformado foi encontrado.'),
                        size_hint=(None, None),
                        size=(300, 150),
                        background ='atlas://data/images/defaulttheme/button_pressed')
                popup.open()
                self.parent.current = 'fornecedores'
                return      

        elif CNPJ_FORNECEDOR == '' and NOME_FORNECEDOR != '':
            sql_command = f"select * from fornecedor WHERE nome='{NOME_FORNECEDOR}';"
            c.execute("SET search_path TO padaria;")
            c.execute(sql_command)
            output = c.fetchall()

            if len(output) == 0:
                popup = Popup(title='ERRO - BUSCAR FORNECEDOR',
                        content=Label(text='Não foi possível realizar a busca.\nNenhum fornecedor com o nome\ninformado foi encontrado.'),
                        size_hint=(None, None),
                        size=(300, 150),
                        background ='atlas://data/images/defaulttheme/button_pressed')
                popup.open()
                self.parent.current = 'fornecedores'
                return 

        else:
            sql_command = f"select * from fornecedor WHERE cnpj='{CNPJ_FORNECEDOR}' and nome='{NOME_FORNECEDOR}';"
            c.execute("SET search_path TO padaria;")
            c.execute(sql_command)
            output = c.fetchall()

        if len(output) == 0:
            popup = Popup(title='BUSCAR FORNECEDOR',
                    content=Label(text='Não foi possível encontrar nenhum\nfornecedor com os dados informados.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'fornecedores'
            return              

        output.append(['', '', '', '', '', '' ,'', ''])
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

    def switchVendas(self):
        self.parent.current = 'venda'

    def remover(self):

        if self.ids.cnpj.text == '' or self.ids.nome.text == '':
            popup = Popup(title='ERRO - REMOVER FORNECEDOR',
                    content=Label(text='Não foi possível remover o fornecedor.\nAlguns dados obrigatórios não foram\ninformados.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.ids.cnpj.text = ''
            self.ids.nome.text = ''            
            self.parent.current = 'fornecedores'
            return               

        conn = ConnectionDatabase.getConnection()     
        c = conn.cursor()

        sql_command = f"select * from fornecedor WHERE cnpj='{self.ids.cnpj.text}' and nome='{self.ids.nome.text}';"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)
        output = c.fetchall()

        if len(output) == 0:
            popup = Popup(title='ERRO - REMOVER FORNECEDOR',
                    content=Label(text='Não foi possível remover o fornecedor.\nNão foi encontrado um fornecedor\ncom os dados informados.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.ids.cnpj.text = ''
            self.ids.nome.text = ''            
            self.parent.current = 'fornecedores'
            return                  

        sql_command = f"delete from fornecedor WHERE cnpj='{self.ids.cnpj.text}' and nome='{self.ids.nome.text}';"
        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)  
        conn.commit()
        conn.close()

        self.ids.cnpj.text = ''
        self.ids.nome.text = ''

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
        self.ids.cnpj.text = ''

        if CNPJ_FORNECEDOR == '':
            popup = Popup(title='ERRO - ATUALIZAR FORNECEDOR',
                    content=Label(text='Não foi informado o CNPJ do fornecedor.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()         
            self.parent.current = 'fornecedores'
            return 
        
        self.parent.current = 'alterar_fornecedor2'

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

    def switchVendas(self):
        self.parent.current = 'venda'


class AlterarFornecedor2(Screen):

    def switchFornecedores(self):
        self.parent.current = 'fornecedores'

    def alterar(self):

        if self.ids.cnpj.text == '' and self.ids.nome.text == '' and self.ids.rua.text == '' and self.ids.estado.text == '' and self.ids.cidade.text == '' and self.ids.cep.text == '' and self.ids.numero.text == '' and self.ids.bairro.text == '' :
            popup = Popup(title='ATUALIZAR FORNECEDOR',
                    content=Label(text='Não foi realizada nenhuma alteração\nnos dados do fornecedor.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()         
            self.parent.current = 'fornecedores'
            return 

        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        if self.ids.cnpj.text != '':
            sql_command = f"select * from fornecedor WHERE cnpj='{self.ids.cnpj.text}';"
            c.execute("SET search_path TO padaria;")
            c.execute(sql_command)
            output = c.fetchall()

            if len(output) != 0:
                popup = Popup(title='ERRO - ATUALIZAR FORNECEDOR',
                        content=Label(text='Já existe um fornecedor com\no CNPJ informado.'),
                        size_hint=(None, None),
                        size=(300, 150),
                        background ='atlas://data/images/defaulttheme/button_pressed')
                popup.open()         
                self.parent.current = 'fornecedores'
                return 

        lista_atributos = [self.ids.cnpj.text,
                        self.ids.nome.text,
                        self.ids.rua.text,
                        self.ids.estado.text,
                        self.ids.cidade.text,
                        self.ids.cep.text,
                        self.ids.numero.text,
                        self.ids.bairro.text]

        sql_command = ''
        lista_values = []

        comAlteracoes = 0
        lista_comAlteracoes = []
        aux = 0

        for atributo in lista_atributos:
            if atributo != '':
                comAlteracoes += 1
                if aux == 0:
                    lista_comAlteracoes.append("cnpj")
                    lista_values.append(atributo)

                if aux == 1:
                    lista_comAlteracoes.append("nome")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 2:
                    lista_comAlteracoes.append("rua")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 3:
                    lista_comAlteracoes.append("estado")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 4:
                    lista_comAlteracoes.append("cidade")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 5:
                    lista_comAlteracoes.append("cep")
                    lista_values.append(atributo)

                if aux == 6:
                    lista_comAlteracoes.append("numero")
                    lista_values.append(atributo)

                if aux == 7:
                    lista_comAlteracoes.append("bairro")
                    lista_values.append(f"{(atributo).lower()}")

            aux += 1

        lista_values.append(f"{CNPJ_FORNECEDOR}")


        if(comAlteracoes == 0):
            popup = Popup(title='ATUALIZAR FORNECEDOR',
                    content=Label(text='Nenhuma alteração nos dados do\nfornecedor foi feita.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'fornecedores'
            return

        sql_command = CriaQuery_UPDATE("fornecedor", lista_comAlteracoes, "cnpj")

        c.execute("SET search_path TO padaria;")
        c.execute(sql_command, tuple(lista_values))
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

    def switchVendas(self):
        self.parent.current = 'venda'
    
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

    def switchVendas(self):
        self.parent.current = 'venda'

    def cadastrar(self):

        if self.ids.nome.text == '' or self.ids.bairro.text == '' or self.ids.rua.text == '' or self.ids.cep.text == '' or self.ids.cidade.text == '' or self.ids.numero.text == '':
            popup = Popup(title='ERRO - CADASTRAR ESTABELECIMENTO',
                    content=Label(text='Alguns campos não foram preenchidos.\nPor favor, preencha todos os campos.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.ids.nome.text = ''
            self.ids.bairro.text = ''
            self.ids.rua.text = ''
            self.ids.cep.text = ''
            self.ids.cidade.text = ''
            self.ids.numero.text = '' 
            self.parent.current = 'estabelecimento'
            return 

        conn = ConnectionDatabase.getConnection()  
        c = conn.cursor()

        # Add dados na tabela de estabelecimento
        sql_command = "INSERT INTO estabelecimento (nome, bairro, rua, cep, cidade, numero) VALUES(%s, %s, %s, %s,%s,%s)"
        values = (self.ids.nome.text,
                  self.ids.bairro.text,
                  self.ids.rua.text,
                  self.ids.cep.text,
                  self.ids.cidade.text,
                  self.ids.numero.text)

        c.execute("SET search_path TO padaria;")
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

        if COD_ESTABELECIMENTO == '':
            popup = Popup(title='ERRO - ALTERAR ESTABELECIMENTO',
                    content=Label(text='Não foi possível realizar a alteração.\nNão foi informado o código do es-\ntabelecimento.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estabelecimento'
            return   

        self.ids.codigo.text = ''
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

    def switchVendas(self):
        self.parent.current = 'venda'


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

    def switchVendas(self):
        self.parent.current = 'venda'

    def alterar(self):

        if self.ids.nome.text == '' and self.ids.bairro.text == '' and self.ids.rua.text == '' and self.ids.cep.text == '' and self.ids.cidade.text == '' and self.ids.numero.text == '':
            popup = Popup(title='ALTERAR ESTABELECIMENTO',
                    content=Label(text='Não foi realizada nenhuma alteração\nnos dados do estabelecimento.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estabelecimento'
            return   

        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        lista_atributos = [self.ids.nome.text,
                            self.ids.bairro.text,
                            self.ids.rua.text,
                            self.ids.cep.text,
                            self.ids.cidade.text,
                            self.ids.numero.text]

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
                    lista_comAlteracoes.append("bairro")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 2:
                    lista_comAlteracoes.append("rua")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 3:
                    lista_comAlteracoes.append("cep")
                    lista_values.append(atributo)

                if aux == 4:
                    lista_comAlteracoes.append("cidade")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 5:
                    lista_comAlteracoes.append("numero")
                    lista_values.append(atributo)

            aux += 1

        lista_values.append(f"{COD_ESTABELECIMENTO}")

        if(comAlteracoes == 0):
            popup = Popup(title='ATUALIZAR DADOS DO ESTABELE-\nCIMENTO',
                    content=Label(text='Nenhuma alteração nos dados do\nestabelecimento foi feita.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estabelecimento'
            return

        sql_command = CriaQuery_UPDATE("estabelecimento", lista_comAlteracoes, "CODIGO")

        c.execute("SET search_path TO padaria;")
        c.execute(sql_command, tuple(lista_values))

        conn.commit()
        conn.close()

        self.ids.nome.text = ''
        self.ids.bairro.text = ''
        self.ids.rua.text = ''
        self.ids.cep.text = ''
        self.ids.cidade.text = ''
        self.ids.numero.text = ''

        popup = Popup(title='ATUALIZAR DADOS DO ESTABELE-\nCIMENTO',
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

    def switchVendas(self):
        self.parent.current = 'venda'

    def switchTabela(self):
        self.parent.current = 'tabela_busca_estabelecimento'

    def buscar(self):
        global COD_ESTABELECIMENTO
        COD_ESTABELECIMENTO = self.ids.codigo.text
        global NOME_ESTABELECIMENTO
        NOME_ESTABELECIMENTO = self.ids.nome.text

        self.ids.codigo.text = ''
        self.ids.nome.text = ''


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

    def switchVendas(self):
        self.parent.current = 'venda'

    def tabela(self):

        if COD_ESTABELECIMENTO == '' and NOME_ESTABELECIMENTO == '':

            popup = Popup(title='ERRO - BUSCAR FORNECEDOR',
                    content=Label(text='Não foi possível realizar a busca.\nNenhum dado do fornecedor foi\ninformado.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estabelecimento'
            return   

        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()  

        sql_command = ''

        if COD_ESTABELECIMENTO != '' and NOME_ESTABELECIMENTO == '':
            sql_command = f"select * from estabelecimento WHERE codigo='{COD_ESTABELECIMENTO}';"

        elif COD_ESTABELECIMENTO == '' and NOME_ESTABELECIMENTO != '':
            sql_command = f"select * from estabelecimento WHERE nome='{NOME_ESTABELECIMENTO}';"

        else:
            sql_command = f"select * from estabelecimento WHERE codigo='{COD_ESTABELECIMENTO}' AND nome='{NOME_ESTABELECIMENTO}';"

        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)  
        output = c.fetchall()

        if len(output) == 0:
            popup = Popup(title='BUSCAR ESTABELECIMENTO',
                    content=Label(text='Não foi possível encontrar nenhum\nestabelecimento com os dados infor-\nmados.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'fornecedores'
            return   

        output.append(['', '', '', '', '', '' ,''])
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

    def switchVendas(self):
        self.parent.current = 'venda'

    def remover(self):

        if self.ids.codigo.text == '' or self.ids.nome.text == '':
            popup = Popup(title='ERRO - REMOVER ESTABELE-\nCIMENTO',
                    content=Label(text='Não foi possível remover o estabele-\ncimento. Alguns dados obrigatórios\nnão foram informados.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.ids.codigo.text = ''
            self.ids.nome.text = ''            
            self.ids.nome.text = 'estabelecimento'
            return        

        conn = ConnectionDatabase.getConnection()   
        c = conn.cursor()

        sql_command = f"delete from estabelecimento WHERE codigo='{self.ids.codigo.text}' and nome='{self.ids.nome.text}';"

        c.execute("SET search_path TO padaria;")
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

    def switchVendas(self):
        self.parent.current = 'venda'

    def tabela(self):
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        sql_command = f"SELECT * FROM CONTA WHERE (conta.DATA_VENCIMENTO - current_date) >= 0;"

        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)  
        output = c.fetchall()

        if len(output) == 0:
            popup = Popup(title='CONTAS ATIVAS',
                    content=Label(text='Não foi possível encontrar nenhuma\nconta ativa.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estabelecimento'
            return   

        output.append(['', '', '', '', '', '' ,''])
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

    def switchVendas(self):
        self.parent.current = 'venda'

    def tabela(self):
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        sql_command = f"SELECT * FROM CONTA WHERE (conta.DATA_VENCIMENTO - current_date) < 0;"

        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)  
        output = c.fetchall()

        if len(output) == 0:
            popup = Popup(title='CONTAS PASSADAS',
                    content=Label(text='Não foi possível encontrar nenhuma\nconta passada.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estabelecimento'
            return   

        output.append(['', '', '', '', '', '' ,''])
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

    def switchVendas(self):
        self.parent.current = 'venda'

    def remover(self):

        if self.ids.cod_barras.text == '':
            popup = Popup(title='ERRO - REMOVER CONTA',
                    content=Label(text='Não foi possível remover a conta.\nNão foi informado o códido\nde barras da conta.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.ids.cod_barras.text = ''
            self.parent.current = 'estabelecimento'
            return    

        conn = ConnectionDatabase.getConnection()    
        c = conn.cursor()

        sql_command = f"delete from conta WHERE cod_barras='{self.ids.cod_barras.text}';"

        c.execute("SET search_path TO padaria;")
        c.execute(sql_command)  
        conn.commit()
        conn.close()

        popup = Popup(title='DELETAR CONTA',
                      content=Label(text='Conta deletada com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()
        self.parent.current = 'estabelecimento'


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

    def switchVendas(self):
        self.parent.current = 'venda'

    def cadastrar(self):
        conn = ConnectionDatabase.getConnection()  
        c = conn.cursor()

        if((self.ids.pago.text).lower() == 's'): self.ids.pago.text = 'true'
        else: self.ids.pago.text = 'false'
  

        if self.ids.cod_barras.text == '' or self.ids.tipo.text == '' or self.ids.valor.text == '' or self.ids.data_vencimento.text == '' or self.ids.pago.text == '' or self.ids.codigo_estabelecimento.text == '':
            popup = Popup(title='ERRO - CADASTRAR CONTA',
                    content=Label(text='Alguns campos obrigatórios não foram\npreenchidos.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.ids.cod_barras.text = ''
            self.ids.tipo.text = ''
            self.ids.valor.text = ''
            self.ids.data_vencimento.text = ''
            self.ids.data_pagamento.text = ''
            self.ids.pago.text = ''
            self.ids.codigo_estabelecimento.text = ''
            self.parent.current = 'estabelecimento'
            return 

        sql_command = ''

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

        c.execute("SET search_path TO padaria;")
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

        self.parent.current = 'estabelecimento'


class AlterarConta(Screen):
    def recolherDados(self):    
        global COD_BARRAS
        COD_BARRAS = self.ids.cod_barras.text
        self.ids.cod_barras.text = ''

        if COD_BARRAS == '':
            popup = Popup(title='ERRO - ALTERAR CONTA',
                    content=Label(text='Não foi possível realizar a alteração.\nNão foi informado o código de\nbarras da conta.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estabelecimento'
            return 

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

    def switchVendas(self):
        self.parent.current = 'venda'


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

    def switchVendas(self):
        self.parent.current = 'venda'

    def alterar(self):

        if self.ids.cod_barras.text == '' and self.ids.tipo.text == '' and self.ids.valor.text == '' and self.ids.data_vencimento.text == '' and self.ids.pago.text == '' and self.ids.codigo_estabelecimento.text == '':
            popup = Popup(title='ALTERAR CONTA',
                    content=Label(text='Não foi realizada nenhuma\nalteração nos dados da conta.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estabelecimento'
            return 

        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()

        if((self.ids.pago.text).lower() == 's'): self.ids.pago.text = 'true'
        else: self.ids.pago.text = 'false'
  
        lista_atributos = [self.ids.cod_barras.text,
                            self.ids.tipo.text,
                            self.ids.valor.text,
                            self.ids.data_vencimento.text,
                            self.ids.data_pagamento.text,
                            self.ids.pago.text,
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
                    lista_comAlteracoes.append("cod_barras")
                    lista_values.append(atributo)

                if aux == 1:
                    lista_comAlteracoes.append("tipo")
                    lista_values.append(f"{(atributo).lower()}")

                if aux == 2:
                    lista_comAlteracoes.append("valor")
                    lista_values.append(atributo)

                if aux == 3:
                    lista_comAlteracoes.append("data_vencimento")
                    lista_values.append(f"{ConversorData(atributo, True)}")

                if aux == 4:
                    if self.ids.data_pagamento.text != '':
                        lista_comAlteracoes.append("data_pagamento")
                        lista_values.append(f"{ConversorData(atributo, True)}")

                if aux == 5:
                    lista_comAlteracoes.append("pago")
                    lista_values.append(atributo)

                if aux == 6:
                    lista_comAlteracoes.append("codigo_estabelecimento")
                    lista_values.append(atributo)

            aux += 1

        lista_values.append(f"{COD_BARRAS}")

        if(comAlteracoes == 0):
            popup = Popup(title='ATUALIZAR DADOS DA CONTA',
                    content=Label(text='Nenhuma alteração nos dados da\nconta foi feita.'),
                    size_hint=(None, None),
                    size=(300, 150),
                    background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.parent.current = 'estabelecimento'
            return

        sql_command = CriaQuery_UPDATE("conta", lista_comAlteracoes, "COD_BARRAS")

        c.execute("SET search_path TO padaria;")
        c.execute(sql_command, tuple(lista_values))

        conn.commit()
        conn.close()

        popup = Popup(title='ATUALIZAR DADOS DA CONTA',
                      content=Label(text='CONTA atualizada com sucesso'),
                      size_hint=(None, None),
                      size=(300, 150),
                      background ='atlas://data/images/defaulttheme/button_pressed')
        popup.open()

        self.parent.current = 'estabelecimento'


class CompraFornecedorPage(Screen):
    def switchHome(self):
        self.parent.current = 'home'

    def switchFuncionario(self):
        self.parent.current = 'funcionario'

    def switchEstoque(self):
        self.parent.current = 'estoque'

    def switchVendas(self):
        self.parent.current = 'venda'

    def switchCadastrar(self):
        self.parent.current = 'cadastrar_compraForn'

    def switchConsultar(self):
        self.parent.current = 'consultar_compras'


class CadastrarCompraForn(Screen):
    def switchCompraForn(self):
        self.parent.current = 'compraFornecedor'

    def cadastrar(self):
        if self.ids.dt_entrega.text == '' or self.ids.fcodigo_funcionario.text == '' or self.ids.cnpj.text == '':
            popup = Popup(title='ERR0 - CADASTRAR COMPRA',
                            content=Label(text='Não foi possível realizar a\ncompra. Alguns dados obrigatórios\nnão foram preenchidos.'),
                            size_hint=(None, None),
                            size=(300, 150),
                            background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()
            self.ids.fcodigo_funcionario.text == ''
            self.ids.cnpj.text == ''
            self.ids.dt_entrega.text == ''
            self.parent.current = 'compraFornecedor'
            return

        global DT_ENTREGA
        DT_ENTREGA = ConversorData(self.ids.dt_entrega.text, True)
        global COD_FUNC
        COD_FUNC = self.ids.fcodigo_funcionario.text
        global CNPJ_FORNECEDOR
        CNPJ_FORNECEDOR = self.ids.cnpj.text

        self.ids.fcodigo_funcionario.text == ''
        self.ids.cnpj.text == ''
        self.ids.dt_entrega.text == ''

        self.parent.current = 'selecionar_produtos'


class SelecionarProdutos(Screen):
    posicaoProduto = 0

    def __init__(self, **kwargs):
        super(Screen,self).__init__(**kwargs)

    def switchCompraForn(self):
        self.parent.current = 'compraFornecedor'

    def adicionaProduto(self):

        #posicao variavel do textBox
        posicaoTextBox = 0.8 - (self.posicaoProduto/10)
        #atualizando o numero de produtos na tela
        self.posicaoProduto+=1

        #criando um textField de codigo de produto
        exec("self.produto"+ str(self.posicaoProduto) + " = MDTextField(mode='rectangle')")
        exec("self.produto"+ str(self.posicaoProduto) + ".hint_text = 'Cod. Barras do produto "+ str(self.posicaoProduto) + "'")
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


    def valida_produtos(self):
                    
        somatorio = 0

        #resetando o exibidor do somatorio
        self.ids.valor_total.text = "------------------------------------"

        if self.posicaoProduto == 0:
             self.ids.lbl_error.text = "Insira ao menos um produto na compra"
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


    def registrar_compra(self):

        if self.valida_produtos():
            #armazenando valores em variaves locais
            valor_total = str(self.ids.valor_total.text).replace(",", ".").replace("R$ ", "")

            #inserindo compra
            conn2 = ConnectionDatabase.getConnection()
            c2 = conn2.cursor()
            c2.execute("SET search_path TO padaria;")
            c2.execute(f"insert into compra (DT_SOLICITACAO, DT_ENTREGA, VALOR_TOTAL, FCODIGO_FUNCIONARIO, CNPJ) VALUES(current_date, '{DT_ENTREGA}', {valor_total}, '{COD_FUNC}', '{CNPJ_FORNECEDOR}')")
            c2.execute(f"(select cod_compra from compra where valor_total={valor_total}) order by dt_solicitacao desc limit 1")
            conn2.commit()
            output = c2.fetchall()
            conn2.close()
            
            #armazenando cod_compra gerado
            for row in output:
                cod_compra = row[0]
                        
            #buscando produtos comprados
            for numProduto in range(1, self.posicaoProduto+1):
                #armazenando o codigo do produto 
                codigoProduto = eval("self.produto" + str(numProduto) + ".text")
                #armazenando a quantidade solicitada do produto            
                qtdProduto = int(eval("self.quantidadeProduto" + str(numProduto) + ".text"))
                
                #inserindo produto e sua quantidade na tabela produto_comprado
                conn3 = ConnectionDatabase.getConnection()
                c3 = conn3.cursor()
                c3.execute("SET search_path TO padaria;")
                c3.execute(f"insert into produto_comprado (QUANTIDADE, COD_COMPRA, COD_BARRAS) " +
                            f"values ({qtdProduto}, {cod_compra}, {codigoProduto})")

                # aumenta a quantidade do produto no estoque
                c3.execute(f"update produto set qtd_estoque = " +
                            f"((select qtd_estoque from produto where cod_barras = '{codigoProduto}') + {qtdProduto}) " +
                            f"where cod_barras = '{codigoProduto}'")
                conn3.commit()
                conn3.close()

            popup = Popup(title='COMPRA COM FORNECEDOR',
            content=Label(text='Compra realizada com sucesso'),
            size_hint=(None, None),
            size=(300, 150),
            background ='atlas://data/images/defaulttheme/button_pressed')
            popup.open()

            self.parent.current = 'compraFornecedor'


class ConsultarCompras(Screen):

    def switchCompras(self):
        self.parent.current = 'compraFornecedor'

    def __init__(self, **kwargs):
        super(Screen,self).__init__(**kwargs)
        global AUX
        if AUX == 0: AUX += 1
        else: self.criaTabela()

    def criaTabela(self):
        #iniciando conexao, criando o cursor
        conn = ConnectionDatabase.getConnection()
        c = conn.cursor()
    
        c.execute("SET search_path TO padaria;")
        string_busca = "select * from compra"
        c.execute(string_busca)
        output = c.fetchall()

        self.table = MDDataTable(
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(0.9, 0.6),
            use_pagination=True,
            column_data=[
                ("Cod. compra", dp(25)),
                ("Data da compra", dp(40)),
                ("Data da entrega", dp(40)),
                ("Valor total", dp(30)),
                ("Cod. adm", dp(25)),
                ("CNPJ do fornecedor", dp(30))
            ],
            sorted_on="Data da compra",
            sorted_order="DSC",
            elevation=2,
            row_data=output
        )

        #inserindo tabela na tela
        self.add_widget(self.table) 



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


# postgres == True: Converte 'dd-mm-aaaa' para 'aaaa-mm-dd' (padrao do Postgresql)
# postgres == False: Converte 'aaaa-mm-dd' para 'dd-mm-aaaa' (mostrar para o usuario)
def ConversorData(dataDesformatada, postgres):
    data = str(dataDesformatada)
    if data == '' or data == 'None': return data
    if bool(postgres): return str(data[len(data)-4:len(data)] + '-' + data[3:5] + '-' + data[0:2])
    return str(data[len(data)-2:len(data)] + '-' + data[5:7] + '-' + data[0:4])


# Troca o caracter ',' por '.' (padrao do Postgresql)
def FormataFloat(num):
    numFormatado = num
    if ',' in num:
        numFormatado = numFormatado.replace(',', '.') 
    return numFormatado


def FormataHora(horario):
    return horario + ':00.00'


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
sm.add_widget(CompraFornecedorPage(name='compraFornecedor'))
sm.add_widget(CadastrarCompraForn(name='cadastrar_compraForn'))
sm.add_widget(SelecionarProdutos(name='selecionar_produtos'))
sm.add_widget(ConsultarCompras(name='consultar_compras'))
sm.add_widget(HistoricoTrabalhoPage(name='historicoTrabalho'))
sm.add_widget(RegistrarHorario(name='registrarHorario'))
sm.add_widget(ConsultarHistorico(name='consultarHistorico'))
sm.add_widget(TabelaHistoricoTrabalho(name='tabela_historicoTrabalho'))


class Main(MDApp):
    def build(self):
        
        ####################
        ###EXEMPLO DE USO###
        ####################

        ##conn = ConnectionDatabase.getConnection()
        ##c = conn.cursor()
        ##conn.close()

        self.theme_cls.primary_palette = "DeepOrange"
        
        return Builder.load_string(KV)


Main().run()
