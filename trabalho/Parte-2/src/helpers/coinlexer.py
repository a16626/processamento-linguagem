import ply.lex as plex
import re
from decimal import Decimal

tokens = ("PRODUTO", "QUANTIA", "CANCELAR",  "MOEDA", "EQUALS", "error", "END", "DESIGNACAO", "SUDO", "ADICIONAR","NL")

states = (
            ('USER', 'exclusive'),('ADMIN', 'exclusive')
        )

ERROR = None
aux = False
saldo = 0
valor_inserido = 0
produto_user = None
temp_nome = None
temp_preco = None
temp_stock = None
produto_admin = None
moedas_adicionadas = []

produto_preco = 0

valor_moedas = {"c50": 0.50,"c5":0.05,"c20":0.20, "c10":0.10,"e1":1.00,"e2":2.00}

moedeiro = [{"nome":"c50","valor": 0.50, "stock":0}, {"nome":"c5","valor":0.05, "stock":0}, {"nome":"c20","valor":0.20, "stock":0}, {"nome":"c10","valor":0.10, "stock":0}, {"nome":"e1","valor":1.00, "stock":0}, {"nome":"e2","valor":2.00,"stock":0}]
#--------------------------------PRODUTOS--------------------------------------------------
produtos = [{"nome":"twix","preco":1,"stock":20 }, {"nome":"mars","preco":1.2,"stock":20}]

#funções para os produtos
def return_products():
    return produtos
#-------------------------------Funções do lexer(ADMIN)-------------------------------------------
def t_SUDO(t):
    r"SUDO\n"
    t.lexer.begin("ADMIN")
    pass

def t_ADMIN_ADICIONAR(t):
    r"nome=([a-z]+)\s+preco=([\d]+(\.\d+)?)\s+stock=(\d+)(\n|$)"
    global produto_admin
    parts = t.value.split()

    nome = parts[0].split('=')[1]
    preco = float(parts[1].split('=')[1])
    stock = int(parts[2].split('=')[1])

    for produto in produtos:
        if produto["nome"] == nome:
            return t

    novo_produto = {"nome": nome, "preco": preco, "stock": stock}
    produtos.append(novo_produto)
    produto_admin = novo_produto


def t_ADMIN_CANCELAR(t):
    r"CANCELAR"
    t.lexer.begin("USER")
    pass

def t_ADMIN_MOEDEIRO(t):
    r"(c5|c10|c20|c50|e1|e2)=[0-9]+"
    parts=t.value.split("=")

    moeda = parts[0]
    stock= int(parts[1])

    for moedeiroT in moedeiro:
        if moedeiroT["nome"] == moeda:
            moedeiroT["stock"]=stock


def t_ADMIN_NL(t):
    r"\n"
    pass

def t_ADMIN_error(t):
    print(f"Token not recognized at ADMIN state: {t.value[0]}")
    t.lexer.skip(1)

#-------------------------------Funções do lexer(USER)-------------------------------------------
def t_QUANTIA(t):
    r"QUANTIA(\s)"
    global aux
    aux = True
    t.lexer.begin("USER")

def t_USER_MOEDA(t):
    r"((c50|c20|c5|c10|e1|e2)(,?)(\s)*)+"
    global saldo
    global string
    global valor_inserido
    global aux
    global ERROR
    global moedas_adicionadas
    if aux is True:
        for coin in t.value.split(','):
            if coin.strip() in valor_moedas:
                valor_inserido += valor_moedas[coin.strip()]
                saldo += valor_moedas[coin.strip()]
                ERROR = ""
                moedas_adicionadas.append(valor_moedas[coin.strip()])
    else:
        ERROR = 'error'
    aux = False

    #print(moedas_adicionadas)

    for moeda in moedas_adicionadas:
        for moeda_s in moedeiro:
            if (moeda == moeda_s["valor"]):
                moeda_s["stock"] = moeda_s["stock"] + 1

    moedas_adicionadas =[]

    print(moedeiro)

def t_USER_CANCELAR(t):
    r"CANCELAR"
    t.lexer.begin("INITIAL")

    for moeda in moedas_adicionadas:
        for moeda_s in moedeiro:
            if (moeda == moeda_s["valor"]):
                moeda_s["stock"] = moeda_s["stock"] - 1

    #print(moedeiro)
    pass

def t_USER_SUDO(t):
    r"SUDO"
    t.lexer.begin("ADMIN")


def t_USER_QUANTIA(t):
    r"QUANTIA(\s)"
    global aux
    aux = True
    pass

def t_USER_PRODUTO(t):
    r"PRODUTO="
    global aux
    aux = True
    pass

def t_USER_DESIGNACAO(t):
    r"[a-z]+"
    global produto_user
    global produto_preco
    global ERROR
    global aux
    found = False

    if aux is True:
        for produto in produtos:
            if produto["nome"] == t.value:
                produto_user = t.value
                found = True
                produto_preco = produto["preco"]
                ERROR = ""
                break

            if not found:
                ERROR = "error"
                #t.type = "error"
                #t.value = f"Product not found: {t.value
    else:
        ERROR = "error"
    aux = False

#---------------------------Funções de Erro do lexer--------------------------------------
def t_USER_error(t):
    print(f"Token not recognized at USER state: {t.value[0]}")
    global ERROR
    global saldo
    global valor_inserido
    saldo = 0
    valor_inserido = 0
    ERROR = t.type
    t.lexer.skip(1)

def t_error(t):
    print(f"Token invalido {t.value[0]}")
    global ERROR
    ERROR = t.type;
    t.lexer.skip(1)


#--------------------------Funções para o administrador----------------------------------
def ReadFile(filename):
    with open(filename, "r") as fh:
        contents = fh.read()
    return contents
def WriteFile(filename):
    file1 = open(filename, "w")


    for Moedas in moedeiro:
        file1.write("%s=%d\n" % (Moedas["nome"],Moedas["stock"]))
    file1.write("CANCELAR")
    
    


#--------------------------Função para o moedeiro----------------------------------------

def troco(valor_troco):

    count = 0
    maior_moeda = 0
    moeda_index = 0
    nome_moeda = ''
    moedas = []
    moedas_dic = None

    while valor_troco != 0:
        for moeda in moedeiro:
            if (moeda["valor"] <= valor_troco and moeda["stock"] > 0):
                if (moeda["valor"] > maior_moeda):
                    maior_moeda = moeda["valor"]
                    nome_moeda = moeda["nome"]

        valor_troco = float("{:.2f}".format(valor_troco)) - float("{:.2f}".format(maior_moeda))
        count = count + maior_moeda
        maior_moeda = 0
        moedas.append(nome_moeda)
        for moeda in moedeiro:
            if (moeda["nome"] == nome_moeda):
                moeda["stock"] = moeda["stock"] - 1


    #Contar numero de moedas
    moedas_dic ={i:moedas.count(i) for i in moedas}


    #print(moedas_dic)
    #print(moedas_dic)
    return moedas_dic





#--------------------------Instância do lexer--------------------------------------------
lexer = plex.lex()

def lexer_input(user_string):
    lexer.input(user_string)
    lexer.token()
    global valor_inserido
    global produto_preco
    global ERROR
    global produto_admin

    return {
        "valor_inserido": valor_inserido,
        "saldo": saldo,
        "produto_escolhido": produto_user,
        "produto_preco": produto_preco,
        "ERROR": ERROR,
        "admin": produto_admin
    }
    valor_inserido = 0
