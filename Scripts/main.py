import os
os.system('csl' if os.name == 'nt' else 'clear')

from funcoes import tratar_linha, carregar_dados_csv, agrupar_por_conteudo, linha_valida, calcular_interacoes_por_conteudo, calcular_media_visualizacao_por_conteudo, top_5_conteudos_mais_vistos, listar_comentarios_por_conteudo


print("Arquivo tratado salvo como interacoes_globo_tratado.csv")

linhas, fieldnames = carregar_dados_csv('./Arquivos/interacoes_globo_tratado.csv')
linhas_tratadas = [tratar_linha(linha) for linha in linhas]

# Agrupamento de conteudo
conteudos = agrupar_por_conteudo(linhas_tratadas, fieldnames)


# Cálculo de Métricas 1 - Total de Interações por Conteúdo
resultado1 = dict(calcular_interacoes_por_conteudo(linhas))

print('\nTotal de Interações por Conteúdo:')
for id_conteudo, info in resultado1.items(): 
    print(f"ID: {id_conteudo} | Nome: {info['nome_conteudo']} | Total de interações: {info['total']}")


# Cálculo de Métricas 2 - Contagem por Tipo de Interação para Cada Conteúdo



# Cálculo de Métricas 3 - Tempo Total de Visualização por Conteúdo




# Cálculo de Métricas 4 - Média de Tempo de Visualização por Conteúdo
resultado4 = calcular_media_visualizacao_por_conteudo(conteudos)
print('\nMédia de Tempo de Visualização por Conteúdo')
for id_conteudo, info in resultado4.items():
    print(f"ID: {id_conteudo} | Nome: {info['nome_conteudo']} | Média de tempo de visualização: {info['media_watch_duration']:.2f} segundos")

# Cálculo de Métricas 5 - Total de Interações por Conteúdo (Listagem de Comentários por Conteúdo)
resultado5 = listar_comentarios_por_conteudo(conteudos, id_conteudo)
print("\nTop 5 conteúdos com mais visualizações:\n")




# Cálculo de Métricas 6 - Listagem dos top-5 conteúdos com mais visualizações)
resultado6 = top_5_conteudos_mais_vistos(linhas)
print("\nTop 5 conteúdos com mais visualizações:\n")
for i, (id_conteudo, info) in enumerate(resultado6, start=1):
    print(f"{i}. ID: {id_conteudo} | Nome: {info['nome_conteudo']} | Visualizações: {info['total_views']}")