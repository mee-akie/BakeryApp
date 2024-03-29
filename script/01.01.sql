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
    ON DELETE CASCADE
);

CREATE TABLE CLIENTE (
    NOME VARCHAR(70) NOT NULL,
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
    FOREIGN KEY(CODIGO_ESTABELECIMENTO) REFERENCES ESTABELECIMENTO(CODIGO)
);  

CREATE TABLE FUNCIONARIO ( 
    CODIGO_FUNC INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    NOME VARCHAR(70) NOT NULL,          
    CPF CHAR(11) NOT NULL,
    SALARIO DECIMAL (10,2), 
    FERIAS DATE,
    CODIGO_ESTABELECIMENTO INT NOT NULL,
    PRIMARY KEY(CODIGO_FUNC),
    FOREIGN KEY (CODIGO_ESTABELECIMENTO) REFERENCES ESTABELECIMENTO(CODIGO)
);

CREATE TABLE HISTORICO_TRABALHO (
    DATA_REGISTRO  DATE NOT NULL,
    HORA_ENTRADA_R TIME NOT NULL,
    HORA_SAIDA_R TIME NOT NULL,
    FCODIGO_FUNCIONARIO INT NOT NULL,
    PRIMARY KEY(DATA_REGISTRO, HORA_ENTRADA_R, HORA_SAIDA_R, FCODIGO_FUNCIONARIO),
    FOREIGN KEY(FCODIGO_FUNCIONARIO) REFERENCES FUNCIONARIO(CODIGO_FUNC)
);

CREATE TABLE ADMINISTRADOR (
    FCODIGO_FUNCIONARIO INT NOT NULL,
    ESPECIALIDADE VARCHAR(30) NOT NULL,
    PRIMARY KEY(FCODIGO_FUNCIONARIO),
    FOREIGN KEY(FCODIGO_FUNCIONARIO) REFERENCES FUNCIONARIO(CODIGO_FUNC)
);

CREATE TABLE ATENDENTE_CAIXA (
    FCODIGO_FUNCIONARIO INT NOT NULL,
    NIVEL_ESCOLARIDADE VARCHAR(30) NOT NULL,
    PRIMARY KEY(FCODIGO_FUNCIONARIO),
    FOREIGN KEY(FCODIGO_FUNCIONARIO) REFERENCES FUNCIONARIO(CODIGO_FUNC)
);

CREATE TABLE TELEFONE_CONTATO (
    TELEFONE VARCHAR (14) NOT NULL,
    TCODIGO CHAR(14) NOT NULL,
    PRIMARY KEY (TELEFONE),
    FOREIGN KEY(TCODIGO) REFERENCES FORNECEDOR(CNPJ)
);

CREATE TABLE VENDE (
    COD_VENDA INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    DT_VENDA TIMESTAMP NOT NULL,
    VALOR_TOTAL DECIMAL(18,2) NOT NULL,
    FCODIGO_FUNCIONARIO INT NOT NULL,
    CPF CHAR(11) NOT NULL,
    PRIMARY KEY (COD_VENDA),
    FOREIGN KEY (CPF  ) REFERENCES CLIENTE(CPF),
    FOREIGN KEY (FCODIGO_FUNCIONARIO) REFERENCES ATENDENTE_CAIXA(FCODIGO_FUNCIONARIO)
);

CREATE TABLE PRODUTO_VENDIDO (
    COD_PRODUTO_VENDIDO INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    QUANTIDADE INT NOT NULL,
    COD_VENDA INT NOT NULL,
    COD_BARRAS CHAR(15) NOT NULL,
    PRIMARY KEY (COD_PRODUTO_VENDIDO),
    FOREIGN KEY (COD_VENDA ) REFERENCES VENDE(COD_VENDA),
    FOREIGN KEY (COD_BARRAS) REFERENCES PRODUTO(COD_BARRAS)
);

