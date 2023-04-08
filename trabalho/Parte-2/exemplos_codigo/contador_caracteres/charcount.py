import ply.lex as plex
from my_lib import slurp

tokens = ("NL", "OUTRO", "MAIUSC", "MINUSC", "DIGITO", "ESPACO")
acumulador = {}

def t_DIGITO(t):
    r"[0-9]+"
    global acumulador
    acumulador["digito"] = acumulador.get("digito", 0) + len(t.value)
    pass

def t_ESPACO(t):
    r"[ ]+"
    global counter
    acumulador["espaco"] = acumulador.get("espaco", 0) + len(t.value)
    pass

def t_MAIUSC(t):
    r"[A-Z]+"
    global counter
    acumulador["maiuscula"] = acumulador.get("maiuscula", 0) + len(t.value)
    pass

def t_MINUSC(t):
    r"[a-z]+"
    global counter
    acumulador["minuscula"] = acumulador.get("minuscula", 0) + len(t.value)
    pass

def t_OUTRO(t):
    r"."
    global counter
    print (t.type, t.value, t.lineno, t.lexpos)
    acumulador["outro"] = acumulador.get("outro", 0) + 1
    pass

def t_NL(t):
    r"\n"
    t.lexer.lineno +=1 # len(t.value)
    global counter
    acumulador["nova linha"] = acumulador.get("nova linha", 0) + 1
    pass


def t_error(t):
    print("Token desconhecido...  {t.value[:10]}")
    exit(1)


lexer = plex.lex()
lexer.input(slurp("texto_entrada.txt"))
lexer.token()


for tipoCaracter in acumulador.keys():
    print(f"Número de {tipoCaracter}: {acumulador[tipoCaracter]}")
