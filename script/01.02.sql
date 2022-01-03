CREATE SCHEMA PADARIA AUTHORIZATION POSTGRES;
SET search_path TO PADARIA;

----------------------------------------------------------------
------------------------CREATE TABLE----------------------------
----------------------------------------------------------------

CREATE TABLE ESTABELECIMENTO (
    CODIGO INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    NOME VARCHAR(70) NOT NULL,
    BAIRRO VARCHAR(100),
    RUA VARCHAR(100),
    CEP CHAR(8),
    CIDADE VARCHAR(100),
    NUMERO VARCHAR(10),
    PRIMARY KEY(CODIGO)
);

CREATE TABLE FORNECEDOR (
    CNPJ CHAR (14) NOT NULL,
    NOME VARCHAR (70) NOT NULL,
    RUA VARCHAR(100) NOT NULL,
    ESTADO VARCHAR(30) NOT NULL,
    CIDADE VARCHAR(100) NOT NULL,
    CEP CHAR(8),
    NUMERO VARCHAR(10),
    BAIRRO VARCHAR(100),
    PRIMARY KEY (CNPJ)
);

CREATE TABLE CLIENTE (
    NOME VARCHAR(70) NULL,
    CPF CHAR(11) NOT NULL,
    DATANASC DATE,
    PRIMARY KEY(CPF)
);

CREATE TABLE PRODUTO (
    COD_BARRAS CHAR(15) NOT NULL,
    NOME VARCHAR(50) NOT NULL,
    NOME_FABRICANTE VARCHAR(100) NOT NULL,
    PRECO DECIMAL(18,2) NOT NULL,
    DATA_FABRICACAO DATE NOT NULL,
    CATEGORIA VARCHAR(50) NOT NULL,
    QTD_ESTOQUE INT NOT NULL,
    DATA_VENCIMENTO DATE NOT NULL,
    PRIMARY KEY (COD_BARRAS)
);

CREATE TABLE CONTA (
    COD_BARRAS CHAR(48) NOT NULL,
    TIPO CHAR(35) NOT NULL,
    VALOR DECIMAL (10,2) NOT NULL,
    DATA_VENCIMENTO DATE NOT NULL,
    DATA_PAGAMENTO DATE NULL,
    PAGO BOOLEAN,
    CODIGO_ESTABELECIMENTO INT NOT NULL,
    PRIMARY KEY(COD_BARRAS),
    FOREIGN KEY(CODIGO_ESTABELECIMENTO) REFERENCES
    ESTABELECIMENTO(CODIGO)
);

