import csv
# Lê o CSV e retorna uma tupla: (lista de linhas como dicionários, lista de fieldnames).
def carregar_dados_csv(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        reader = csv.DictReader(arquivo)
        linhas = list(reader)
        fieldnames = reader.fieldnames
    return linhas, fieldnames
from collections import defaultdict

def calcular_interacoes_por_conteudo(linhas):
    interacoes_por_conteudo = defaultdict(int)

    for linha in linhas:
        if linha_valida(linha):  # Usa sua função já existente
            conteudo_id = linha.get('id_conteudo')
            if conteudo_id:
                interacoes_por_conteudo[conteudo_id] += 1

    return dict(interacoes_por_conteudo)

"""
Limpa e trata uma linha do CSV:
- Remove espaços extras dos campos de texto 'plataforma' e 'tipo_interacao'.
- Converte o campo 'watch_duration_seconds' para float ou None, conforme as regras:
    * Se o tipo de interação for de visualização, valores ausentes/vazios/não numéricos viram 0.
    * Para outros tipos de interação, valores ausentes/vazios/não numéricos viram 'não aplicável'.
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
    else: # Para qualquer tipo que não seja visualização, sempre atribui 'não aplicável'
        watch_duration = 'não aplicável'
        
    linha['plataforma'] = plataforma
    linha['tipo_interacao'] = tipo_interacao
    linha['watch_duration_seconds'] = watch_duration

    # Remove qualquer chave None que possa ter sido criada por erro de leitura do CSV
    if None in linha:
        del linha[None]
    return linha

"""
Verifica se a linha é válida para processamento.
Uma linha é considerada válida se os campos 'plataforma' e 'tipo_interacao'
não estão vazios após a remoção de espaços extras.
"""
def linha_valida(linha):
    return linha.get('plataforma', '').strip() != '' and linha.get('tipo_interacao', '').strip() != ''

"""
Remove do dicionário qualquer chave que seja None ou que não esteja em fieldnames.
Isso garante que apenas as colunas corretas serão escritas no CSV final.
"""
def limpar_none_keys(linha, fieldnames):
    return {k: v for k, v in linha.items() if k in fieldnames and k is not None}