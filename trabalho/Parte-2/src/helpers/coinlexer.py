import ply.lex as plex
import re

tokens = ("PRODUTO", "QUANTIA", "CANCELAR",  "MOEDA", "EQUALS", "error", "END", "DESIGNACAO", "SUDO", "ADICIONAR")

states = (
            ('USER', 'exclusive'),('ADMIN', 'exclusive')
        )

saldo = 0
valor_inserido = 0
produto_user = None
temp_nome = None
temp_preco = None
temp_stock = None

produto_preco = 0

valor_moedas = {"c50": 0.50, "c5":0.05, "c20":0.20, "c10":0.10, "e1":1.00, "e2":2.00}

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
    t.lexer.begin("USER")
    pass

def t_USER_MOEDA(t):
    r"((c50|c20|c5|c10|e1|e2)(,?)(\s)*)+"
    global saldo
    global string
    global valor_inserido
    for coin in t.value.split(','):
        if coin.strip() in valor_moedas:
            valor_inserido += valor_moedas[coin.strip()]
            saldo += valor_moedas[coin.strip()]
    pass

def t_USER_PRODUTO(t):
    r"PRODUTO="
    pass

def t_USER_DESIGNACAO(t):
    r"[a-z]+"
    global produto_user
    found = False
    for produto in produtos:
        if produto["nome"] == t.value:
            produto_user = t.value
            found = True
            produto_preco = produto["preco"]
            break

    if not found:
        t.type = "error"
        t.value = f"Product not found: {t.value}"
        return t

#---------------------------Funções de Erro do lexer--------------------------------------
def t_USER_error(t):
    print(f"Token not recognized at USER state: {t.value[0]}")
    t.lexer.skip(1)

def t_error(t):
    print(f"Token invalido {t.value[0]}")
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

    return {
        "valor_inserido": valor_inserido,
        "saldo": saldo,
        "produto_escolhido": produto_user,
        "preco_produto": produto_preco
    }
    valor_inserido = 0

#print(lexer_input("QUANTIA c20, c50, e1, e2"))
