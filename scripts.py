import csv

with open('interacoes_globo.csv', 'r', newline='', encoding='utf-8') as arquivo:
    leitor = csv.reader(arquivo)
    linhas = list(leitor)

cabecalho = linhas[0]
dados = linhas[1:]