CREATE TABLE COMPRA(
    COD_COMPRA INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    DT_SOLICITACAO TIMESTAMP NOT NULL,
    DT_ENTREGA TIMESTAMP NOT NULL,
    VALOR_TOTAL DECIMAL(18,2) NOT NULL,
    FCODIGO_FUNCIONARIO INT NOT NULL,
    CNPJ CHAR (14) NOT NULL,
    PRIMARY KEY (COD_COMPRA),
    FOREIGN KEY (FCODIGO_FUNCIONARIO ) REFERENCES ADMINISTRADOR(FCODIGO_FUNCIONARIO),
    FOREIGN KEY (CNPJ) REFERENCES FORNECEDOR(CNPJ)
);

CREATE TABLE PRODUTO_COMPRADO (
    COD_PRODUTO_COMPRADO INT NOT NULL GENERATED ALWAYS AS IDENTITY,
    QUANTIDADE INT NOT NULL,
    COD_COMPRA INT NOT NULL,
    COD_BARRAS CHAR(15) NOT NULL,
    PRIMARY KEY (COD_PRODUTO_COMPRADO ),
    FOREIGN KEY (COD_COMPRA  ) REFERENCES COMPRA(COD_COMPRA ),
    FOREIGN KEY (COD_BARRAS) REFERENCES PRODUTO(COD_BARRAS));

----------------------------------------------------------------
---------------------------INSERTS------------------------------
----------------------------------------------------------------

INSERT INTO ESTABELECIMENTO(nome, rua, numero, bairro, cep, cidade)
VALUES
    ('Panificadora Alfa','Rua Projetada', '553', 'Ouro Verde','78135616','Várzea Grande'),
    ('Padaria Seu Nelson','Rua legal', '583', 'Longe','25716080','Petrópolis'),
    ('Padaria da Melissaa','Rua Jose Mendes', '593', 'Atibaia','71927180','Brasília'),
    ('Panificadora Theo','Rua zona leste', '123', 'Guarulhos','61900630','Maracanaú'),
    ('Panificadora Silas','Rua praia', '1553', 'Santos ','49020190','Aracaju'),
    ('Panificadora Will','Rua Dormindo demais', '1234', 'Saúde','70723040','Brasília'),
    ('Padaria Patricia','Rua Nota alta', '1234', 'Felicidade','87308270','Campo Mourão'),
    ('Panificadora Josefa','Rua Scooby Doo', '553', 'Ouro','68902080','Macapá'),
    ('Panificadora Joao','Rua Mario', '553', 'Taboão','54270100','Jaboatão dos Guararapes'),
    ('Panificadora Catarina','Rua Projeta', '553', 'São francisco','26277301','Nova Iguaçu'),
    ('Panificadora Edu','Rua Giulia', '1553', 'Longe demais','77064014','Palmas'),
    ('Panificadora Murilo','Rua Marcado', '5553', 'São Carlos','74970410','Aparecida de Goiânia'),
    ('Panificadora Espirro','Rua Felicidade', '4553', 'Embu das artes','71551204','Brasília'),
    ('Padaria Caetano','Rua dos bobos', '0', 'Lugar nenhum','60830465','Fortaleza'),
    ('Panificadora Penha','Rua Salgada', '5353', 'Jardim Salete','76964107','Cacoal'),
    ('Panificadora Chique','Avenida Faria Lima', '553', 'Pinheiros','69309400','Boa Vista'),
    ('Panificadora Cult','Rua gamer', '4553', 'Pirajussara','64051140','Teresina'),
    ('Panificadora Estudante','Rua Projetada', '553', 'Ouro Verde','93525240','Novo Hamburgo'),
    ('Panificadora Quente','Rua Xuxa', '553', 'Acre','65081622','São Luís'),
    ('Panificadora Mickey','Rua Disney', '77', 'Rondônia','69089071','Manaus');
    
