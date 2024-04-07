import csv


def carregarDados(nomeArquivo: str) -> list:
    ''' Carrega do arquivo CSV uma lista de informações, com cada item
    da lista sendo um dicionário

    Parâmetros
    ----------
    nomeArquivo: nome do arquivo que contém os dados que se deseja carregar

    Retorno
    -------
    Retorna uma lista vazia caso o arquivo não exista ou
    uma lista de dicionários contendo os dados do arquivo CSV que se deseja carregar
    '''
    try:
        arq = open(nomeArquivo, "r")
        listaClientes = csv.DictReader(arq, delimiter=';')
        listaClientes = list(listaClientes)
    except FileNotFoundError:
        print("Arquivo não encontrado ", nomeArquivo)
        return []
    return listaClientes


########################################################

def gravarDados(nomeArquivo: str, campos: list, lista: list, modo: str = "w") -> bool:
    '''Grava a informação da lista em um arquivo CSV

    Parâmetros
    ----------
    nomeArquivo: nome do arquivo que contém os dados dos clientes
    campos: campos do header arquivo CSV
    lista: lista com os dados a serem gravados
    modo: modo de abertura do arquivo ("w" para escrita, "a" para adição)

    Retorno
    -------
    Retorna True caso tenha sucesso ao gravar o cliente e
    false caso ocorra algum erro durante a gravação
    '''
    try:
        # abrindo o arquivo a ser gravado com o modo especificado
        with open(nomeArquivo, modo, newline='') as arq:
            meuCSV = csv.DictWriter(arq, fieldnames=campos, delimiter=';')
            if modo == "w":
                meuCSV.writeheader()
            for r in lista:
                meuCSV.writerow(r)
                print(r)
            arq.flush()
        return True
    except FileNotFoundError:
        print("erro na abertura do arquivo ", nomeArquivo)
        return False

