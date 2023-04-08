"""
ESI laboral (Processamento de Linguagens)
Aula 13 -   30/março quinta-feira, 14:00
"""
import ply.lex as plex
from my_lib import slurp

tokens = ("EQ", "NUM", "NL", "OTHER", "ON", "OFF")
states = (("SOMAR","exclusive" ), )

somatorio = 0

def t_SOMAR_EQ(t): #  token:  "EQ"  
    r"="
    print(f"\tsoma parcial: {somatorio}")
    pass

def t_SOMAR_NUM(t):   # token: "NUM"
    r"[0-9]+"
    print(f"{t.value}", end=' ')
    global somatorio
    somatorio += int(t.value)
    pass

def t_ON(t):   
    r"[oO][nN]"
    t.lexer.begin("SOMAR")
    pass  

def t_SOMAR_OFF(t):   
    r"[oO][fF][fF]"
    t.lexer.begin("INITIAL")
    global somatorio
    print(f"\tsoma: {somatorio}")
    somatorio=0
    pass   

def t_ANY_OTHER(t): # token: "OTHER"
    r"."
    pass

def t_ANY_NL(t):   # toke: "NL"
    r"\n"
    pass

def t_error(t):
    print(f"Token not recognized at INITIAL state: {t.value[:10]}")
    exit(1)

def t_SOMAR_error(t):
    print(f"Token not recognized at SOMAR state: {t.value[:10]}")
    exit(1)

lexer = plex.lex()
lexer.input(slurp("texto_entrada_v3.txt"))

lexer.token()
# print(f"soma: {somatorio}")



