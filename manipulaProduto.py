import manipulaCSV as mcsv
import apresentacao


def carregar() -> list:
    '''
    Carrega a lista de produtos do arquivo produto.csv

    Retorno
    -------
    Retorna uma lista de dicionários com os produtos lidos
    '''
    listaProdutos = mcsv.carregarDados("Produtos.csv")
    return listaProdutos


def cadastrar(listaProdutos: list) -> bool:
    apresentacao.limpaTela()
    prod = apresentacao.CadastrarProduto()
    listaProdutos.append(prod)
    campos = ["Id", "Setor", "Nome", "Preco", "Validade", "Quantidade"]
    return mcsv.gravarDados("Produtos.csv", campos, listaProdutos)

def editar(listaProdutos: list) -> bool:
    '''
    Permite editar um produto na lista de produtos e atualizar o arquivo CSV

    Parâmetros
    ----------
    listaProdutos: Lista atual dos produtos

    Retorno
    -------
    Retorna True se o produto foi editado com sucesso
    '''
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
                    novo_produto[campo] = novo_valor
                else:
                    novo_produto[campo] = valor_atual

            # Atualiza o produto na lista
            index_produto = listaProdutos.index(produto)
            listaProdutos[index_produto] = novo_produto

            # Grava os produtos atualizados no arquivo CSV
            campos = ["Id", "Setor", "Nome", "Preco", "Validade", "Quantidade"]
            return mcsv.gravarDados("Produtos.csv", campos, listaProdutos)

    if not produto_encontrado:
        print("Produto não encontrado.")
        return False
