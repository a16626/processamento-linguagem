import ply.lex as plex

tokens = ("PRODUTO", "QUANTIA", "CANCELAR",  "MOEDA", "EQUALS", "error", "END", "DESIGNACAO")

states = (
            ('USER', 'exclusive'),
        )

saldo = 0
valor_inserido = 0
produto_user = None
produto_preco = 0

valor_moedas = {"c50": 0.50, "c5":0.05, "c20":0.20, "c10":0.10, "e1":1.00, "e2":2.00}

#--------------------------------PRODUTOS--------------------------------------------------
produtos = [{"nome":"twix","preco":1,"stock":20 }, {"nome":"mars","preco":1.2,"stock":20}]

#funções para os produtos
def return_products():
    return produtos


#-------------------------------Funções do lexer-------------------------------------------
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

def t_USER_QUANTIA(t):
    r"QUANTIA(\s)"
    pass

def t_USER_PRODUTO(t):
    r"PRODUTO="
    pass

def t_USER_DESIGNACAO(t):
    r"[a-z]+"
    global produto_user
    global produto_preco
    found = False
    for produto in produtos:
        if produto["nome"] == t.value:
            produto_user = t.value
            found = True
            produto_preco = produto["preco"]
            break

#---------------------------Funções de Erro do lexer--------------------------------------
def t_USER_error(t):
    print(f"Token not recognized at USER state: {t.value[0]}")
    t.lexer.skip(1)

def t_error(t):
    print(f"Token invalido {t.value[0]}")
    t.lexer.skip(1)


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
        "produto_preco": produto_preco
    }
    valor_inserido = 0

#print(lexer_input("QUANTIA c20, c50, e1, e2"))