INSERT INTO FORNECEDOR (cnpj, nome, rua, estado, cidade, cep, numero, bairro) VALUES 
('12345123000122', 'Teresinha e Tereza Filmagens ME', 'Avenida Andrade','São Paulo', 'São Paulo', '18053060', '609', 'Vila Bancário'),
('32124222000165', 'Alexandre e Isabella Ferragens Ltda', 'Rua Caracol','São Paulo', 'Valinhos', '12916361', '933', 'São Benedito (Jordanésia)'),
('98847625000198', 'Lívia e Lúcia Marcenaria ME', 'Rua das Rosas','Praça Interact Club', 'São Paulo', '12705120', '762', 'Vila Ema'),
('79123543000212', 'Carlos e Manoel Buffet Ltda', 'Rua Santos Severo Scapol','São Paulo', 'Marília', '12237530', '104', 'Vila Rezende'),
('73243857000232', 'Ester e Vicente Telecomunicações ME', 'Rua Thomaz Bérgamo','São Paulo', 'Jaú', '12232879', '740', 'Jardim Dermínio'),
('10345897000134', 'Thales e Bryan Lavanderia ME', 'Rua Paschoal Carlos Magno','São Paulo', 'Brás', '13189212', '919', 'Jardim Maria Estela'),
('17736837000177', 'Kaique e Renato Entulhos Ltda', 'Rua Pedro Fernandes de Souza','São Paulo', 'São Vicente', '02937080', '732', 'Jardim Miragaia'),
('11938223000144', 'Jaqueline e Teresinha Adega ME', 'Rua Engenheiro Elias Machado de Almeida','São Paulo', 'Bragança Paulista', '15816060', '290', 'Perdizes'),
('20738234000167', 'Anthony e Fabiana Buffet Ltda', 'Rua Parnamirim','Rio de Janeiro', 'Valinhos', '16022620', '752', 'Vila Mamedina'),
('59343746000174', 'Diego e Rosângela Eletrônica ME', 'Rua Valentina de Siqueira Cardoso','São Paulo', 'Campinas', '04719050', '596', 'Vila Romana'),
('30213837000226', 'Murilo e João Esportes ME', 'Rua Gérson Marques da Silva','São Paulo', 'Itapecerica da Serra', '12302050', '596', 'Vila Santa Izabel'),
('90287324000100', 'Lorenzo e Luiza Fotografias ME', 'Rua Benedito Bernardes de Brito','São Paulo', 'Barretos', '18706705', '321', 'Baeta Neves'),
('18837716000187', 'Rosa e Ruan Assessoria Jurídica ME', 'Travessa Martin Faber','São Paulo', 'São Paulo', '06870160', '308', 'Núcleo Bartholomeu Bueno de Miranda'),
('98289111000111', 'Carlos e Thales Ferragens Ltda', 'Rua Jorge Americano 380','Santa Catarina', 'São José do Rio Preto', '15048090', '786', 'Conjunto Habitacional Doutor José Secchi'),
('10987987000177', 'Thiago e Marcos Vinicius Adega Ltda', 'Rua Salvador do Sul','São Paulo', 'Campinas', '12092763', '903', 'Loteamento Nova Espírito Santo'),
('33872982010177', 'Rosa e Mário Marcenaria ME', 'Rua Bolívia','São Paulo', 'Diadema', '16204395', '673', 'Vila Angelo Vial'),
('12333334000188', 'Henry e Márcia Marcenaria Ltda', 'Rua Morro Agudo','São Paulo', 'São Bernardo do Campo', '06709470', '377', 'Piratininga'),
('91900903000277', 'Liz e Isaac Buffet Ltda', 'Avenida Hans Stadem','São Paulo', 'Franca', '05159160', '601', 'Loteamento Loanda'),
('88223555000144', 'Igor e Carolina Telas ME', 'Rua Aureliano Alves Genuíno','São Paulo', 'São José dos Campos', '07223235', '476', 'Cidade Morumbi'),
('47222666000176', 'Ayla e Vitor Gráfica Ltda', 'Rua Antonieta de Marco','São Paulo', 'Sorocaba', '13331674', '994', 'Chácara São Luiz');

