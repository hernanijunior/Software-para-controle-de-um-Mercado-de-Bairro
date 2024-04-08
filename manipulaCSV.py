import csv
import os

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
        with open(nomeArquivo, "r", encoding="utf-8") as arq:
            listaClientes = list(csv.DictReader(arq, delimiter=';'))
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
    False caso ocorra algum erro durante a gravação
    '''
    try:
        # Verifica se o arquivo já existe
        arquivo_existe = os.path.isfile(nomeArquivo)

        # Abrindo o arquivo a ser gravado com o modo especificado e a codificação UTF-8
        with open(nomeArquivo, modo, newline='', encoding='utf-8') as arq:
            meuCSV = csv.DictWriter(arq, fieldnames=campos, delimiter=';')

            # Se o arquivo não existir ou for criado, escreva o cabeçalho
            if modo == "w" or not arquivo_existe:
                meuCSV.writeheader()

            # Escreva os dados da lista
            for r in lista:
                meuCSV.writerow(r)
            arq.flush()

        return True
    except FileNotFoundError:
        print("erro na abertura do arquivo ", nomeArquivo)
        return False


