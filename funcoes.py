# Lista dos tipos de interação que indicam consumo de vídeo
tipos_visualizacao = ['view_start', 'play']

def tratar_linha(linha):
    """
    Limpa e trata uma linha do CSV:
    - Remove espaços extras dos campos de texto 'plataforma' e 'tipo_interacao'.
    - Converte o campo 'watch_duration_seconds' para float ou None, conforme as regras:
        * Se o tipo de interação for de visualização, valores ausentes/vazios/não numéricos viram 0.
        * Para outros tipos de interação, valores ausentes/vazios/não numéricos viram None.
    - Remove qualquer chave None do dicionário (caso tenha sido criada por erro de leitura).
    """
    plataforma = linha.get('plataforma', '').strip()
    tipo_interacao = linha.get('tipo_interacao', '').strip()
    valor = linha.get('watch_duration_seconds', None)
    tipo_lower = tipo_interacao.lower()

    if tipo_lower in tipos_visualizacao: # Para interações de visualização, valores ausentes/vazios/não numéricos viram 0
        if valor is None or valor.strip() == '':
            watch_duration = 0
        else:
            try:
                watch_duration = float(valor.strip())
            except (ValueError, TypeError):
                watch_duration = 0
    else: # Para outros tipos de interação, valores ausentes/vazios/não numéricos viram None
        if valor is None or valor.strip() == '':
            watch_duration = None
        else:
            try:
                watch_duration = float(valor.strip())
            except (ValueError, TypeError):
                watch_duration = None

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