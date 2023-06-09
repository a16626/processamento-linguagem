import os
import sys

# Adiciona o caminho relativo da pasta helpers ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'helpers')))

# Importa a função lexer_input do módulo coinlexer
from helpers.coinlexer import lexer_input, return_products, lexer, ReadFile, moedeiro, troco, WriteFile

lexer_input(ReadFile("produtos.txt"))
lexer.token()
lexer_input(ReadFile("moedas.txt"))
lexer.token()

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
            print("-> Moedas3 aceites: c5, c20, c50, e1, e2")
            print("-> Para inserir dinheiro: QUANTIA + moedas. ex: QUANTIA c20, c50")
            print("-> Para escolher um produto: PRODUTO=nomeDoProduto. ex: PRODUTO=twix")
            print('-----------------------------------------------------------------------')


            #Inserir Moedas
            print("Insira a quantia:")

            user_string = input()

            if (user_string == "CANCELAR"):
                atual_user = 'ADMIN'
            else:
                chosen_product = lexer_input(user_string)

                while chosen_product["ERROR"] == 'error' or chosen_product["saldo"] <= 0:

                    if chosen_product["saldo"] <= 0:
                        print("Moeda invalida!")

                    user_string = input()
                    chosen_product = lexer_input(user_string)

                print (f'> Valor inserido: €{chosen_product["valor_inserido"]}0 (saldo:{chosen_product["saldo"]}0)')


                #Escolher Produto
                print("Escolha um produto:")

                user_string = input()
                chosen_product = lexer_input(user_string)

                while chosen_product["ERROR"] == "error":

                    print("Produto não encontrado!")
                    user_string = input()
                    chosen_product = lexer_input(user_string)

                #Se o valor inserido for menor que o valor do produto
                while (chosen_product["saldo"] < chosen_product["produto_preco"]):

                    #Inserir Moedas
                    print(f'> Quantia insuficiente. faltam: €{chosen_product["produto_preco"] - chosen_product["saldo"]}0')
                    user_string = input()
                    chosen_product = lexer_input(user_string)

                if (chosen_product["saldo"] > chosen_product["produto_preco"]):

                    #Retirar moedas do moedeiro
                    moedas = troco(chosen_product["saldo"]-chosen_product["produto_preco"])

                    print("> Troco: {:.2f}€".format(chosen_product["saldo"]-chosen_product["produto_preco"]))

                    for key, value in moedas.items():
                        print(f"{value} moeda de {key}")

                else:
                    user_comprou = True
            Menu = False
            print("Obrigado pela compra!")

    if (atual_user == 'ADMIN'):
        user_string = input()
        lexer_input(user_string)

        user_string = input()
        chosen_product = lexer_input(user_string)


        if chosen_product["admin"]:
            print("Produto adicionado com sucesso")
            for key, value in chosen_product["admin"].items():
                print(f"{key}: {value}")
        else:
            print("Produto não adicionado!ERROR!")


    WriteFile("moedas.txt")

    



