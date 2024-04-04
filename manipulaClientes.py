import manipulaCSV as mcsv


def carregar() -> list:
    '''
    Carrega o arquivo de Cliente.csv numa lista

    Retorno
    -------
    Retorna uma lista vazia caso o arquivo não exista ou
    uma lista de dicionários contendo os dados dos clientes
    '''
    lista = mcsv.carregarDados("Cliente.csv")
    return lista


def cadastrar(listaClientes: list) -> bool:
    '''
    Rotina para cadastrar um cliente

    Parâmetros
    ----------
    listaClientes: Lista atual dos clientes

    Retorno
    -------
    Retorna True se o cliente foi cadastrado com sucesso
    '''
    camposCliente = ["CPF", "Nome", "Nascimento", "Idade", "Endereço", "Cidade", "Estado", "Pontos"]
    cliente = {}
    for campo in camposCliente:
        if (campo != 'Pontos'):
            cliente[campo] = input(f"{campo}:")
        else:
            cliente[campo] = 0

    listaClientes.append(cliente)
    print(listaClientes)
    return mcsv.gravarDados('Cliente.csv', camposCliente, listaClientes)


def excluir(listaClientes: list, cpf: str) -> bool:
    '''
    Excluir um cliente da lista de clientes e atualiza o arquivo CSV
    '''
    flag = False
    camposCliente = list(listaClientes[0].keys())
    for i, cliente in enumerate(listaClientes):
        if cliente['CPF'] == cpf:
            flag = True
            listaClientes.pop(i)
    # print(listaClientes)
    if flag:
        mcsv.gravarDados("Cliente.csv", camposCliente, listaClientes)
    return flag



