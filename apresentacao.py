from os import system, name
import csv
import manipulaCSV as mcsv
import manipulaProduto as mprod
import apresentacao as apre
import manipulaClientes as mcli

def limpaTela():
    '''
    Limpa a tela de acordo com o sistema operacional (Windows ou Linux)
    '''
    if name == 'nt':
        _ = system("cls")
    else:
        _ = system("clear")

def print_produtos(listaProdutos):
    '''
    Imprime a lista de produtos formatada
    '''
    print("{:<3} {:<10} {:<20} {:<7} {:<10} {:<10}".format("ID", "Setor", "Nome", "Preço", "Validade", "Quantidade"))
    print("-" * 60)  # Linha divisória
    for product in listaProdutos:
        print("{:<3} {:<10} {:<20} {:<7} {:<10} {:<10}".format(product["Id"], product["Setor"], product["Nome"], product["Preco"], product["Validade"], product["Quantidade"]))
    print()  # Linha em branco após a lista de produtos

def cadastrarProduto():
    '''
    Interface para cadastrar um novo produto
    '''
    limpaTela()
    print("=" * 30)
    print("Cadastro de um novo produto ")
    print("=" * 30)
    produto = {}
    produto['Id'] = input("Identificação do produto: ")
    produto['Setor'] = input("Setor do produto: ")
    produto['Nome'] = input("Nome do produto: ")
    produto['Preco'] = float(input("Preço do produto: "))
    produto['Validade'] = input("Data de validade do produto: ")
    produto['Quantidade'] = int(input("Quantidade de produto no estoque: "))
    print("=" * 30)
    return produto

def menu_produto():
    '''
    Exibe o menu relacionado aos produtos e executa a opção selecionada pelo usuário.
    '''
    while True:
        limpaTela()
        print("=== Menu Produto ===")
        print("1. Cadastrar Produto")
        print("2. Editar Produto")
        print("3. Excluir Produto")
        print("4. Verificar Estoque Baixo")
        print("5. Quantidade de estoque por setor")
        print("9. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            listaProdutos = mprod.carregar()
            print_produtos(listaProdutos)
            mprod.cadastrar_produto(listaProdutos)
        elif opcao == '2':
            listaProdutos = mprod.carregar()
            print_produtos(listaProdutos)
            mprod.editar_produto(listaProdutos)
        elif opcao == '3':
            listaProdutos = mprod.carregar()
            print_produtos(listaProdutos)
            mprod.excluir_produto(listaProdutos)
        elif opcao == '4':
            limite_estoque_baixo = int(input("Qual o limite de estoque que pode ser considerado baixo: "))
            mprod.verifica_estoque_baixo(limite_estoque_baixo)
        elif opcao == '5':
            limpaTela()
            mprod.calcular_estoque_por_setor()
        elif opcao == '9':
            print("Retornando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


def menu_clientes():
    '''
    Exibe o menu relacionado aos clientes e executa a opção selecionada pelo usuário.
    '''
    while True:
        limpaTela()
        print("=== Menu Clientes ===")
        print("1. Cadastrar Novo Cliente")
        print("2. Excluir Cliente")
        print("3. Atualizar Cliente")
        print("9. Voltar ao Menu Principal")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            listaClientes = mcli.carregar_cleinte()  # Corrigindo o nome da função
            mcli.cadastrar_Cliente(listaClientes)
        elif opcao == '2':
            listaClientes = mcli.carregar_cleinte()  # Corrigindo o nome da função
            cpf = input("Digite o CPF do cliente a ser excluído: ")
            mcli.excluir_Cliente(listaClientes, cpf)
        elif opcao == '3':
            mcli.editar_cliente()
        elif opcao == '9':
            print("Retornando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
