import csv
from funcoes import tratar_linha, linha_valida, limpar_none_keys

with open('interacoes_globo.csv', 'r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    linhas = list(reader)
    fieldnames = reader.fieldnames

linhas_filtradas = filter(linha_valida, linhas)
linhas_tratadas = map(tratar_linha, linhas_filtradas)

with open('interacoes_globo_tratado.csv', 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for linha in linhas_tratadas:
        linha_limpa = limpar_none_keys(linha, fieldnames)
        writer.writerow(linha_limpa)

print("Arquivo tratado salvo como interacoes_globo_tratado.csv")