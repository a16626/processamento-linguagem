import ply.lex as plex
import re

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

produto_preco = 0

valor_moedas = {"c50": 0.50,"c5":0.05,"c20":0.20, "c10":0.10,"e1":1.00,"e2":2.00}

moedeiro = [{"nome":"c50","c50": 0.50, "stock":0}, {"nome":"c5","c5":0.05, "stock":0}, {"nome":"c20","c20":0.20, "stock":0}, {"nome":"c10","c10":0.10, "stock":0}, {"nome":"e1","e1":1.00, "stock":0}, {"nome":"e2","e2":2.00,"stock":0}]
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

    parts = t.value.split()

    nome = parts[0].split('=')[1]
    preco = float(parts[1].split('=')[1])
    stock = int(parts[2].split('=')[1])

    for produto in produtos:
        if produto["nome"] == nome:
            return t

    novo_produto = {"nome": nome, "preco": preco, "stock": stock}
    produtos.append(novo_produto)   


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




#def t_ADMIN_ADICIONAR(t):
 #   r"nome=([a-z]+)\s+preco=([\d]+(\.\d+)?)\s+stock=(\d+)"
  #  for produto in produtos:
   #     if(produto["nome"] == t.value):
    #        return t
     #   else:
      #      nome = t.lexer.lexmatch.group(1)
       #     preco = float(t.lexer.lexmatch.group(2))
        #    stock = int(t.lexer.lexmatch.group(4))
         #   print(f"{nome} {preco} {stock}")
          #  novo_produto = {"nome": nome, "preco": preco, "stock": stock}
           # produtos.append(novo_produto)

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
    if aux is True:
        for coin in t.value.split(','):
            if coin.strip() in valor_moedas:
                valor_inserido += valor_moedas[coin.strip()]
                saldo += valor_moedas[coin.strip()]
                ERROR = ""
    else:
        ERROR = 'error'
    aux = False

def t_USER_CANCELAR(t):
    r"CANCELAR"
    t.lexer.begin("INITIAL")
    pass


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

def ReadFile(filename):
    with open(filename, "r") as fh:
        contents = fh.read()
    return contents

#--------------------------Instância do lexer---------------------------------------------
lexer = plex.lex()

def lexer_input(user_string):
    lexer.input(user_string)
    lexer.token()
    global valor_inserido
    global produto_preco
    global ERROR

    return {
        "valor_inserido": valor_inserido,
        "saldo": saldo,
        "produto_escolhido": produto_user,
        "produto_preco": produto_preco,
        "ERROR": ERROR
    }
    valor_inserido = 0
