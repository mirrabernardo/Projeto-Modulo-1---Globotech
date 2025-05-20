from funcoes import carregar_dados_csv

linhas, fieldnames = carregar_dados_csv('./Arquivos/interacoes_globo_tratado.csv')

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

# Texte de código para ver o ID, nome do contúdo e total de interações
for id_conteudo, info in conteudos.items():
    print(f"ID: {id_conteudo} | Nome: {info['nome_conteudo']} | Total de interações: {len(info['interacoes'])}")