CREATE TABLE FUNCIONARIO (
    CODIGO_FUNC INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    NOME VARCHAR(70) NOT NULL,
    CPF CHAR(11) NOT NULL,
    SALARIO DECIMAL (10,2),
    FERIAS DATE,
    CODIGO_ESTABELECIMENTO INT NOT NULL,
    SENHA VARCHAR(50) NOT NULL,
    PRIMARY KEY(CODIGO_FUNC),
    FOREIGN KEY (CODIGO_ESTABELECIMENTO) REFERENCES
    ESTABELECIMENTO(CODIGO) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE HISTORICO_TRABALHO (
    DATA_REGISTRO DATE NOT NULL,
    HORA_ENTRADA_R TIME NOT NULL,
    HORA_SAIDA_R TIME NOT NULL,
    FCODIGO_FUNCIONARIO INT NOT NULL,
    PRIMARY KEY(DATA_REGISTRO, HORA_ENTRADA_R, HORA_SAIDA_R,
    FCODIGO_FUNCIONARIO),
    FOREIGN KEY(FCODIGO_FUNCIONARIO) REFERENCES
    FUNCIONARIO(CODIGO_FUNC) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE ADMINISTRADOR (
    FCODIGO_FUNCIONARIO INT NOT NULL,
    ESPECIALIDADE VARCHAR(30) NOT NULL,
    PRIMARY KEY(FCODIGO_FUNCIONARIO),
    FOREIGN KEY(FCODIGO_FUNCIONARIO) REFERENCES
    FUNCIONARIO(CODIGO_FUNC) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE ATENDENTE_CAIXA (
    FCODIGO_FUNCIONARIO INT NOT NULL,
    NIVEL_ESCOLARIDADE VARCHAR(30) NOT NULL,
    PRIMARY KEY(FCODIGO_FUNCIONARIO),
    FOREIGN KEY(FCODIGO_FUNCIONARIO) REFERENCES
    FUNCIONARIO(CODIGO_FUNC) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE TELEFONE_CONTATO (
    TELEFONE VARCHAR (14) NOT NULL,
    TCODIGO CHAR(14) NOT NULL,
    PRIMARY KEY (TELEFONE),
    FOREIGN KEY(TCODIGO) REFERENCES FORNECEDOR(CNPJ) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE VENDE (
    COD_VENDA INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    DT_VENDA TIMESTAMP NOT NULL,
    VALOR_TOTAL DECIMAL(18,2) NOT NULL,
    FCODIGO_FUNCIONARIO INT NOT NULL,
    CPF CHAR(11) NOT NULL,
    PRIMARY KEY (COD_VENDA),
    FOREIGN KEY (CPF ) REFERENCES CLIENTE(CPF),
    FOREIGN KEY (FCODIGO_FUNCIONARIO) REFERENCES
    ATENDENTE_CAIXA(FCODIGO_FUNCIONARIO)
);

CREATE TABLE PRODUTO_VENDIDO (
    COD_PRODUTO_VENDIDO INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    QUANTIDADE INT NOT NULL,
    COD_VENDA INT NOT NULL,
    COD_BARRAS CHAR(15) NOT NULL,
    PRIMARY KEY (COD_PRODUTO_VENDIDO),
    FOREIGN KEY (COD_VENDA ) REFERENCES VENDE(COD_VENDA),
    FOREIGN KEY (COD_BARRAS) REFERENCES PRODUTO(COD_BARRAS) ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE COMPRA(
    COD_COMPRA INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    DT_SOLICITACAO TIMESTAMP NOT NULL,
    DT_ENTREGA TIMESTAMP NOT NULL,
    VALOR_TOTAL DECIMAL(18,2) NOT NULL,
    FCODIGO_FUNCIONARIO INT NOT NULL,
    CNPJ CHAR (14) NOT NULL,
    PRIMARY KEY (COD_COMPRA),
    FOREIGN KEY (FCODIGO_FUNCIONARIO ) REFERENCES
    ADMINISTRADOR(FCODIGO_FUNCIONARIO) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (CNPJ) REFERENCES FORNECEDOR(CNPJ)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE PRODUTO_COMPRADO (
    COD_PRODUTO_COMPRADO INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    QUANTIDADE INT NOT NULL,
    COD_COMPRA INT NOT NULL,
    COD_BARRAS CHAR(15) NOT NULL,
    PRIMARY KEY (COD_PRODUTO_COMPRADO ),
    FOREIGN KEY (COD_COMPRA ) REFERENCES COMPRA(COD_COMPRA ) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (COD_BARRAS) REFERENCES PRODUTO(COD_BARRAS) ON DELETE CASCADE ON UPDATE CASCADE);

----------------------------------------------------------------
---------------------------INSERTS------------------------------
----------------------------------------------------------------

INSERT INTO ESTABELECIMENTO(nome, rua, numero, bairro, cep, cidade)
VALUES
('panificadora alfa','rua projetada', '553', 'ouro verde','78135616','várzea grande'),
('padaria seu nelson','rua legal', '583', 'longe','25716080','petrópolis'),
('padaria da melissaa','rua jose mendes', '593', 'atibaia','71927180','brasília'),
('panificadora theo','rua zona leste', '123', 'guarulhos','61900630','maracanaú'),
('panificadora silas','rua praia', '1553', 'santos ','49020190','aracaju'),
('panificadora will','rua dormindo demais', '1234', 'saúde','70723040','brasília'),
('padaria patricia','rua nota alta', '1234', 'felicidade','87308270','campo mourão'),
('panificadora josefa','rua scooby doo', '553', 'ouro','68902080','macapá'),
('panificadora joao','rua mario', '553', 'taboão','54270100','jaboatão dos
guararapes'),
('panificadora catarina','rua projeta', '553', 'são francisco','26277301','nova
iguaçu'),
('panificadora edu','rua giulia', '1553', 'longe demais','77064014','palmas'),
('panificadora murilo','rua marcado', '5553', 'são carlos','74970410','aparecida de
goiânia'),
('panificadora espirro','rua felicidade', '4553', 'embu das
artes','71551204','brasília'),
('padaria caetano','rua dos bobos', '0', 'lugar nenhum','60830465','fortaleza'),
('panificadora penha','rua salgada', '5353', 'jardim salete','76964107','cacoal'),
('panificadora chique','avenida faria lima', '553', 'pinheiros','69309400','boa vista'),
('panificadora cult','rua gamer', '4553', 'pirajussara','64051140','teresina'),
('panificadora estudante','rua projetada', '553', 'ouro verde','93525240','novo
hamburgo'),
('panificadora quente','rua xuxa', '553', 'acre','65081622','são luís'),
('panificadora mickey','rua disney', '77', 'rondônia','69089071','manaus');

INSERT INTO FORNECEDOR (cnpj, nome, rua, estado, cidade, cep, numero, bairro)
VALUES
('12345123000122', 'teresinha e tereza filmagens me', 'avenida andrade','são paulo', 'são
paulo', '18053060', '609', 'vila bancário'),
('32124222000165', 'alexandre e isabella ferragens ltda', 'rua caracol','são paulo',
'valinhos', '12916361', '933', 'são benedito (jordanésia)'),
('98847625000198', 'lívia e lúcia marcenaria me', 'rua das rosas','praça interact club',
'são paulo', '12705120', '762', 'vila ema'),
('79123543000212', 'carlos e manoel buffet ltda', 'rua santos severo scapol','são paulo',
'marília', '12237530', '104', 'vila rezende'),
('73243857000232', 'ester e vicente telecomunicações me', 'rua thomaz bérgamo','são
paulo', 'jaú', '12232879', '740', 'jardim dermínio'),
('10345897000134', 'thales e bryan lavanderia me', 'rua paschoal carlos magno','são
paulo', 'brás', '13189212', '919', 'jardim maria estela'),
('17736837000177', 'kaique e renato entulhos ltda', 'rua pedro fernandes de souza','são
paulo', 'são vicente', '02937080', '732', 'jardim miragaia'),
('11938223000144', 'jaqueline e teresinha adega me', 'rua engenheiro elias machado de
almeida','são paulo', 'bragança paulista', '15816060', '290', 'perdizes'),
('20738234000167', 'anthony e fabiana buffet ltda', 'rua parnamirim','rio de janeiro',
'valinhos', '16022620', '752', 'vila mamedina'),
('59343746000174', 'diego e rosângela eletrônica me', 'rua valentina de siqueira
cardoso','são paulo', 'campinas', '04719050', '596', 'vila romana'),
('30213837000226', 'murilo e joão esportes me', 'rua gérson marques da silva','são
paulo', 'itapecerica da serra', '12302050', '596', 'vila santa izabel'),
('90287324000100', 'lorenzo e luiza fotografias me', 'rua benedito bernardes de
brito','são paulo', 'barretos', '18706705', '321', 'baeta neves'),
('18837716000187', 'rosa e ruan assessoria jurídica me', 'travessa martin faber','são
paulo', 'são paulo', '06870160', '308', 'núcleo bartholomeu bueno de miranda'),
('98289111000111', 'carlos e thales ferragens ltda', 'rua jorge americano 380','santa
catarina', 'são josé do rio preto', '15048090', '786', 'conjunto habitacional doutor josé
secchi'),
('10987987000177', 'thiago e marcos vinicius adega ltda', 'rua salvador do sul','são
paulo', 'campinas', '12092763', '903', 'loteamento nova espírito santo'),
('33872982010177', 'rosa e mário marcenaria me', 'rua bolívia','são paulo', 'diadema',
'16204395', '673', 'vila angelo vial'),
('12333334000188', 'henry e márcia marcenaria ltda', 'rua morro agudo','são paulo', 'são
bernardo do campo', '06709470', '377', 'piratininga'),
('91900903000277', 'liz e isaac buffet ltda', 'avenida hans stadem','são paulo', 'franca',
'05159160', '601', 'loteamento loanda'),
('88223555000144', 'igor e carolina telas me', 'rua aureliano alves genuíno','são paulo',
'são josé dos campos', '07223235', '476', 'cidade morumbi'),
('47222666000176', 'ayla e vitor gráfica ltda', 'rua antonieta de marco','são paulo',
'sorocaba', '13331674', '994', 'chácara são luiz');

INSERT INTO CLIENTE (NOME, CPF, DATANASC)
VALUES
('giovanni matheus leandro silva', '22469763088', '2001-03-19'),
('giovanni matheus leandro silva', '92965266046', '2004-03-02'),
('thomas césar cláudio da cunha', '23333396084', '2003-01-04'),
('samuel juan santos', '51247966003', '1988-08-25'),
('bárbara lavínia santos', '10214031055', '1946-03-26'),
('patrícia francisca da paz', '97853491956', '1995-08-13'),
('arthur augusto renato brito','78896957990','1988-10-12'),
('rosângela giovana da cunha','70628971087','1999-12-17'),
('juan mário victor silva','66978464376','1982-02-08'),
('sebastião lorenzo rocha','18579663849','1942-10-07'),
('marina olivia joana da mota','81940392667','1969-09-26'),
('fátima lavínia lima','91689441011','1958-11-06'),
('isabela lívia vanessa figueiredo','60367866382','1963-07-14'),
('juliana maria pires','66643517303','1961-06-03'),
('marcelo iago sebastião rodrigues','65153214492','1941-05-15'),
('clara luiza kamilly souza','89759133172','1956-02-18'),
('daniel isaac pietro porto','73509000153','1959-04-02'),
('yago isaac arthur alves','98367827249','1989-04-11'),
('danilo osvaldo manuel mendes','7841437370','1946-12-01'),
('eduarda clarice da cruz','19275326800','1988-03-02'),
('elaine vera aragão','79461912005','1979-03-11'),
('stefany elza antonella da luz','08177733660','1965-10-23'),
('aline sandra fernandes','65853503596','1946-12-09'),
('geraldo cauã da cunha','92842487109','1941-06-15'),
('ruan gabriel danilo rodrigues','66796028740','1970-12-07');

INSERT INTO PRODUTO (COD_BARRAS, NOME, NOME_FABRICANTE, PRECO,
DATA_FABRICACAO, CATEGORIA, QTD_ESTOQUE, DATA_VENCIMENTO)
VALUES
('189181891891896','pão de mel','indústrias de
melaço',12.25,'2020-01-02','doces',5,'2020-02-02'),
('189189132178765','pão de queijo','pães
mineiros',5.12,'2020-06-05','pães',7,'2021-01-01'),
('654651864869153','pão
francês','caseiros',0.25,'2020-10-15','pães',2,'2020-10-16'),
('317815317621347','coxinha','salgados do seu
jorge',4.50,'2019-05-12','salgados',1,'2021-08-12'),
('651531715632173','mistinho','salgados do seu
jorge',8.99,'2019-05-12','salgados',4,'2021-09-11'),
('751896317781376','maravilha','salgados do seu
jorge',3.23,'2019-05-12','salgados',1,'2021-07-22'),
('165156105054176','detergente','vanish',15.99,'2019-05-12','limpeza',6,'2020-01-01'),
('465438413845631','rodo','madeira e
madeira',25.50,'2021-05-05','limpeza',4,'2021-07-07'),
('646218317495131','pano de chão','madeira e
madeira',4.99,'2021-01-10','limpeza',11,'2021-10-15'),
('786484312384954','geladinha','dr. oetker',1.00,'2020-12-21','produto
alimentício',15,'2021-12-21'),
('648796521560431','bolinho','ana maria',4.99,'2021-01-01','comida',7,'2021-07-12'),
('645987321004164','geleia','linea',7.95,'2020-01-15','comida',8,'2021-07-12'),
('613176498423184','queijo','seara',8.99,'2021-11-12','frios',1,'2021-12-12'),
('615817631798456','mussarela','sadia',9.99,'2021-02-05','frios',6,'2021-05-31'),
('561798435121864','presunto','seara',15.05,'2020-12-15','frios',3,'2021-01-05'),
('465423171315621','mortadela','sadia',20.00,'2020-07-25','frios',6,'2021-03-12'),
('861351761231764','queijinho','polenguinho',55.20,'2021-01-02','frios',5,'2021-02-01'),
('645616245754712','ovo de chocolate','kinder
ovo',12.20,'2019-06-22','sobremesa',5,'2022-06-12'),
('618917416617912','margarina','qualy',12.55,'2018-05-16','laticínios',6,'2021-08-26'),
('168165315615189','manteiga','qualy',13.50,'2017-07-15','laticínios',9,'2020-09-08'),
('165123184891231','pão integral','puma',8.00,'2020-08-12','pães',4,'2021-10-10'),
('684653176513548','pão de forma','puma',9.50,'2020-09-12','pães',6,'2022-04-17'),
('984617906506885','requeijão','catupiry',14.55,'2021-07-16','laticínios',8,'2022-09-14'),
('561749805161208','catupiry','catupiry',18.60,'2021-09-23','laticínios',9,'2022-07-16'),
('654894231050407','chinelo','havaianas',25.00,'2020-03-03','vestimentas',1,'2025-03-03'),
('891984792130510','suco laranja','tang',4.99,'2021-01-15','bebida',6,'2022-06-18'),
('165105608792068','suco uva','tang',4.99,'2021-01-15','bebida',7,'2022-06-18'),
('941651030684943','suco
morango','tang',4.99,'2021-01-15','bebida',8,'2022-06-18'),
('651891716305605','suco abacaxi','tang',4.99,'2021-01-15','bebida',2,'2022-06-18'),
('651981719861056','suco limão','tang',4.99,'2021-01-15','bebida',16,'2022-06-18');

INSERT INTO CONTA (COD_BARRAS, TIPO, VALOR, DATA_VENCIMENTO,
DATA_PAGAMENTO, PAGO, codigo_estabelecimento) VALUES
(123456789012345678904321987162739487654319023234,'conta de luz do mes de
janeiro' , 74.38,'2021-02-05', '2021-02-01', true,1),
(987162739487654319023234123487689012345678904321, 'conta de agua do mes de
marco', 70.21,'2021-05-21', '2021-04-12', true,1),
(123487689012345678904321982134657890123456729875, 'conserto da pia do banheiro',
53.00, '2021-11-01', null, false,1),
(821346578901234567298765123487689012345678904321, 'itens de decoracao',
121.21,'2021-10-01', null, false,1),
(000487689012345678904321000000001119287653981432, 'supermercado convem',
143.92, '2021-02-12', '2021-02-11', true,2),
(000000001119287653981432123487689000018978904321, 'itens de cozinha',
219.12,'2021-04-06', '2021-03-28', true,2),
(101010101010101010101010999987689012345678904321, 'produtos de limpeza', 85.34,
'2021-08-04', null, false,2),
(123487689012345678904321101010101010101010101010, 'fornecedor sr joao carvalho',
183.21, '2021-09-12', null, false,2),
(999987689012345678904321123487689012345678904321, 'aluguel do mes de fevereiro',
3500.00, '2021-03-01', '2021-01-28', true,3),
(123487689012345678904321888888888822222222224563, 'aluguel do mes de marco',
3500.00, '2021-04-01', '2021-03-24', true,3),
(888888888822222222224563123487689012345678904321, 'conta de luz do mes de abril',
82.12, '2021-03-06', '2021-03-02', true,3),
(555555589012345678904321858585858585858585858585, 'conta de agua do mes de
junho', 62.54, '2021-07-01', '2021-06-23', true,3),
(123487689012345678904321555555589012345678904321, 'supermercado champ',
301.65, '2021-11-01', null, false,4),
(858585858585858585858585123487689012345678904321, 'produtos de limpeza', 54.21,
'2021-10-01', '2021-09-21', true,4),
(123487689012345678904321123487689000000078904321, 'aluguel do mes de junho',
3510.00, '2021-07-03', '2021-06-25', true,4),
(666687689000000078904321222222222212345678904321, 'supermercado convem',
128.25, '2021-11-10', null, false,4),
(767676689012345678904321767676689012345678904321, 'fornecedora srta marilia
barros', 129.65,'2021-11-10', null, false,5),
(123487689012345678904321767676689012345678904321, 'conta de luz do mes de
outubro', 70.21, '2021-10-28', '2021-10-24', true,5),
(123487689033333378904321123487689033333378902222, 'aluguel do mes de outubro',
3510.00, '2021-11-02', null, false,5),
(123487689000000078904321666687689000000078904321, 'fornecedor sr joao carvalho',
121.45, '2021-09-09', '2021-09-02', true,5),
(222222222212345678904321222222222212345678904321, 'fornecedor quitanda sol
nascente', 134.21, '2021-05-23', '2021-05-12', true,6);

INSERT INTO FUNCIONARIO (NOME, CPF, SALARIO, FERIAS, codigo_estabelecimento, SENHA)
VALUES
('maria eduarda', '23456712356', 3000, null, 1, '123321'),
('mario santos', '44454798012', 2500, '2021-02-10',1, '123321'),
('iam silveira','10104387828', 3000, '2021-10-21',1, '123321'),
('lais silva', '20084521388', 5000, null,1, '123321'),
('rodrigo camara', '30299902019', 2500, '2021-03-02',2, '123321'),
('benedita magalhaes','48291028371', 3200, '2021-01-20',2, '123321'),
('martin coelho', '12323458653', 2800.80, null,2, '123321'),
('jade ponte', '20981726367', 2830, null,2,'123321'),
('gloria bernardes', '18726354663', 3200, '2021-05-23',3, '123321'),
('eliseu bastos', '20010239888', 2700, '2021-07-11',3, '123321'),
('gilberto lara', '11122233392', 2300, '2020-07-02',3, '123321'),
('caleb boaventura', '33183723212', 2500, '2020-05-21',3, '123321'),
('ryan tuna', '19329387172', 2500, null,4, '123321'),
('evelyn braganca', '34521000002', 3200, '2020-04-19',4, '123321'),
('ciara felix', '12674325678', 3100, null,4, '123321'),
('gabriela marques', '19827183215', 2500, null,5, '123321'),
('giovanni castelo','19200235891', 5200, null,5, '123321'),
('luiz abranches', '19287369100', 4200, null,5, '123321'),
('rodolfo amorin', '80291222281', 4100, null,6, '123321'),
('bianca santana', '92012332212', 2500, null,6, '123321'),
('sebastião felipe da mata', '04732289126', 1200,'2020-12-12',7, '123321'),
('roberto vitor silveira', '73510771931',2410,'2020-05-07',7, '123321'),
('vitória francisca da cunha', '96235126603',2550,null,7, '123321'),
('luiza sebastiana sarah cavalcanti', '80382414799',5660,null,7, '123321'),
('lucas iago thiago de paula', '73302515502',2500,null,8, '123321'),
('clara bárbara da luz', '14592011830',1200,'2019-08-12',8, '123321'),
('isabelly elaine tânia rodrigues', '98482060864',1750,'2018-06-12',8, '123321'),
('luzia maya jennifer lima', '17293420943',1960,'2019-06-02',9, '123321'),
('emanuelly camila barros', '67937562145',2250,null,9, '123321'),
('josé diego fogaça', '62808743033',3550,null,9, '123321'),
('isabelly aurora milena campos', '40656407093',1880,null,10, '123321'),
('laura bárbara alice corte real', '66554096329',1990,null,10, '123321'),
('luzia sarah da luz', '51405973811',2660,'2020-05-05',10, '123321'),
('alice pietra jaqueline moraes', '83600719424',2700,null,11, '123321'),
('renato jorge rafael pires', '19542274505',2900,null,11, '123321'),
('severino césar luiz monteiro', '49042543256',2800,'2021-01-05',11, '123321'),
('matheus lucas ribeiro', '29846269820',2700,null,11, '123321'),
('nathan victor barbosa', '53731151421',2900,'2019-09-13',12, '123321'),
('julia raimunda figueiredo', '94789134504',2650,null,12, '123321'),
('flávia alessandra catarina freitas', '11890984078',2300,null,13, '123321'),
('carolina ana letícia pires', '04417662428',2200,'2021-04-03',13, '123321'),
('noah davi da mota', '56321800341',2000,'2020-12-24',13, '123321'),
('aparecida marcela castro', '41003771343',3700,'2021-06-18',14, '123321'),
('luana helena gabriela nogueira', '34844539078',4200,null,14, '123321'),
('tiago renan melo', '08166327660',2300,null,14, '123321'),
('elaine aparecida rezende', '38354689360',1750,null,15, '123321'),
('rayssa kamilly priscila da paz', '41435182103',1900,'2021-04-05',15, '123321'),
('anthony noah campos', '88337111020',2300,'2021-04-06',15, '123321'),
('eloá gabriela evelyn lopes', '50605512108',2350,'2020-04-04',16, '123321'),
('elza flávia giovana aparício', '85858226191',2600,'2020-12-12',16, '123321'),
('bernardo alexandre corte real', '39046379086',2200,null,16, '123321'),
('fabiana andreia jesus', '90667847685',2650,null,17, '123321'),
('joana rosângela aparício', '73272955267',1750,null,17, '123321'),
('erick augusto juan da paz', '26456643180',6190,null,18, '123321'),
('carla marlene bianca almeida', '84484673703',5500,'2020-01-06',18, '123321'),
('rayssa alice fabiana assis', '29720861207',2660,'2021-06-04',19, '123321'),
('victor theo bernardes', '69102534770',2400,null,19, '123321'),
('bernardo otávio novaes', '88394941206',3200,null,19, '123321'),
('thiago murilo thales da paz', '63046268866',2000,'2017-02-28',20, '123321'),
('renata analu luna campos', '82047533147',2600,null,20, '123321');

INSERT INTO HISTORICO_TRABALHO (DATA_REGISTRO, HORA_ENTRADA_R,
HORA_SAIDA_R, FCODIGO_FUNCIONARIO)
VALUES
('2021-06-01', '07:30:00.00', '15:00:00.00', 1),
('2021-10-21', '08:00:10.00', '18:32:00.00', 5),
('2021-03-11', '09:10:10.00', '20:11:30.00', 10),
('2021-03-11', '07:43:00.00', '20:20:40.00', 12),
('2021-06-01', '07:20:00.00', '16:21:00.00', 4),
('2021-04-21', '07:00:40.00', '15:41:00.00', 16),
('2021-09-30', '07:22:00.00', '18:00:31.00', 20),
('2021-01-07', '08:20:00.00', '18:11:00.00', 2),
('2021-03-12', '08:22:00.00', '19:33:00.00', 20),
('2021-02-21', '09:30:32.00', '20:38:05.00', 1),
('2021-02-21', '12:00:00.00', '17:31:00.00', 3),
('2021-07-04', '07:46:00.00', '17:55:00.00', 12),
('2021-02-01', '08:42:00.00', '19:31:00.00', 3),
('2021-02-01', '08:43:00.00', '20:02:00.00', 11),
('2021-03-12', '09:12:12.00', '17:02:03.00', 15),
('2021-01-18', '05:11:00.00', '17:03:12.00', 1),
('2021-06-09', '05:04:00.00', '18:22:00.00', 13),
('2021-03-12', '05:01:00.00', '19:26:45.00', 6),
('2021-07-22', '06:20:11.00', '16:28:56.00', 7),
('2021-07-25', '06:20:11.00', '16:28:56.00', 11),
('2021-07-21', '06:20:11.00', '16:28:56.00', 19),
('2021-07-12', '06:20:11.00', '16:28:56.00', 7),
('2021-08-21', '06:20:00.00', '16:41:00.00', 8);

INSERT INTO ADMINISTRADOR (FCODIGO_FUNCIONARIO, ESPECIALIDADE)
VALUES
(3, 'gestão de pessoas'),
(5, 'gestão logística'),
(9, 'rh'),
(20,'administração'),
(25,'gestão de pessoas'),
(30,'rh'),
(35,'gestão de pessoas'),
(40,'gestão logística'),
(45,'phd de processos'),
(50,'rh'),
(55,'marketing'),
(60,'administração de empresas'),
(21,'gestão de processos'),
(26,'gestão de pessoas'),
(31,'marketing'),
(36,'gestão de leads'),
(41,'economia'),
(46,'gestão logística'),
(51,'marketing'),
(56,'gestão de processos');

INSERT INTO ATENDENTE_CAIXA (FCODIGO_FUNCIONARIO,
NIVEL_ESCOLARIDADE)
VALUES
(1, 'médio completo'),
(10, 'superior completo'),
(12, 'superior incompleto'),
(15, 'médio incompleto'),
(13, 'superior incompleto'),
(22, 'fundamental completo'),
(27, 'fundamental incompleto'),
(32, 'médio completo'),
(37, 'superior completo'),
(42, 'superior completo'),
(47, 'superior completo'),
(52, 'superior incompleto'),
(57, 'médio completo'),
(23, 'superior incompleto'),
(28, 'médio incompleto'),
(33, 'médio completo'),
(38, 'fundamental incompleto'),
(43, 'fundamental incompleto'),
(48, 'médio completo'),
(53, 'médio completo');

INSERT INTO TELEFONE_CONTATO(TELEFONE, TCODIGO)
VALUES
('4727382935','20738234000167'),
('9827170745','88223555000144'),
('6928664716','98847625000198'),
('69982557436','17736837000177'),
('85988893540','12333334000188'),
('8526272042','18837716000187'),
('8338596547','12345123000122'),
('83988744881','90287324000100'),
('21981858971','17736837000177'),
('2126440251','79123543000212'),
('8229642570','18837716000187'),
('82982466183','33872982010177'),
('8435684168','20738234000167'),
('84994102440','98847625000198'),
('21981835071','88223555000144'),
('2127524743','98289111000111'),
('4727966814','18837716000187'),
('47986356132','17736837000177'),
('6125565539','91900903000277'),
('61994405764','47222666000176');

INSERT INTO VENDE (DT_VENDA, VALOR_TOTAL, FCODIGO_FUNCIONARIO, CPF)
VALUES
('2021-06-22 19:10:25', 13.40, 1, '22469763088'),
('2021-08-21 09:10:25', 20.10, 10, '23333396084'),
('2021-10-12 09:10:25', 8.00, 13, '70628971087'),
('2021-06-02 07:10:25', 19.15, 10, '66978464376'),
('2021-11-03 07:10:25', 25.10, 22, '91689441011'),
('2021-02-05 18:10:25', 7.40, 22, '98367827249'),
('2021-02-24 18:10:25', 18.15, 22, '92965266046'),
('2021-02-24 15:10:25', 13.45, 53, '08177733660'),
('2021-06-21 14:10:25', 14.00, 15, '92842487109'),
('2021-06-21 13:10:25', 73.00, 42, '79461912005'),
('2021-06-01 12:10:25', 28.00, 47, '70628971087'),
('2021-08-19 11:10:25', 30.40, 47, '98367827249'),
('2021-08-19 08:10:25', 16.30, 12, '19275326800'),
('2021-08-28 09:10:25', 20.20, 12, '66796028740'),
('2021-07-28 09:10:25', 29.15, 22, '23333396084'),
('2021-07-28 11:10:25', 39.10, 1, '10214031055'),
('2021-07-21 10:10:25', 14.70, 1, '78896957990'),
('2021-06-15 17:10:25', 11.80, 52, '18579663849'),
('2021-06-15 16:10:25', 8.90, 32, '81940392667'),
('2021-02-01 14:10:25', 6.90, 32, '66643517303'),
('2021-02-01 13:10:25', 21.30, 52, '89759133172'),
('2021-02-01 14:10:25', 13.20, 52, '73509000153');

INSERT INTO PRODUTO_VENDIDO(QUANTIDADE , COD_VENDA , COD_BARRAS)
VALUES
(10,1,'189181891891896'),
(13,2,'651981719861056'),
(12,3,'645616245754712'),
(100,4,'941651030684943'),
(1,5,'613176498423184'),
(2,6,'651531715632173'),
(3,7,'645987321004164'),
(4,7,'165123184891231'),
(5,8,'654651864869153'),
(6,9,'189181891891896'),
(7,10,'189189132178765'),
(10,11,'891984792130510'),
(70,12,'465423171315621'),
(34,13,'465438413845631'),
(22,14,'651531715632173'),
(12,15,'165123184891231'),
(13,16,'654651864869153'),
(15,17,'645616245754712'),
(10,18,'189189132178765'),
(9,19,'941651030684943'),
(30,20,'165123184891231'),
(10,21,'645616245754712'),
(2,22,'786484312384954');

INSERT INTO COMPRA (DT_SOLICITACAO, DT_ENTREGA, VALOR_TOTAL,
FCODIGO_FUNCIONARIO, CNPJ)
VALUES
('2020-01-06','2020-01-17',3000,3,'12345123000122'),
('2020-01-07','2020-01-19',2000,3,'18837716000187'),
('2020-02-06','2020-02-15',2630,35,'12333334000188'),
('2020-02-07','2020-02-16',1790,30,'12345123000122'),
('2020-02-08','2020-02-18',1600,9,'91900903000277'),
('2020-03-05','2020-03-17',1960,30,'91900903000277'),
('2020-04-04','2020-04-19',2330,35,'47222666000176'),
('2020-04-05','2020-04-20',2500,9,'98289111000111'),
('2020-04-06','2020-04-22',2700,5,'20738234000167'),
('2020-05-06','2020-05-14',3300,5,'10345897000134'),
('2020-05-07','2020-05-13',3350,5,'10345897000134'),
('2020-06-07','2020-06-15',3200,3,'47222666000176'),
('2020-06-08','2020-06-14',3420,41,'17736837000177'),
('2020-06-09','2020-06-16',3950,36,'18837716000187'),
('2020-07-04','2020-07-18',4200,5,'12345123000122'),
('2020-07-05','2020-07-20',4100,35,'17736837000177'),
('2020-08-06','2020-08-17',3900,30,'17736837000177'),
('2020-08-07','2020-08-18',3650,41,'18837716000187'),
('2020-09-06','2020-09-19',4300,36,'98289111000111'),
('2020-09-07','2020-09-20',4120,3,'18837716000187'),
('2020-10-04','2020-10-15',4220,9,'18837716000187'),
('2020-10-05','2020-10-16',3560,9,'20738234000167');

INSERT INTO PRODUTO_COMPRADO (QUANTIDADE , COD_COMPRA ,
COD_BARRAS)
VALUES
(10,1,'891984792130510'),
(13,2,'984617906506885'),
(12,3,'651981719861056'),
(100,4,'684653176513548'),
(1,5,'645616245754712'),
(2,6,'561749805161208'),
(3,7,'561798435121864'),
(4,8,'165156105054176'),
(5,9,'561749805161208'),
(6,10,'165123184891231'),
(7,11,'645987321004164'),
(10,12,'646218317495131'),
(70,13,'317815317621347'),
(34,14,'941651030684943'),
(22,15,'861351761231764'),
(12,16,'613176498423184'),
(13,17,'651891716305605'),
(15,18,'651531715632173'),
(1,19,'189189132178765'),
(9,20,'615817631798456'),
(30,21,'317815317621347'),
(10,22,'168165315615189');