INSERT INTO CLIENTE (NOME, CPF, DATANASC)
VALUES 
    ('Giovanni Matheus Leandro Silva', '22469763088', '2001-03-19'),
    ('Giovanni Matheus Leandro Silva', '92965266046', '2004-03-02'),
    ('Thomas César Cláudio da Cunha', '23333396084', '2003-01-04'),
    ('Samuel Juan Santos', '51247966003', '1988-08-25'),
    ('Bárbara Lavínia Santos', '10214031055', '1946-03-26'),
    ('Patrícia Francisca da Paz', '97853491956', '1995-08-13'),
    ('Arthur Augusto Renato Brito','78896957990','1988-10-12'),
    ('Rosângela Giovana da Cunha','70628971087','1999-12-17'),
    ('Juan Mário Victor Silva','66978464376','1982-02-08'),
    ('Sebastião Lorenzo Rocha','18579663849','1942-10-07'),
    ('Marina Olivia Joana da Mota','81940392667','1969-09-26'),
    ('Fátima Lavínia Lima','91689441011','1958-11-06'),
    ('Isabela Lívia Vanessa Figueiredo','60367866382','1963-07-14'),
    ('Juliana Maria Pires','66643517303','1961-06-03'),
    ('Marcelo Iago Sebastião Rodrigues','65153214492','1941-05-15'),
    ('Clara Luiza Kamilly Souza','89759133172','1956-02-18'),
    ('Daniel Isaac Pietro Porto','73509000153','1959-04-02'),
    ('Yago Isaac Arthur Alves','98367827249','1989-04-11'),
    ('Danilo Osvaldo Manuel Mendes','7841437370','1946-12-01'),
    ('Eduarda Clarice da Cruz','19275326800','1988-03-02'),
    ('Elaine Vera Aragão','79461912005','1979-03-11'),
    ('Stefany Elza Antonella da Luz','08177733660','1965-10-23'),
    ('Aline Sandra Fernandes','65853503596','1946-12-09'),
    ('Geraldo Cauã da Cunha','92842487109','1941-06-15'),
    ('Ruan Gabriel Danilo Rodrigues','66796028740','1970-12-07');
    
INSERT INTO PRODUTO (COD_BARRAS, NOME, NOME_FABRICANTE, PRECO, DATA_FABRICACAO, CATEGORIA, QTD_ESTOQUE, DATA_VENCIMENTO)
VALUES 
    ('189181891891896','Pão de Mel','Indústrias de Melaço',12.25,'2020-01-02','Doces',5,'2020-02-02'),
    ('189189132178765','Pão de Queijo','Pães Mineiros',5.12,'2020-06-05','Pães',7,'2021-01-01'),
    ('654651864869153','Pão Francês','Caseiros',0.25,'2020-10-15','Pães',2,'2020-10-16'),
    ('317815317621347','Coxinha','Salgados do seu Jorge',4.50,'2019-05-12','Salgados',1,'2021-08-12'),
    ('651531715632173','Mistinho','Salgados do seu Jorge',8.99,'2019-05-12','Salgados',4,'2021-09-11'),
    ('751896317781376','Maravilha','Salgados do seu Jorge',3.23,'2019-05-12','Salgados',1,'2021-07-22'),
    ('165156105054176','Detergente','Vanish',15.99,'2019-05-12','Limpeza',6,'2020-01-01'),
    ('465438413845631','Rodo','Madeira e Madeira',25.50,'2021-05-05','Limpeza',4,'2021-07-07'),
    ('646218317495131','Pano de chão','Madeira e Madeira',4.99,'2021-01-10','Limpeza',11,'2021-10-15'),
    ('786484312384954','Geladinha','Dr. Oetker',1.00,'2020-12-21','Produto Alimentício',15,'2021-12-21'),
    ('648796521560431','Bolinho','Ana Maria',4.99,'2021-01-01','Comida',7,'2021-07-12'),
    ('645987321004164','Geleia','Linea',7.95,'2020-01-15','Comida',8,'2021-07-12'),
    ('613176498423184','Queijo','Seara',8.99,'2021-11-12','Frios',1,'2021-12-12'),
    ('615817631798456','Mussarela','Sadia',9.99,'2021-02-05','Frios',6,'2021-05-31'),
    ('561798435121864','Presunto','Seara',15.05,'2020-12-15','Frios',3,'2021-01-05'),
    ('465423171315621','Mortadela','Sadia',20.00,'2020-07-25','Frios',6,'2021-03-12'),
    ('861351761231764','Queijinho','Polenguinho',55.20,'2021-01-02','Frios',5,'2021-02-01'),
    ('645616245754712','Ovo de Chocolate','Kinder Ovo',12.20,'2019-06-22','Sobremesa',5,'2022-06-12'),
    ('618917416617912','Margarina','Qualy',12.55,'2018-05-16','Laticínios',6,'2021-08-26'),
    ('168165315615189','Manteiga','Qualy',13.50,'2017-07-15','Laticínios',9,'2020-09-08'),
    ('165123184891231','Pão Integral','Puma',8.00,'2020-08-12','Pães',4,'2021-10-10'),
    ('684653176513548','Pão de Forma','Puma',9.50,'2020-09-12','Pães',6,'2022-04-17'),
    ('984617906506885','Requeijão','Catupiry',14.55,'2021-07-16','Laticínios',8,'2022-09-14'),
    ('561749805161208','Catupiry','Catupiry',18.60,'2021-09-23','Laticínios',9,'2022-07-16'),
    ('654894231050407','Chinelo','Havaianas',25.00,'2020-03-03','Vestimentas',1,'2025-03-03'),
    ('891984792130510','Suco Laranja','Tang',4.99,'2021-01-15','Bebida',6,'2022-06-18'),
    ('165105608792068','Suco Uva','Tang',4.99,'2021-01-15','Bebida',7,'2022-06-18'),
    ('941651030684943','Suco Morango','Tang',4.99,'2021-01-15','Bebida',8,'2022-06-18'),
    ('651891716305605','Suco Abacaxi','Tang',4.99,'2021-01-15','Bebida',2,'2022-06-18'),
    ('651981719861056','Suco Limão','Tang',4.99,'2021-01-15','Bebida',16,'2022-06-18');

