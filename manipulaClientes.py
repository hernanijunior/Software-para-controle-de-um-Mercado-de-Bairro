import manipulaCSV as mcsv
import apresentacao as apre


def carregar_cleinte() -> list:
    '''
    Carrega o arquivo de Cliente.csv numa lista

    Retorno
    -------
    Retorna uma lista vazia caso o arquivo não exista ou
    uma lista de dicionários contendo os dados dos clientes
    '''
    lista = mcsv.carregarDados("Cliente.csv")
    return lista


def cadastrar_Cliente(listaClientes: list) -> bool:
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


def excluir_Cliente(listaClientes: list, cpf: str) -> bool:
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

# Em manipulaClientes.py

# No arquivo manipulaClientes.py

def editar_cliente() -> bool:
    '''
    Permite editar um cliente na lista de clientes e atualizar o arquivo CSV

    Parâmetros
    ----------
    Nenhum

    Retorno
    -------
    Retorna True se o cliente foi editado com sucesso
    '''
    apre.limpaTela()
    listaClientes = carregar_cleinte()  # Corrigindo o nome da função
    cpf_cliente = input("Digite o CPF do cliente que deseja editar: ")
    campos = ["CPF", "Nome", "Nascimento", "Idade", "Endereço", "Cidade", "Estado", "Pontos"]

    # Verifica se o cliente está na lista
    cliente_encontrado = False
    for cliente in listaClientes:
        if cliente['CPF'] == cpf_cliente:
            cliente_encontrado = True
            print("Cliente encontrado:")
            print(cliente)
            print("-" * 30)

            # Solicita as novas informações do cliente
            print("Digite as novas informações do cliente (deixe em branco para manter o mesmo valor):")
            for campo, valor_atual in cliente.items():
                novo_valor = input(f"{campo} ({valor_atual}): ").strip()
                if novo_valor:
                    cliente[campo] = novo_valor


            # Grava os clientes atualizados no arquivo CSV

            if mcsv.gravarDados("Cliente.csv", campos, listaClientes):  # Verificando se a gravação foi bem-sucedida
                print("Cliente atualizado com sucesso.")
                return True
            else:
                print("Erro ao atualizar o cliente.")
                return False

    if not cliente_encontrado:
        print("Cliente não encontrado.")
        return False
