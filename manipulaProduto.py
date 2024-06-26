import manipulaCSV as mcsv
import apresentacao
import csv
from datetime import datetime


def carregar() -> list:
    '''
    Carrega a lista de produtos do arquivo produto.csv

    Retorno
    -------
    Retorna uma lista de dicionários com os produtos lidos
    '''
    listaProdutos = mcsv.carregarDados("Produtos.csv")
    return listaProdutos


def cadastrar_produto(listaProdutos: list) -> bool:
    apresentacao.limpaTela()
    prod = apresentacao.cadastrarProduto()
    listaProdutos.append(prod)
    campos = ["Id", "Setor", "Nome", "Preco", "Validade", "Quantidade"]
    return mcsv.gravarDados("Produtos.csv", campos, listaProdutos)

# Dentro de manipulaProduto.py

def editar_produto(listaProdutos: list) -> None:
    """
    Permite editar um produto na lista de produtos e atualizar o arquivo CSV.

    Parâmetros:
        lista_produtos (list): Lista atual dos produtos.

    Retorno:
        None
    """
    apresentacao.limpaTela()
    id_produto = input("Digite o ID do produto que deseja editar: ")

    # Verifica se o produto está na lista
    produto_encontrado = False
    for produto in listaProdutos:
        if produto['Id'] == id_produto:
            produto_encontrado = True
            print("Produto encontrado:")
            print(produto)
            print("-" * 30)

            # Solicita as novas informações do produto
            print("Digite as novas informações do produto (deixe em branco para manter o mesmo valor):")
            novo_produto = {}
            for campo, valor_atual in produto.items():
                novo_valor = input(f"{campo} ({valor_atual}): ").strip()
                if novo_valor:
                    # Se o campo for 'Setor', verifique se o novo setor fornecido está na lista de setores válidos
                    if campo == 'Setor':
                        setores_validos = ["Bebidas", "Frios", "Produtos de Limpeza", "Higiene Pessoal", "Padaria", "Frutas e Verduras", "Congelados"]

                        while novo_valor not in setores_validos:
                            print("Setor inválido. Os setores válidos são:", setores_validos)
                            novo_valor = input(f"{campo} ({valor_atual}): ").strip()
                        novo_produto[campo] = novo_valor
                    else:
                        novo_produto[campo] = novo_valor
                else:
                    novo_produto[campo] = valor_atual

            # Atualiza o produto na lista
            index_produto = listaProdutos.index(produto)
            listaProdutos[index_produto] = novo_produto

            # Grava os produtos atualizados no arquivo CSV
            campos = ["Id", "Setor", "Nome", "Preco", "Validade", "Quantidade"]
            mcsv.gravarDados("Produtos.csv", campos, listaProdutos)

            print("Produto editado com sucesso.")
            break

    if not produto_encontrado:
        print("Produto não encontrado.")




def excluir_produto(listaProdutos: list) -> bool:
    '''
    Exclui um produto da lista de produtos e atualiza o arquivo CSV

    Parâmetros
    ----------
    listaProdutos: Lista atual dos produtos

    Retorno
    -------
    Retorna True se o produto foi excluído com sucesso
    '''
    apresentacao.limpaTela()
    id_produto = input("Digite o ID do produto que deseja excluir: ")

    # Verifica se o produto está na lista
    produto_encontrado = False
    for produto in listaProdutos:
        if produto['Id'] == id_produto:
            produto_encontrado = True
            print("Produto encontrado:")
            print(produto)
            print("-" * 30)

            # Confirmação da exclusão
            confirmacao = input("Tem certeza que deseja excluir este produto? (S/N): ").strip().upper()
            if confirmacao == "S":
                # Remove o produto da lista
                listaProdutos.remove(produto)

                # Grava os produtos atualizados no arquivo CSV
                campos = ["Id", "Setor", "Nome", "Preco", "Validade", "Quantidade"]
                return mcsv.gravarDados("Produtos.csv", campos, listaProdutos)

    if not produto_encontrado:
        print("Produto não encontrado.")
        return False

def verifica_estoque_baixo(limite_estoque_baixo: int) -> list:
    '''
    Carrega a lista de produtos do arquivo Produtos.csv e verifica se há produtos com estoque baixo.

    Parâmetros
    ----------
    limite_estoque_baixo: Limite inferior para considerar um estoque baixo

    Retorno
    -------
    Retorna uma lista de dicionários com os produtos lidos.
    '''
    listaProdutos = mcsv.carregarDados("Produtos.csv")
    produtos_estoque_baixo = []

    for produto in listaProdutos:
        if int(produto['Quantidade']) < limite_estoque_baixo:
            produtos_estoque_baixo.append(produto)

    if produtos_estoque_baixo:
        print("Os seguintes produtos estão com estoque baixo:")
        for produto in produtos_estoque_baixo:
            print(f"ID: {produto['Id']}, Setor: {produto['Setor']}, Nome: {produto['Nome']}, Preço: R${produto['Preco']}, Validade: {produto['Validade']}, Quantidade: {produto['Quantidade']}")
    else:
        print("Nenhum produto está com estoque baixo.")

    return listaProdutos

verifica_estoque_baixo(10)


def calcular_estoque_por_setor():
    '''
    Calcula a quantidade total de estoque por setor no arquivo Produtos.csv e imprime na tela.
    '''
    # Dicionário para armazenar a quantidade de estoque por setor
    estoque_por_setor = {}

    # Abre o arquivo Produtos.csv e lê os dados
    with open('Produtos.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            setor = row['Setor']
            quantidade = int(row['Quantidade'])
            # Se o setor já estiver no dicionário, adiciona a quantidade de estoque
            if setor in estoque_por_setor:
                estoque_por_setor[setor] += quantidade
            # Caso contrário, cria uma nova entrada no dicionário com a quantidade de estoque
            else:
                estoque_por_setor[setor] = quantidade

    # Imprime a quantidade de estoque por setor
    print("Quantidade de estoque por setor:")
    for setor, estoque in estoque_por_setor.items():
        print(f"{setor}: {estoque}")

def verificar_e_imprimir_produtos_vencidos():
        '''
        Verifica e imprime na tela os produtos vencidos a partir do arquivo CSV fornecido.

        Parâmetros:
            nome_arquivo (str): O nome do arquivo CSV contendo os dados dos produtos.

        Retorno:
            None
        '''
        produtos = mcsv.carregarDados("Produtos.csv")

        # Obtém a data atual
        data_atual = datetime.now()

        # Verifica a validade de cada produto e imprime os vencidos
        produtos_vencidos = False
        for produto in produtos:
            validade = datetime.strptime(produto['Validade'], '%d/%m/%Y')
            if validade < data_atual:
                produtos_vencidos = True
                print("Produto Vencido:")
                print("ID:", produto['Id'])
                print("Setor:", produto['Setor'])
                print("Nome:", produto['Nome'])
                print("Preço:", produto['Preco'])
                print("Validade:", produto['Validade'])
                print("Quantidade:", produto['Quantidade'])
                print()

        if not produtos_vencidos:
            print("Não há produtos vencidos.")