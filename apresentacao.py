from os import system, name


#################################################################
def limpaTela():
    '''
    Limpa a tela de acordo com o systema operacional (Windows ou Linux)
    '''
    if name == 'nt':
        _ = system("cls")
    else:
        _ = system("clear")


#################################################################

def MenuPrincipal() -> str:
    '''
    Exemplo de Menu principal para o sistema

    Retorno
    -------
    Retorna válida escolhida

    '''
    opcoes = [1, 2, 3, 9]
    opcao = 10
    while opcao not in opcoes:
        limpaTela()
        print("#" * 20)
        print("1.Venda\n2.Clientes\n3.Produto\n9.Sair")
        print('#' * 20)
        opcao = int(input("Opção -> "))
    return opcao


#################################################################

def CadastrarProduto() -> dict:
    '''
    Exibe uma interface para ler os dados de um produto

    Retorno
    -------
    Retorno um dicionário com os campos e dados de um produto
    '''
    produto = {}
    print("=" * 30)
    print("Cadastro de um novo produto ")
    print("=" * 30)
    produto['Id'] = input("Identificação do produto: ")
    print("-" * 30)
    produto['Setor'] = input("Setor do produto: ")
    print("-" * 30)
    produto['Nome'] = input("Nome do produto: ")
    print("-" * 30)
    produto['Preco'] = float(input("Preço do produto: "))
    print("-" * 30)
    produto['Validade'] = input("Data de validade do produto: ")
    print("-" * 30)
    produto['Quantidade'] = int(input("Quantidade de produto no estoque: "))
    print("=" * 30)
    return produto

