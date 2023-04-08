import ply.lex as plex
from my_lib import slurp
tokens = ("I", "V", "IV", "OTHER", "IERRO")

t_ignore=" \n\t" # string com a lista de caracteres a ignorar

def t_IV(t):
    r"IV"
    print(t, end='\t')
    print(f"t.type={t.type} t.value='{t.value}' -> valor 4")
    #global total
    #total += 4;
    #pass # ignora o token encontrado
    t.value = 4;  
    return t

def t_IERRO(t):  #  IIII IIIII ...
    r"I{4,}"  
    print(t, end='\t')
    print(f"t.type={t.type} t.value='{t.value}' -> valor {len(t.value)}")
    #global total
    #total += len(t.value);  
    #pass
    print(f"número inválido {t.value}")  
    pass

def t_I(t):  # I | II | III   I{1,3}
    r"I{1,3}"  
    print(t, end='\t')
    print(f"t.type={t.type} t.value='{t.value}' -> valor {len(t.value)}")
    #global total
    #total += len(t.value);  
    #pass
    t.value = len(t.value);  
    return t

def t_V(t):
    r"V"
    print(t, end='\t')
    print(f"t.type={t.type} t.value='{t.value}' -> valor 5")
    #global total
    #total += 5;  
    #pass
    t.value = 5;  
    return t

#def t_OTHER(t):
#    r".|\n"
#    print(t, end='\t')
#    print(f"t.type={t.type} t.value='{t.value}' -> valor ??? ")
#    pass

def t_error(t):
    print("Unexpected token... ")
    exit(1)


lexer = plex.lex()
lexer.input("IV I V II III \n IIII \t")

# lexer.token()
# print(f"somatório: {total}")
total =0
for t in iter(lexer.token, None):
    print(t)
    total += t.value
    # print(f"{t.type} {t.value} {t.lineno} {t.lexpos} ")

print(f"somatório: {total}")