from os import system, name
import csv
import manipulaCSV as mcsv
import manipulaProduto as mprod
import apresentacao


def limpaTela():
    '''
    Limpa a tela de acordo com o sistema operacional (Windows ou Linux)
    '''
    if name == 'nt':
        _ = system("cls")
    else:
        _ = system("clear")


def MenuPrincipal() -> int:
    '''
    Exemplo de Menu principal para o sistema

    Retorno
    -------
    Retorna a opção escolhida
    '''
    opcoes = [1, 2, 3, 4, 9]
    opcao = 10
    while opcao not in opcoes:
        limpaTela()
        print("#" * 20)
        print("1. Venda\n2. Clientes\n3. Produto\n4. Editar Produto\n9. Sair")
        print('#' * 20)
        opcao = int(input("Opção -> "))
    return opcao


def main():
    listaProdutos = mprod.carregar()
    while True:
        opcao = MenuPrincipal()
        if opcao == 1:
            # Implemente a lógica para a opção de venda
            pass
        elif opcao == 2:
            # Implemente a lógica para a opção de clientes
            pass
        elif opcao == 3:
            mprod.cadastrar(listaProdutos)
        elif opcao == 4:
            mprod.editar(listaProdutos)
        elif opcao == 9:
            break


if __name__ == "__main__":
    main()
