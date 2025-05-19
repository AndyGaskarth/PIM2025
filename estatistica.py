import json
import random
import statistics

with open('estatisticas_usuarios.json', 'r', encoding='utf-8') as arquivo:
    dados = json.load(arquivo)

tempo_acesso = []

for usuario in dados["usuarios"]:
    if "acessos" in usuario:
        tempo_acesso.extend(usuario["acessos"]) # adiciona todos os tempos à lista geral

print(tempo_acesso)