import os
os.system('cls' if os.name == 'nt' else 'clear')
from funcoes import (carregar_dados_csv, 
                     tratar_e_salvar_csv, 
                     agrupar_por_conteudo, 
                     tratar_linha, 
                     calcular_interacoes_por_conteudo, 
                     contar_tipos_interacao_por_conteudo, 
                     calcular_media_visualizacao_por_conteudo, 
                     listar_comentarios_por_conteudo, 
                     top_5_conteudos_mais_vistos, 
                     contar_tempo_total_de_visualizacao_por_conteudo)

# Carrega os nomes das colunas do arquivo original
_, fieldnames = carregar_dados_csv('interacoes_globo.csv')

# Trata e salva o arquivo tratado
print('\n' + '='*60)
print('TRATAMENTO DO ARQUIVO'.center(60))
print('='*60)
tratar_e_salvar_csv('interacoes_globo.csv', 'interacoes_globo_tratado.csv', fieldnames)
print("Arquivo tratado salvo como: interacoes_globo_tratado.csv\n")

linhas, fieldnames = carregar_dados_csv('interacoes_globo_tratado.csv')
linhas_tratadas = [tratar_linha(linha) for linha in linhas]

# Agrupa o conteúdo
print('\n' + '='*60)
print('AGRUPAMENTO DE CONTEÚDO'.center(60))
print('='*60)
conteudos = agrupar_por_conteudo(linhas_tratadas, fieldnames)
print("Conteúdo agrupado com sucesso!\n")

# Cálculo de Métricas 1 - Total de Interações por Conteúdo
print('\n' + '='*60)
print('TOTAL DE INTERAÇÕES POR CONTEÚDO'.center(60))
print('='*60)
resultado1 = dict(calcular_interacoes_por_conteudo(linhas_tratadas))
for id_conteudo, info in resultado1.items(): 
    print(f"ID: {id_conteudo} | Nome: {info['nome_conteudo']} | Total de interações: {info['total']}")


# Cálculo de Métricas 2 - Contagem por Tipo de Interação para Cada Conteúdo
print('\n' + '='*60)
print('CONTAGEM POR TIPO DE INTERAÇÃO'.center(60))
print('='*60)
resultado2 = contar_tipos_interacao_por_conteudo(linhas_tratadas)
for id_conteudo, info in resultado2.items():
    print(f"ID: {id_conteudo} | Nome: {info['nome_conteudo']}")
    for tipo, total in info['interacoes'].items():
        print(f"  {tipo}: {total}")
    print()  # Linha em branco entre conteúdos


# Cálculo de Métricas 3 - Tempo Total de Visualização por Conteúdo
#resultado3 = tempo_total_visualizacao_por_conteudo(conteudos)
print('\n' + '='*60)
print('TEMPO TOTAL DE VISUALIZAÇÃO POR CONTEÚDO'.center(60))
print('='*60)
resultado3 = contar_tempo_total_de_visualizacao_por_conteudo(linhas_tratadas)
for id_conteudo, info in resultado3.items():
    print(f"ID: {id_conteudo} | Nome: {info['nome']}")
    print(f"  Tempo total de visualização (minutos): {(info['watch_duration_seconds']/60):.2f}")
    print()  # Linha em branco entre conteúdos

# Cálculo de Métricas 4 - Média de Tempo de Visualização por Conteúdo
print('\n' + '='*60)
print('MÉDIA DE TEMPO DE VISUALIZAÇÃO POR CONTEÚDO'.center(60))
print('='*60)
resultado4 = calcular_media_visualizacao_por_conteudo(conteudos)
for id_conteudo, info in resultado4.items():
    print(f"ID: {id_conteudo} | Nome: {info['nome_conteudo']} | Média de tempo de visualização: {(info['media_watch_duration']/60):.2f} minutos")


# Cálculo de Métricas 5 - Total de Interações por Conteúdo (Listagem de Comentários por Conteúdo)
print('\n' + '='*60)
print('COMENTÁRIOS POR CONTEÚDO'.center(60))
print('='*60)
for id_conteudo, conteudo in conteudos.items():
    comentarios = listar_comentarios_por_conteudo(conteudos, id_conteudo)
    nome_conteudo = conteudo.get('nome_conteudo', 'Desconhecido')
    print(f"ID: {id_conteudo} | Nome: {nome_conteudo}")
    if comentarios:
        for i, comentario in enumerate(comentarios, start=1):
            print(f"  {i}. {comentario}")
    else:
        print("  Nenhum comentário encontrado.")
    print()  # Linha em branco entre conteúdos


# Cálculo de Métricas 6 - Listagem dos top-5 conteúdos com mais visualizações)
print('\n' + '='*60)
print('TOP 5 CONTEÚDOS COM MAIS VISUALIZAÇÕES'.center(60))
print('='*60)
resultado6 = top_5_conteudos_mais_vistos(linhas_tratadas)
for i, (id_conteudo, info) in enumerate(resultado6, start=1):
    print(f"{i}. ID: {id_conteudo} | Nome: {info['nome_conteudo']} | Visualizações: {info['total_views']}")
