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

    # Adiciona pontos ao cliente
    adicionar_pontos_cliente(cliente, valor_total)

    # Obtém o último ID de venda registrado
    vendas = mcsv.carregarDados("Vendas.csv")
    ultimo_id_venda = 1 if not vendas else int(vendas[-1]['ID']) + 1

    # Registra os itens comprados
    registros_itens_compra = []
    for produto in compras:
        produto_vendido = produto.copy()
        quantidade_comprada = produto_vendido.pop('Quantidade')  # Remove a quantidade comprada do produto vendido
        produto_vendido['ID_Venda'] = str(ultimo_id_venda)
        produto_vendido['Data_Compra'] = data_atual
        # Adiciona cada item na lista conforme a quantidade comprada
        for _ in range(quantidade_comprada):
            registros_itens_compra.append(produto_vendido)

    # Adiciona os registros de itens de compra ao arquivo ItensCompra.csv sem sobrescrever o conteúdo existente
    mcsv.gravarDados("ItensCompra.csv", list(compras[0].keys()) + ['ID_Venda', 'Data_Compra', 'Quantidade'], registros_itens_compra, modo="a")

    # Registra a venda
    venda = {'ID': str(ultimo_id_venda), 'CPF_Cliente': cliente['CPF'], 'Nome_Cliente': cliente['Nome'],
             'Data_Compra': data_atual, 'Valor_Total': valor_total, 'Quantidade_Itens': len(registros_itens_compra)}  # Usamos a quantidade de registros de itens de compra
    mcsv.gravarDados("Vendas.csv", list(venda.keys()), [venda], modo="a")

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
    lista=mcli.carregar_cleinte()
    cliente = verificar_cliente(cpf)
    if cliente is None:
        print("Cliente não cadastrado.")
        if input("Deseja cadastrar o cliente? (S/N): ").upper() == 'S':
            mcli.cadastrar_Cliente(lista)
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

def adicionar_pontos_cliente(cliente, valor_compra):
    '''
    Adiciona pontos ao cliente com base no valor da compra.

    Parâmetros:
        cliente (dict): Dados do cliente.
        valor_compra (float): Valor total da compra.

    Retorno:
        None
    '''
    # Carregar os dados dos clientes
    clientes = mcsv.carregarDados("Cliente.csv")

    # Localizar o cliente pelo CPF
    cpf_cliente = cliente.get('CPF')  # Obtém o CPF do cliente
    cliente_encontrado = None
    for c in clientes:
        if c.get('CPF') == cpf_cliente:
            cliente_encontrado = c
            break

    # Verificar se o cliente foi encontrado
    if cliente_encontrado:
        # Calcular a quantidade de pontos a serem adicionados
        pontos_ganhos = int(valor_compra)  # Um ponto para cada 1 real gasto

        # Atualizar os pontos do cliente
        cliente_encontrado['Pontos'] = str(int(cliente_encontrado.get('Pontos', 0)) + pontos_ganhos)

        # Atualizar o arquivo de clientes com os novos pontos
        # Remover o cliente encontrado do arquivo
        clientes.remove(cliente_encontrado)
        # Adicionar o cliente atualizado
        clientes.append(cliente_encontrado)
        # Gravar os dados atualizados no arquivo
        mcsv.gravarDados("Cliente.csv", list(cliente_encontrado.keys()), clientes, modo="w")
    else:
        print("Cliente não encontrado.")


def imprimir_itens_mais_vendidos_ultimos_3_dias():
    vendas = carregar_vendas_ultimos_3_dias()

    # Contagem dos itens vendidos
    contagem_itens = {}
    for venda in vendas:
        nome_produto = venda['Nome']
        if nome_produto in contagem_itens:
            contagem_itens[nome_produto] += 1
        else:
            contagem_itens[nome_produto] = 1

    # Ordena os itens com base na contagem de vendas
    itens_mais_vendidos = sorted(contagem_itens.items(), key=lambda x: x[1], reverse=True)

    # Imprime os 5 itens mais vendidos
    print("=== 5 Itens Mais Vendidos nos Últimos 3 Dias ===")
    for i, (produto, quantidade) in enumerate(itens_mais_vendidos[:5], start=1):
        print(f"{i}. {produto}: {quantidade} unidades")

def carregar_vendas_ultimos_3_dias():
    vendas = []
    # Calcula a data de 3 dias atrás
    data_3_dias_atras = datetime.datetime.now() - datetime.timedelta(days=3)

    # Carrega os dados das vendas do arquivo ItensCompra.csv
    with open('ItensCompra.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for item in reader:
            if 'Data_Compra' in item:
                data_compra = datetime.datetime.strptime(item['Data_Compra'], '%Y-%m-%d %H:%M:%S')
                if data_compra >= data_3_dias_atras:
                    vendas.append(item)
    return vendas


def contar_quantidade_por_produto(vendas):
    quantidade_por_produto = {}
    for venda in vendas:
        id_venda = venda['ID']
        # Carrega os dados dos itens comprados para a venda atual
        with open('ItensCompra.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            itens_compra = [item for item in reader if item['ID_Venda'] == id_venda]
        for item in itens_compra:
            id_produto = item['Id']
            quantidade = int(item['Quantidade'])
            quantidade_por_produto[id_produto] = quantidade_por_produto.get(id_produto, 0) + quantidade
    return quantidade_por_produto

def classificar_produtos_por_quantidade(quantidade_por_produto):
    # Ordena os produtos com base na quantidade vendida
    produtos_mais_vendidos = sorted(quantidade_por_produto.items(), key=lambda x: x[1], reverse=True)
    return produtos_mais_vendidos

def imprimir_top_5(produtos_mais_vendidos):
    print("=== Top 5 Itens Mais Vendidos nos Últimos 3 Dias ===")
    for i, (id_produto, quantidade) in enumerate(produtos_mais_vendidos[:5], start=1):
        print(f"{i}. Produto ID: {id_produto}, Quantidade Vendida: {quantidade}")


def obter_informacoes_vendas_por_cpf(cpf: str) -> None:
    '''
    Obtém informações de vendas relacionadas a um CPF específico e imprime na tela.

    Parâmetros
    ----------
    cpf: CPF do cliente

    Retorno
    -------
    None
    '''
    with open('Vendas.csv', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        vendas_cliente = []

        for venda in reader:
            if venda['CPF_Cliente'] == cpf:
                vendas_cliente.append(venda)

        if vendas_cliente:
            print(f"Informações de vendas para o CPF {cpf}:")
            for venda in vendas_cliente:
                data_compra = venda['Data_Compra']
                valor_total = float(venda['Valor_Total'])
                quantidade_itens = int(venda['Quantidade_Itens'])
                print(f"Data da compra: {data_compra},\n Valor total: R${valor_total},\n Quantidade de itens: {quantidade_itens}")
        else:
            print("Não foram encontradas vendas para o CPF fornecido.")