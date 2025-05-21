from funcoes import tratar_linha, carregar_dados_csv, agrupar_por_conteudo, linha_valida
from collections import defaultdict

linhas, fieldnames = carregar_dados_csv('./Arquivos/interacoes_globo_tratado.csv')
linhas_tratadas = [tratar_linha(linha) for linha in linhas]
conteudos = agrupar_por_conteudo(linhas_tratadas, fieldnames)

# Agrupamento de conteudo
conteudos = {}
for linha in linhas:
    id_conteudo = linha['id_conteudo']
    nome_conteudo = linha['nome_conteudo']
    interacao = {campo: linha[campo] for campo in fieldnames if campo not in ('id_conteudo', 'nome_conteudo')}
    if id_conteudo not in conteudos:
        conteudos[id_conteudo] = {
            'nome_conteudo': nome_conteudo,
            'interacoes': []
        }
    conteudos[id_conteudo]['interacoes'].append(interacao)


# Cálculo de Métricas 1 - Total de Interações por Conteúdo
"""
Para cada id_conteudo (e seu respectivo nome_conteudo), calcular o número total de interações dos tipos 'like', 'share', 'comment'.
"""
interacoes_por_conteudo = defaultdict(int)

for linha in linhas:
    if linha_valida(linha):  # Usa função já existente
        conteudo_id = linha.get('id_conteudo')
        if conteudo_id:
            interacoes_por_conteudo[conteudo_id] += 1

resultado = dict(interacoes_por_conteudo)
print(resultado)


# Cálculo de Métricas 2 - Contagem por Tipo de Interação para Cada Conteúdo
"""
Para cada id_conteudo (e nome_conteudo), contar quantas vezes cada tipo_interacao ocorreu (ex: Conteúdo X teve 50 'likes', 10 'shares', 5 'comments').
"""


# Cálculo de Métricas 3 - Tempo Total de Visualização por Conteúdo
"""
Para cada id_conteudo (e nome_conteudo), calcular a soma total de watch_duration_seconds.
"""


# Cálculo de Métricas 4 - Média de Tempo de Visualização por Conteúdo
"""
Para cada id_conteudo (e nome_conteudo), calcular a média de watch_duration_seconds. Atenção: Considerar apenas as interações onde watch_duration_seconds for maior que 0 para este cálculo.
"""
for id_conteudo, info in conteudos.items():
    duracoes = [
        interacao.get('watch_duration_seconds')
        for interacao in info['interacoes']
        if isinstance(interacao.get('watch_duration_seconds'), (int, float)) and interacao.get('watch_duration_seconds') > 0
    ]
    if duracoes:
        media = sum(duracoes) / len(duracoes)
    else:
        media = 0
    print(f"ID: {id_conteudo} | Nome: {info['nome_conteudo']} | Média de tempo de visualização: {media:.2f} segundos")

# Cálculo de Métricas 5 - Total de Interações por Conteúdo (Listagem de Comentários por Conteúdo)
"""
Criar uma função que, dado um id_conteudo, retorne (ou imprima de forma organizada) todos os comment_text associados a ele.
"""


# Cálculo de Métricas 6 - Listagem dos top-5 conteúdos com mais visualizações)
"""
Criar uma função que retorne (ou imprima de forma organizada) os top-5 conteúdos com mais visualizações.
"""
