# Projeto Módulo 1 - Globotech

*Fase 1 do projeto unificado "Análise de Engajamento de Mídias Globo"*

## Dependências

Este projeto foi desenvolvido utilizando apenas **Python puro**, ou seja, não é necessário instalar nenhuma biblioteca externa para executar o código.  
Todas as funcionalidades utilizam apenas módulos da biblioteca padrão do Python.

- **Versão recomendada do Python:** 3.8 ou superior

**Ferramentas utilizadas no desenvolvimento:**
- **Editor de código:** Visual Studio Code (VSCode)
- **Controle de versão e colaboração:** Git e GitHub

**Observação:**  
Para executar os scripts, basta garantir que você tenha o Python instalado em seu sistema operacional.  
Não é necessário rodar `pip install` ou qualquer outro gerenciador de pacotes.

## Estrutura do Repositório

-   `Scripts/`: Contém os scripts em Python main, tratamento e funções.
-   `Arquivos/`: Contém os arquivos de dados resultantes dos scripts.
-   `Docs/`: Contém os arquivos de texto, incluindo o relatório final.
-   `README.md`: Este arquivo de documentação.

## Solicitações do Projeto

### Parte 1 - Validação e Limpeza dos Dados 
Foi solicitado no projeto que, após o carregamento inicial dos dados para a memória (em uma lista de dicionários, onde cada dicionário representa uma linha do CSV), fossem desenvolvidas funções em Python para:

- **Tratamento de `watch_duration_seconds`:**
  - Identificar valores ausentes ou vazios nesta coluna.
  - Caso o campo `tipo_interacao` indique consumo de vídeo (por exemplo, `view_start`), converter valores ausentes ou vazios para 0.
  - Para tipos de interação que não envolvem visualização (como `like`, `share`, `comment`), o campo foi tratado como `None`, diferenciando de visualizações reais.
  - **Justificativa:**  
    Optou-se por utilizar o valor `None` para indicar ausência de duração, pois isso facilita o tratamento dos dados e evita erros nos cálculos de soma e média. Se fosse utilizado um valor como `"não aplicável"` (string), operações matemáticas resultariam em erro, já que não é possível somar ou dividir strings com números. Com `None`, é possível filtrar facilmente apenas os valores numéricos durante os cálculos.
  - Converter a coluna `watch_duration_seconds` para um tipo numérico adequado (float) quando aplicável.
- **Limpeza de Campos de Texto:**
  - Remover espaços em branco desnecessários no início e no fim de campos como `plataforma` e `tipo_interacao`.
- **Tratamento de Exceções:**
  - Implementar tratamento básico de exceções (blocos try-except) durante as conversões de tipo e outras operações de limpeza, evitando que o script seja interrompido por dados inesperados.
  
---

### Parte 2 - Estruturação dos Dados
Foi solicitado no projeto que, após a limpeza, os dados processados fossem armazenados em uma estrutura de dados Python que facilitasse consultas e cálculos de métricas.

- **Estrutura escolhida:**  
  Dicionário agrupado por conteúdo (`id_conteudo`), onde:
  - Cada chave corresponde a um `id_conteudo`.
  - O valor associado é um dicionário contendo:
    - `nome_conteudo` (string)
    - Uma lista de todas as interações (cada uma como dicionário com: `timestamp_interacao`, `id_usuario`, `plataforma`, `tipo_interacao`, `watch_duration_seconds`, `comment_text`).

**Justificativa:**  
Essa estrutura foi considerada adequada por permitir acesso rápido e eficiente às interações de cada conteúdo, facilitando o cálculo de métricas e a geração de relatórios por conteúdo.

---

### Parte 3 - Cálculo de Métricas Simples
Foi solicitado no projeto o desenvolvimento de funções para calcular as seguintes métricas de engajamento:

- **Total de Interações por Conteúdo:**  
  Para cada `id_conteudo` (e seu respectivo `nome_conteudo`), calcular o número total de interações dos tipos `'like'`, `'share'`, `'comment'`.

- **Contagem por Tipo de Interação para Cada Conteúdo:**  
  Para cada conteúdo, contar quantas vezes cada `tipo_interacao` ocorreu (exemplo: 50 `'likes'`, 10 `'shares'`, 5 `'comments'`).

- **Tempo Total de Visualização por Conteúdo:**  
  Para cada conteúdo, calcular a soma total de `watch_duration_seconds`.

- **Média de Tempo de Visualização por Conteúdo:**  
  Para cada conteúdo, calcular a média de `watch_duration_seconds` (considerando apenas valores maiores que 0).

- **Listagem de Comentários por Conteúdo:**  
  Função que, dado um `id_conteudo`, retorna ou imprime todos os `comment_text` associados a ele.

- **Top-5 conteúdos com mais visualizações:**  
  Função que retorna ou imprime os cinco conteúdos com maior número de visualizações.

---

## Autores

- André Carioca
- Diego Teixeira
- Marcelo Zilotti
- Mirra Bernardo
- Tales Honorio
- William Lopes