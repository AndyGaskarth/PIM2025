import json

# 1. Abrir o arquivo JSON
with open('dados.json', 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

# 2. Adicionar o campo "consentimento" para cada usuário, se ainda não existir
for usuario in dados['usuarios']:
    if 'consentimento' not in usuario:
        usuario['consentimento'] = False  # ou True, se preferir

# 3. Salvar o JSON de volta no mesmo arquivo
with open('dados.json', 'w', encoding='utf-8') as arquivo:
    json.dump(dados, arquivo, indent=4, ensure_ascii=False)

print("Campo 'consentimento' adicionado com sucesso!")