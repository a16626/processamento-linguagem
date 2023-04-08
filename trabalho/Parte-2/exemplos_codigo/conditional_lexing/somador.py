"""
ESI laboral (Processamento de Linguagens)
Aula 11 
"""
import ply.lex as plex
from my_lib import slurp

tokens = ("EQ", "NUM", "NL", "OTHER")
somatorio = 0

def t_EQ(t): #  token:  "EQ"  
    r"="
    #global somatorio
    print(f"soma parcial: {somatorio}")
    pass

def t_NUM(t):   # token: "NUM"
    r"[0-9]+"
    #  t.value  # lexema: valor do token 
    global somatorio
    somatorio += int(t.value)
    pass
    
def t_OTHER(t): # token: "OTHER"
    r"."
    pass

def t_NL(t):   # toke: "NL"
    r"\n"
    pass

def t_error(t):
    print("Token not recognized: {t.value[:10]}")
    exit(1)


lexer = plex.lex()
lexer.input(slurp("texto_entrada.txt"))
lexer.token()


print(f"soma total: {somatorio}")


