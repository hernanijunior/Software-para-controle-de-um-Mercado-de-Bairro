import csv
import datetime
import manipulaCSV as mcsv
import manipulaClientes as mcli
import manipulaProduto as mprod
import apresentacao as apre

def verificar_cliente(cpf):
    '''
    Verifica se o cliente está cadastrado.

    Parâmetros:
        cpf (str): CPF do cliente.

    Retorno:
        dict or None: Retorna os dados do cliente se estiver cadastrado, None caso contrário.
    '''
    lista_clientes = mcli.carregar_cleinte()
    for cliente in lista_clientes:
        if cliente['CPF'] == cpf:
            return cliente
    return None

def obter_info_produto():
    '''
    Obtém as informações do produto e verifica a disponibilidade em estoque.

    Retorno:
        dict or None: Retorna os dados do produto se estiver disponível em estoque, None caso contrário.
    '''
    lista_produtos = mprod.carregar()
    apre.limpaTela()
    print("=== Produtos Disponíveis ===")
    apre.print_produtos(lista_produtos)
    id_produto = input("Digite o ID do produto que deseja comprar (ou '0' para encerrar a compra): ")
    if id_produto == '0':
        return None
    for produto in lista_produtos:
        if produto['Id'] == id_produto:
            quantidade_desejada = int(input("Digite a quantidade desejada: "))
            if quantidade_desejada <= int(produto['Quantidade']):
                produto['Quantidade'] = quantidade_desejada
                return produto
            else:
                print("Não há quantidade disponível para o produto.")
                return None
    print("Produto não encontrado.")
    return None

def registrar_venda(cliente, compras):
    '''
    Registra a venda e os itens comprados.

    Parâmetros:
        cliente (dict): Dados do cliente.
        compras (list): Lista de produtos comprados.

    Retorno:
        None
    '''
    # Obtém a data atual
    data_atual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Calcula o valor total da compra
    valor_total = calcular_valor_total(compras)

    # Obtém o último ID de venda registrado
    vendas = mcsv.carregarDados("Vendas.csv")
    ultimo_id_venda = 1 if not vendas else int(vendas[-1]['ID']) + 1

    # Registra a venda
    venda = {'ID': str(ultimo_id_venda), 'CPF_Cliente': cliente['CPF'], 'Nome_Cliente': cliente['Nome'], 'Data_Compra': data_atual, 'Valor_Total': valor_total}
    mcsv.gravarDados("Vendas.csv", list(venda.keys()), [venda])

    # Registra os itens comprados
    registros_itens_compra = []
    for produto in compras:
        produto_vendido = produto.copy()
        produto_vendido['ID_Venda'] = str(ultimo_id_venda)
        produto_vendido['Data_Compra'] = data_atual
        produto_vendido.pop('Quantidade')  # Remove a quantidade comprada do produto vendido
        registros_itens_compra.append(produto_vendido)

    # Adiciona os registros de itens de compra ao arquivo sem sobrescrever o conteúdo existente
    mcsv.gravarDados("ItensCompra.csv", list(compras[0].keys()) + ['ID_Venda', 'Data_Compra'], registros_itens_compra)

    # Atualiza o estoque
    atualizar_estoque(compras)

def calcular_valor_total(compras):
    '''
    Calcula o valor total da compra.

    Parâmetros:
        compras (list): Lista de produtos comprados.

    Retorno:
        float: Valor total da compra.
    '''
    valor_total = 0
    for produto in compras:
        valor_total += float(produto['Preco']) * int(produto['Quantidade'])
    return valor_total

def atualizar_estoque(compras):
    '''
    Atualiza o estoque dos produtos.

    Parâmetros:
        compras (list): Lista de produtos comprados.

    Retorno:
        None
    '''
    produtos = mprod.carregar()
    for produto in produtos:
        for compra in compras:
            if produto['Id'] == compra['Id']:
                produto['Quantidade'] = str(int(produto['Quantidade']) - int(compra['Quantidade']))
    mcsv.gravarDados("Produtos.csv", list(produtos[0].keys()), produtos)

def carrinho_de_compras(cpf):
    '''
    Implementa o carrinho de compras.

    Parâmetros:
        cpf (str): CPF do cliente.

    Retorno:
        None
    '''
    cliente = verificar_cliente(cpf)
    if cliente is None:
        print("Cliente não cadastrado.")
        if input("Deseja cadastrar o cliente? (S/N): ").upper() == 'S':
            mcli.cadastrar_Cliente([{'CPF': cpf}])  # Cadastra apenas com o CPF
            return

    compras = []
    while True:
        produto = obter_info_produto()
        if produto is None:
            break
        compras.append(produto)
        print("Produto adicionado ao carrinho.")

    if compras:
        # Registrar a venda e os itens comprados
        registrar_venda(cliente, compras)

        # Calcular e exibir o valor total da compra
        valor_total = calcular_valor_total(compras)
        print(f"Valor total da compra: R$ {valor_total:.2f}")
    else:
        print("Nenhum produto adicionado ao carrinho.")