INSERT INTO CONTA (COD_BARRAS, TIPO, VALOR, DATA_VENCIMENTO, DATA_PAGAMENTO, PAGO, codigo_estabelecimento) VALUES
(123456789012345678904321987162739487654319023234,'conta de luz do mes de janeiro' , 74.38,'2021-02-05', '2021-02-01', TRUE,1),
(987162739487654319023234123487689012345678904321, 'conta de agua do mes de marco', 70.21,'2021-05-21', '2021-04-12', TRUE,1),
(123487689012345678904321982134657890123456729875, 'conserto da pia do banheiro', 53.00, '2021-11-01', NULL, FALSE,1),
(821346578901234567298765123487689012345678904321, 'itens de decoracao', 121.21,'2021-10-01', NULL, FALSE,1),
(000487689012345678904321000000001119287653981432, 'supermercado convem', 143.92, '2021-02-12', '2021-02-11', TRUE,2),
(000000001119287653981432123487689000018978904321, 'itens de cozinha', 219.12,'2021-04-06', '2021-03-28', TRUE,2),
(101010101010101010101010999987689012345678904321, 'produtos de limpeza', 85.34, '2021-08-04', NULL, FALSE,2),
(123487689012345678904321101010101010101010101010, 'fornecedor Sr Joao Carvalho', 183.21, '2021-09-12', NULL, FALSE,2),
(999987689012345678904321123487689012345678904321, 'aluguel do mes de fevereiro', 3500.00, '2021-03-01', '2021-01-28', TRUE,3),
(123487689012345678904321888888888822222222224563, 'aluguel do mes de marco', 3500.00, '2021-04-01', '2021-03-24', TRUE,3),
(888888888822222222224563123487689012345678904321, 'conta de luz do mes de abril', 82.12, '2021-03-06', '2021-03-02', TRUE,3),
(555555589012345678904321858585858585858585858585, 'conta de agua do mes de junho', 62.54, '2021-07-01', '2021-06-23', TRUE,3),
(123487689012345678904321555555589012345678904321, 'supermercado champ', 301.65, '2021-11-01', NULL, FALSE,4),
(858585858585858585858585123487689012345678904321, 'produtos de limpeza', 54.21, '2021-10-01', '2021-09-21', TRUE,4),
(123487689012345678904321123487689000000078904321, 'aluguel do mes de junho', 3510.00, '2021-07-03', '2021-06-25', TRUE,4),
(666687689000000078904321222222222212345678904321, 'supermercado convem', 128.25, '2021-11-10', NULL, FALSE,4),
(767676689012345678904321767676689012345678904321, 'fornecedora Srta Marilia Barros', 129.65,'2021-11-10', NULL, FALSE,5),
(123487689012345678904321767676689012345678904321, 'conta de luz do mes de outubro', 70.21, '2021-10-28', '2021-10-24', TRUE,5),
(123487689033333378904321123487689033333378902222, 'aluguel do mes de outubro', 3510.00, '2021-11-02', NULL, FALSE,5),
(123487689000000078904321666687689000000078904321, 'fornecedor Sr Joao Carvalho', 121.45, '2021-09-09', '2021-09-02', TRUE,5),
(222222222212345678904321222222222212345678904321, 'fornecedor Quitanda Sol Nascente', 134.21, '2021-05-23', '2021-05-12', TRUE,6);

