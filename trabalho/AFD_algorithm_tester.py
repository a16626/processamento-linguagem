"""
ESI laboral (Processamento de Linguagens)
Aula 10 -   16/março quinta-feira, 14:00-16:00
"""
from typing import List

V = set([str(i) for i in range(0,10)] + [".", "e", "+", "-"])# {"0", "1"... }


print(V)

Q = { "q0", "q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10"}

tt = { "q0": { "digito":"q1", ".":"q4", "e":"ERRO", "+":"q2", "-":"q3"},
      "q1": { "digito":"q1", ".":"q6", "e":"q7", "+":"ERRO", "-":"ERRO"},
      "q2": { "digito":"q1", ".":"ERRO", "e":"ERRO", "+":"ERRO", "-":"ERRO" },
      "q3": { "digito":"q1", ".":"ERRO", "e":"ERRO", "+":"ERRO", "-":"ERRO" },
      "q4": { "digito":"q5", ".":"ERRO", "e":"ERRO", "+":"ERRO", "-":"ERRO"},
      "q5": { "digito":"q5", ".":"ERRO", "e":"q7", "+":"ERRO", "-":"ERRO" },
      "q6": { "digito":"q5", ".":"ERRO", "e":"ERRO", "+":"ERRO", "-":"ERRO" },
      "q7": { "digito":"q8", ".":"ERRO", "e":"ERRO", "+":"q10", "-":"q9" },
      "q8": { "digito":"q8", ".":"ERRO", "e":"ERRO", "+":"ERRO", "-":"ERRO" },
      "q9": { "digito":"q8", ".":"ERRO", "e":"ERRO", "+":"ERRO", "-":"ERRO" },
      "q10": { "digito":"q8", ".":"ERRO", "e":"ERRO", "+":"ERRO", "-":"ERRO" }
    }


q0 = "q0"
F = {"q8"}


def categorize_symbol(symbol: str) -> str:
    if symbol.isdigit():
        return "digito"
    return symbol



def reconhece(palavra: str)-> bool:
	"""_summary_
       função que implementa o algoritmo de reconhecimento
 de uma palavra...

	Args:
		palavra (str): _description_
		palavra a ser reconhecida
	Returns:
		bool: _description_
	"""
	alpha = q0  # alpha representa o estado atual (começa em q0)
	while len(palavra)>0 and alpha != "ERRO" :
		#simbolo_atual = palavra[0]  # primeira posição
		#palavra=palavra[1:]         # da segunda posição para frente
		simbolo_atual, *palavra = palavra
		if (simbolo_atual in V) : #and (simbolo_atual in tt[alpha]) :
			## simbolo_atual = "digito"
			alpha = tt[alpha][categorize_symbol(simbolo_atual)]
		else:
			alpha = "ERRO"
		#alpha = tt[alpha][simbolo_atual] if (simbolo_atual in V) and (simbolo_atual in tt[alpha]) else "ERRO"
		# a = valido? x: y;    // em C
		# a = x  if valido else y  // em Python
 	# termina o while
	return (len(palavra)==0) and (alpha in F)

def testar_reconhece(ps: List[str])->None:
	print('palavra','reconhece(palavra)',sep=' \t')
	for p in ps:
		print(f"'{p}'    \t{reconhece(p)}")

testar_reconhece(["1e1", "2.2e3", "-2.2e3", "-2.2e-3", ".1e1", "1e"])
print('----------------------');
testar_reconhece(["11", "223", "223", "223", "1e"])


#print(f'{tt}')
#for estado in Q:
#	for simbolo in V:
#		print(f'{estado} -{simbolo}-> {tt[estado][simbolo]}')

# f" " string interpolation
#print(f"{'aba'} {reconhece('aba')}") # aba  True
#print(f'{reconhece("ba")}')  # False
#print(f'{reconhece("abac")}') # False
