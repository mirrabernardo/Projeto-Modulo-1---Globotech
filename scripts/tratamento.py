import csv
from funcoes import carregar_dados_csv, tratar_linha, linha_valida, limpar_none_keys

linhas, fieldnames = carregar_dados_csv('./arquivos/interacoes_globo.csv')

linhas_filtradas = filter(linha_valida, linhas)
linhas_tratadas = map(tratar_linha, linhas_filtradas)

with open('./arquivos/interacoes_globo_tratado.csv', 'w', encoding='utf-8', newline='') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for linha in linhas_tratadas:
        linha_limpa = limpar_none_keys(linha, fieldnames)
        writer.writerow(linha_limpa)

print("Arquivo tratado salvo como interacoes_globo_tratado.csv")