INSERT INTO FUNCIONARIO (NOME, CPF, SALARIO, FERIAS, codigo_estabelecimento) VALUES
('MARIA EDUARDA', '23456712356', 3000, NULL, 1),
('MARIO SANTOS', '44454798012', 2500, '2021-02-10',1),
('IAM SILVEIRA','10104387828', 3000, '2021-10-21',1),
('LAIS SILVA', '20084521388', 5000, NULL,1),
('RODRIGO CAMARA', '30299902019', 2500, '2021-03-02',2),
('BENEDITA MAGALHAES','48291028371', 3200, '2021-01-20',2),
('MARTIN COELHO', '12323458653', 2800.80, NULL,2),
('JADE PONTE', '20981726367', 2830, NULL,2),
('GLORIA BERNARDES', '18726354663', 3200, '2021-05-23',3),
('ELISEU BASTOS', '20010239888', 2700, '2021-07-11',3),
('GILBERTO LARA', '11122233392', 2300, '2020-07-02',3),
('CALEB BOAVENTURA', '33183723212', 2500, '2020-05-21',3),
('RYAN TUNA', '19329387172', 2500, NULL,4),
('EVELYN BRAGANCA', '34521000002', 3200, '2020-04-19',4),
('CIARA FELIX', '12674325678', 3100, NULL,4),
('GABRIELA MARQUES', '19827183215', 2500, NULL,5),
('GIOVANNI CASTELO','19200235891', 5200, NULL,5),
('LUIZ ABRANCHES', '19287369100', 4200, NULL,5),
('RODOLFO AMORIN', '80291222281', 4100, NULL,6),
('BIANCA SANTANA', '92012332212', 2500, NULL,6),
('Sebastião Felipe da Mata', '04732289126', 1200,'2020-12-12',7),
('Roberto Vitor Silveira', '73510771931',2410,'2020-05-07',7),
('Vitória Francisca da Cunha', '96235126603',2550,NULL,7),
('Luiza Sebastiana Sarah Cavalcanti', '80382414799',5660,NULL,7),
('Lucas Iago Thiago de Paula', '73302515502',2500,NULL,8),
('Clara Bárbara da Luz', '14592011830',1200,'2019-08-12',8),
('Isabelly Elaine Tânia Rodrigues', '98482060864',1750,'2018-06-12',8),
('Luzia Maya Jennifer Lima', '17293420943',1960,'2019-06-02',9),
('Emanuelly Camila Barros', '67937562145',2250,NULL,9),
('José Diego Fogaça', '62808743033',3550,NULL,9),
('Isabelly Aurora Milena Campos', '40656407093',1880,NULL,10),
('Laura Bárbara Alice Corte Real', '66554096329',1990,NULL,10),
('Luzia Sarah da Luz', '51405973811',2660,'2020-05-05',10),
('Alice Pietra Jaqueline Moraes', '83600719424',2700,NULL,11),
('Renato Jorge Rafael Pires', '19542274505',2900,NULL,11),
('Severino César Luiz Monteiro', '49042543256',2800,'2021-01-05',11),
('Matheus Lucas Ribeiro', '29846269820',2700,NULL,11),
('Nathan Victor Barbosa', '53731151421',2900,'2019-09-13',12),
('Julia Raimunda Figueiredo', '94789134504',2650,NULL,12),
('Flávia Alessandra Catarina Freitas', '11890984078',2300,NULL,13),
('Carolina Ana Letícia Pires', '04417662428',2200,'2021-04-03',13),
('Noah Davi da Mota', '56321800341',2000,'2020-12-24',13),
('Aparecida Marcela Castro', '41003771343',3700,'2021-06-18',14),
('Luana Helena Gabriela Nogueira', '34844539078',4200,NULL,14),
('Tiago Renan Melo', '08166327660',2300,NULL,14),
('Elaine Aparecida Rezende', '38354689360',1750,NULL,15),
('Rayssa Kamilly Priscila da Paz', '41435182103',1900,'2021-04-05',15),
('Anthony Noah Campos', '88337111020',2300,'2021-04-06',15),
('Eloá Gabriela Evelyn Lopes', '50605512108',2350,'2020-04-04',16),
('Elza Flávia Giovana Aparício', '85858226191',2600,'2020-12-12',16),
('Bernardo Alexandre Corte Real', '39046379086',2200,NULL,16),
('Fabiana Andreia Jesus', '90667847685',2650,NULL,17),
('Joana Rosângela Aparício', '73272955267',1750,NULL,17),
('Erick Augusto Juan da Paz', '26456643180',6190,NULL,18),
('Carla Marlene Bianca Almeida', '84484673703',5500,'2020-01-06',18),
('Rayssa Alice Fabiana Assis', '29720861207',2660,'2021-06-04',19),
('Victor Theo Bernardes', '69102534770',2400,NULL,19),
('Bernardo Otávio Novaes', '88394941206',3200,NULL,19),
('Thiago Murilo Thales da Paz', '63046268866',2000,'2017-02-28',20),
('Renata Analu Luna Campos', '82047533147',2600,NULL,20);

