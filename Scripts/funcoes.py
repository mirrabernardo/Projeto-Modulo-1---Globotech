import csv
from collections import defaultdict

# FUNÇÃO 1 -  CARREGAR CSV (Lê o CSV e retorna uma tupla: (lista de linhas como dicionários, lista de fieldnames)).
def carregar_dados_csv(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        reader = csv.DictReader(arquivo)
        linhas = list(reader)
        fieldnames = reader.fieldnames
    return linhas, fieldnames


# FUNÇÃO 2 - Tratamento (Limpa e trata linha do CSV)
"""
- Remove espaços extras dos campos de texto 'plataforma' e 'tipo_interacao'.
- Converte o campo 'watch_duration_seconds' para float ou None, conforme as regras: (Se o tipo de interação for de visualização, valores ausentes/vazios/não numéricos viram 0; Para outros tipos de interação, valores ausentes/vazios/não numéricos viram None)
- Remove qualquer chave None do dicionário (caso tenha sido criada por erro de leitura).
"""
def tratar_linha(linha):
    tipos_visualizacao = ['view_start', 'play'] # Lista dos tipos de interação que indicam consumo de vídeo
    plataforma = linha.get('plataforma', '').strip()
    tipo_interacao = linha.get('tipo_interacao', '').strip()
    valor = linha.get('watch_duration_seconds', None)
    tipo_lower = tipo_interacao.lower()

    if tipo_lower in tipos_visualizacao: # Para interações de visualização, valores ausentes/vazios/não numéricos viram 0
        valor = linha.get('watch_duration_seconds', None)
        if valor is None or valor.strip() == '':
            watch_duration = 0
        else:
            try:
                watch_duration = float(valor.strip())
            except (ValueError, TypeError):
                watch_duration = 0
    else: # Para qualquer tipo que não seja visualização, sempre atribui None
        watch_duration = None
        
    linha['plataforma'] = plataforma
    linha['tipo_interacao'] = tipo_interacao
    linha['watch_duration_seconds'] = watch_duration

    # Remove qualquer chave None que possa ter sido criada por erro de leitura do CSV
    if None in linha:
        del linha[None]
    return linha


# FUNÇÃO 3 - Validação (Verifica se a linha é válida para processamento)
"""
Uma linha é considerada válida se os campos 'plataforma' e 'tipo_interacao'
não estão vazios após a remoção de espaços extras.
"""
def linha_valida(linha):
    return linha.get('plataforma', '').strip() != '' and linha.get('tipo_interacao', '').strip() != ''


# FUNÇÃO 4 - Limpeza de chaves inválidas
"""
Remove do dicionário qualquer chave que seja None ou que não esteja em fieldnames.
Isso garante que apenas as colunas corretas serão escritas no CSV final.
"""
def limpar_none_keys(linha, fieldnames):
    return {k: v for k, v in linha.items() if k in fieldnames and k is not None}


# FUNÇÃO 5 - Estruturação (agrupa as interações por id_conteudo)
def agrupar_por_conteudo(linhas, fieldnames):
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
    return conteudos


# FUNÇÃO 6 - Cálculo de Métricas (Total de Interações por Conteúdo)
"""
Para cada id_conteudo (e seu respectivo nome_conteudo), calcula o número total de interações dos tipos 'like', 'share', 'comment'.)
"""
def calcular_interacoes_por_conteudo(linhas):
    interacoes_por_conteudo = defaultdict(int)
    for linha in linhas:
        if linha_valida(linha):  # Usa função já existente
            conteudo_id = linha.get('id_conteudo')
            if conteudo_id:
                interacoes_por_conteudo[conteudo_id] += 1

    return dict(interacoes_por_conteudo)


# FUNÇÃO 7 - Cálculo de Métricas (Contagem por Tipo de Interação para Cada Conteúdo)
"""
Para cada id_conteudo (e nome_conteudo), contar quantas vezes cada tipo_interacao ocorreu (ex: Conteúdo X teve 50 'likes', 10 'shares', 5 'comments').
"""


# FUNÇÃO 8 - Cálculo de Métricas (Tempo Total de Visualização por Conteúdo)
"""
Para cada id_conteudo (e nome_conteudo), calcular a soma total de watch_duration_seconds.
"""


# FUNÇÃO 9 - Cálculo de Métricas (Média de Tempo de Visualização por Conteúdo)
"""
Para cada id_conteudo (e nome_conteudo), calcular a média de watch_duration_seconds. Atenção: Considerar apenas as interações onde watch_duration_seconds for maior que 0 para este cálculo.
"""


# FUNÇÃO 10 - Cálculo de Métricas (Total de Interações por Conteúdo (Listagem de Comentários por Conteúdo)
"""
Criar uma função que, dado um id_conteudo, retorne (ou imprima de forma organizada) todos os comment_text associados a ele.
"""


# FUNÇÃO 11 - Cálculo de Métricas (Listagem dos top-5 conteúdos com mais visualizações)
"""
Criar uma função que retorne (ou imprima de forma organizada) os top-5 conteúdos com mais visualizações.
"""