from os import system, name
import csv
import manipulaCSV as mcsv
import manipulaProduto as mprod
import apresentacao as apre
import manipulaProduto as mcli

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
    opcoes = [1, 2, 3, 4, 5, 9]
    opcao = 10
    while opcao not in opcoes:
        limpaTela()
        print("#" * 20)
        print("1. Venda\n2. Clientes\n3. Produto\n4. \n9. Sair")
        print('#' * 20)
        opcao = int(input("Opção -> "))
    return opcao


# Em main()

def menu_principal():
    '''
    Exibe o menu principal e executa a opção selecionada pelo usuário.
    '''
    while True:
        limpaTela()
        print("=== Menu Principal ===")
        print("1. Venda")
        print("2. Clientes")
        print("3. Produto")
        print("9. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == '1':
            # Implemente a lógica para a opção de venda
            print("Opção de venda selecionada.")
            input("Pressione Enter para continuar...")
        elif opcao == '2':
            # Implemente a lógica para a opção de clientes
            print("Opção de clientes selecionada.")
            input("Pressione Enter para continuar...")
        elif opcao == '3':
            print("Opção de produto selecionada.")
            apre.menu_produto()
        elif opcao == '9':
            print("Saindo...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")


if __name__ == "__main__":

    menu_principal()