INSERT INTO HISTORICO_TRABALHO (DATA_REGISTRO, HORA_ENTRADA_R, HORA_SAIDA_R, FCODIGO_FUNCIONARIO)
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
(3, 'Gestão de Pessoas'),
(5, 'Gestão Logística'),
(9, 'RH'),
(20,'Administração'),
(25,'Gestão de Pessoas'),
(30,'RH'),
(35,'Gestão de Pessoas'),
(40,'Gestão Logística'),
(45,'PHD de Processos'),
(50,'RH'),
(55,'Marketing'),
(60,'Administração de Empresas'),
(21,'Gestão de Processos'),
(26,'Gestão de Pessoas'),
(31,'Marketing'),
(36,'Gestão de Leads'),
(41,'Economia'),
(46,'Gestão Logística'),
(51,'Marketing'),
(56,'Gestão de Processos');

INSERT INTO ATENDENTE_CAIXA (FCODIGO_FUNCIONARIO, NIVEL_ESCOLARIDADE)
VALUES 
(1, 'Médio Completo'),
(10, 'Superior Completo'),
(12, 'Superior Incompleto'),
(15, 'Médio Incompleto'),
(13, 'Superior Incompleto'),
(22, 'Fundamental Completo'),
(27, 'Fundamental Incompleto'),
(32, 'Médio Completo'),
(37, 'Superior Completo'),
(42, 'Superior Completo'),
(47, 'Superior Completo'),
(52, 'Superior Incompleto'),
(57, 'Médio Completo'),
(23, 'Superior Incompleto'),
(28, 'Médio Incompleto'),
(33, 'Médio Completo'),
(38, 'Fundamental Incompleto'),
(43, 'Fundamental Incompleto'),
(48, 'Médio Completo'),
(53, 'Médio Completo');

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
    
INSERT INTO COMPRA (DT_SOLICITACAO, DT_ENTREGA, VALOR_TOTAL, FCODIGO_FUNCIONARIO, CNPJ)
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
    
INSERT INTO PRODUTO_COMPRADO (QUANTIDADE , COD_COMPRA , COD_BARRAS)
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


