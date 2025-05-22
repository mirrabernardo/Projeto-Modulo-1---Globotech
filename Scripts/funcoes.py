import csv
from collections import defaultdict

# FUNÇÃO 0 -  Carregar CSV (Lê o CSV e retorna uma tupla: (lista de linhas como dicionários, lista de fieldnames)).
def carregar_dados_csv(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as arquivo:
        reader = csv.DictReader(arquivo)
        linhas = list(reader)
        fieldnames = reader.fieldnames
    return linhas, fieldnames


# =========================
# VALIDAÇÃO E LIMPEZA DOS DADOS (ITEM 3.2)
# =========================

# FUNÇÃO 1.1 - Tratar e salvar CSV (Carrega, trata e salva o CSV tratado)
def tratar_e_salvar_csv(input_path, output_path, fieldnames):
    linhas, _ = carregar_dados_csv(input_path)
    linhas_filtradas = filter(linha_valida, linhas)
    linhas_tratadas = map(tratar_linha, linhas_filtradas)

    with open(output_path, 'w', encoding='utf-8', newline='') as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()
        for linha in linhas_tratadas:
            linha_limpa = limpar_none_keys(linha, fieldnames)
            writer.writerow(linha_limpa)


# FUNÇÃO 1.2 - Tratamento (Limpa e trata linha do CSV)
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
        try:
            if valor is None or valor.strip() == '':
                watch_duration = 0
            else:
                watch_duration = float(valor.strip())
        except (ValueError, TypeError): # Se não for possível converter para float, atribui 0
            watch_duration = 0
        finally: # Garante que o campo será atualizado, independentemente de erro ou não
            linha['watch_duration_seconds'] = watch_duration
    else: # Para qualquer tipo que não seja visualização, sempre atribui None
        watch_duration = None
        linha['watch_duration_seconds'] = watch_duration

    # Remove espaços extras dos campos de texto
    linha['plataforma'] = plataforma
    linha['tipo_interacao'] = tipo_interacao

    # Remove qualquer chave None que possa ter sido criada por erro de leitura do CSV
    if None in linha:
        del linha[None]
    return linha


# FUNÇÃO 1.3 - Validação (Verifica se a linha é válida para processamento)
"""
Uma linha é considerada válida se os campos 'plataforma' e 'tipo_interacao'
não estão vazios após a remoção de espaços extras.
"""
def linha_valida(linha):
    return linha.get('plataforma', '').strip() != '' and linha.get('tipo_interacao', '').strip() != ''


# FUNÇÃO 1.4 - Limpeza de chaves inválidas
"""
Remove do dicionário qualquer chave que seja None ou que não esteja em fieldnames.
Isso garante que apenas as colunas corretas serão escritas no CSV final.
"""
def limpar_none_keys(linha, fieldnames):
    return {k: v for k, v in linha.items() if k in fieldnames and k is not None}


# =========================
# ESTRUTURAÇÃO DOS DADOS (ITEM 3.3)
# =========================

# FUNÇÃO 2.1 - Estruturação (agrupa as interações por id_conteudo)
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


# =========================
# CÁLCULO DE MÉTRICAS SIMPLES (ITEM 3.4)
# =========================

# FUNÇÃO 3.1 - Cálculo de Métricas (Total de Interações por Conteúdo)
"""
Para cada id_conteudo (e seu respectivo nome_conteudo), calcula o número total de interações dos tipos 'like', 'share', 'comment'.)

def calcular_interacoes_por_conteudo(linhas):
    interacoes_por_conteudo = defaultdict(int)
    for linha in linhas:
        if linha_valida(linha):  # Usa função já existente
            conteudo_id = linha.get('id_conteudo')
            if conteudo_id:
                interacoes_por_conteudo[conteudo_id] += 1

    return dict(interacoes_por_conteudo)
"""
def calcular_interacoes_por_conteudo(linhas):
    interacoes_por_conteudo = defaultdict(lambda: {'nome_conteudo': '', 'total': 0})
    for linha in linhas:
        if linha_valida(linha):  # Usa função já existente
            conteudo_id = linha.get('id_conteudo')
            conteudo_nome = linha.get('nome_conteudo')
            if conteudo_id:
                interacoes_por_conteudo[conteudo_id]['nome_conteudo'] = conteudo_nome
                interacoes_por_conteudo[conteudo_id]['total'] += 1

    return dict(interacoes_por_conteudo)


# FUNÇÃO 3.2 - Cálculo de Métricas (Contagem por Tipo de Interação para Cada Conteúdo)
"""
Para cada id_conteudo (e nome_conteudo), contar quantas vezes cada tipo_interacao ocorreu (ex: Conteúdo X teve 50 'likes', 10 'shares', 5 'comments').
"""
def contar_tipos_interacao_por_conteudo(dados):
    resultado = {}
    for interacao in dados:
        id_conteudo = interacao.get('id_conteudo')
        nome_conteudo = interacao.get('nome_conteudo')
        tipo = interacao.get('tipo_interacao', '').strip().lower()
        if id_conteudo not in resultado:
            resultado[id_conteudo] = {
                'nome_conteudo': nome_conteudo,
                'interacoes': {}
            }
        if tipo:
            if tipo in resultado[id_conteudo]['interacoes']:
                resultado[id_conteudo]['interacoes'][tipo] += 1
            else:
                resultado[id_conteudo]['interacoes'][tipo] = 1
    return resultado


# FUNÇÃO 3.3 - Cálculo de Métricas (Tempo Total de Visualização por Conteúdo)
"""
Para cada id_conteudo (e nome_conteudo), calcular a soma total de watch_duration_seconds.
"""



# FUNÇÃO 3.4 - Cálculo de Métricas (Média de Tempo de Visualização por Conteúdo)
"""
Para cada id_conteudo (e nome_conteudo), calcular a média de watch_duration_seconds. Atenção: Considerar apenas as interações onde watch_duration_seconds for maior que 0 para este cálculo.
"""
def calcular_media_visualizacao_por_conteudo(conteudos):
    medias = {}
    for id_conteudo, info in conteudos.items():
        # Filtra apenas durações numéricas e maiores que zero
        duracoes = [
            interacao.get('watch_duration_seconds')
            for interacao in info['interacoes']
            if isinstance(interacao.get('watch_duration_seconds'), (int, float)) and interacao.get('watch_duration_seconds') > 0
        ]
        if duracoes:
            media = sum(duracoes) / len(duracoes)
        else:
            media = 0
        medias[id_conteudo] = {
            'nome_conteudo': info['nome_conteudo'],
            'media_watch_duration': media
        }
    return medias


# FUNÇÃO 3.5 - Cálculo de Métricas (Total de Interações por Conteúdo (Listagem de Comentários por Conteúdo)
"""
Criar uma função que, dado um id_conteudo, retorne (ou imprima de forma organizada) todos os comment_text associados a ele.
"""
def listar_comentarios_por_conteudo(conteudos, id_conteudo):
    comentarios = []
    conteudo = conteudos.get(id_conteudo)
    if conteudo:
        for interacao in conteudo['interacoes']:
            if interacao.get('tipo_interacao') == 'comment':
                comentarios.append(interacao.get('comment_text'))
    return comentarios


# FUNÇÃO 3.6 - Cálculo de Métricas (Listagem dos top-5 conteúdos com mais visualizações)
"""
Criar uma função que retorne (ou imprima de forma organizada) os top-5 conteúdos com mais visualizações.
"""
def top_5_conteudos_mais_vistos(linhas):
    visualizacoes = defaultdict(lambda: {'nome_conteudo': '', 'total_views': 0})
    for linha in linhas:
        if linha.get('tipo_interacao') == 'view_start':
            conteudo_id = linha['id_conteudo']
            visualizacoes[conteudo_id]['nome_conteudo'] = linha['nome_conteudo']
            visualizacoes[conteudo_id]['total_views'] += 1
# Colocar na ordem
    top_5 = sorted(visualizacoes.items(), key=lambda item: item[1]['total_views'], reverse=True)[:5]
    return top_5