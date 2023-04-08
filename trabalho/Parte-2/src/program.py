import os
import sys

# Adiciona o caminho relativo da pasta helpers ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'helpers')))

# Importa a função lexer_input do módulo coinlexer
from helpers.coinlexer import lexer_input, return_products

#Variaveis para interação com menu
atual_user = 'USER'
Menu = True
user_string = None
user_comprou = False

chosen_product = None

while Menu == True:

    if (atual_user == 'USER' and user_comprou == False):

        #Imprimir produtos
        if (user_string == None):
            print('----Produtos-----------------------------------------------------------')
            for product in return_products():
                print(f'Nome: {product["nome"]} | Preço: {product["preco"]} | Stock: {product["stock"]}')

            print('-----------------------------------------------------------------------')
            print("-> Moedas aceites: c5, c20, c50, e1, e2")
            print("-> Para inserir dinheiro: QUANTIA + moedas. ex: QUANTIA c20, c50")
            print("-> Para escolher um produto: PRODUTO=nomeDoProduto. ex: PRODUTO=twix")
            print('-----------------------------------------------------------------------')

            #Inserir Moedas
            user_string = input()
            chosen_product = lexer_input(user_string)

            print (f'> Valor inserido: €{chosen_product["valor_inserido"]} (saldo: {chosen_product["saldo"]})')

            #Escolher Produto
            print("Escolha um produto:")

            user_string = input()
            chosen_product = lexer_input(user_string)

            #Se o valor inserido for menor que o valor do produto
            while (chosen_product["saldo"] < chosen_product["produto_preco"]):

                #Inserir Moedas
                print(f'> Quantia insuficiente. faltam: €{chosen_product["produto_preco"] - chosen_product["saldo"]}')
                user_string = input()
                chosen_product = lexer_input(user_string)

            if (chosen_product["saldo"] > chosen_product["produto_preco"]):
                print(f'> Troco: €{chosen_product["saldo"] - chosen_product["produto_preco"]}')
                user_comprou = True
            else:
                user_comprou = True
        Menu = False

print("Obrigado pela compra!")

