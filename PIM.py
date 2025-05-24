import json
import statistics
import bcrypt
from cryptography.fernet import Fernet
import os
from datetime import datetime
import openpyxl
from tkinter import Tk, filedialog
import copy


# Variável global para armazenar o login do usuário
usuario_logado = None
# Variável global para armazenar o tipo de acesso do usuário
usuario_role = None

# Armazena o nome de usuário do usuário atualmente logado, fiz isso porque não tava indo no menu de estatisticas 
usuario_logado_username = None

campos_sensiveis = ["firstName", "lastName", "idade"]

def carregar_chave():
    with open("chave.key", "rb") as arquivo_chave:
        chave = arquivo_chave.read()  # lê a chave já existente no arquivo
    cipher = Fernet(chave)  # cria o objeto Fernet com essa chave
    return cipher  # retorna o objeto para criptografar/descriptografar

def descriptografar_campos(usuario, campos_sensiveis, cipher):
    """Descriptografa os campos sensíveis de um usuário.
       Os campos não sensíveis são retornados como estão.
    """
    usuario_descriptografado = usuario.copy() # Cria uma cópia para não modificar o original

    for campo in campos_sensiveis: # Itera APENAS sobre os campos que DEVEM ser sensíveis
        if campo in usuario_descriptografado: # Verifica se o campo existe no dicionário do usuário
            try:
                # O valor a ser descriptografado é o valor do campo atual do usuário
                valor_criptografado = usuario_descriptografado[campo]
                valor_original_bytes = cipher.decrypt(valor_criptografado.encode('utf-8'))
                valor_original = valor_original_bytes.decode('utf-8')

                if campo == "idade":
                    valor_original = int(valor_original)
                
                usuario_descriptografado[campo] = valor_original
            except Exception as e:
                print(f"Erro ao descriptografar o campo '{campo}' para o usuário (ou dado inválido): {e}")
    return usuario_descriptografado

def criptografar_campos_usuarios(usuarios, campos_sensiveis, cipher):
    """
    Recebe uma lista de usuários com campos descriptografados e retorna a lista 
    com os campos sensíveis criptografados, pronta para salvar no JSON.
    """
    usuarios_criptografados = []

    for usuario in usuarios:
        # Faz uma cópia profunda para evitar alterações no original
        usuario_copy = copy.deepcopy(usuario)

        for campo in campos_sensiveis:
            if campo in usuario_copy:
                # Converte para string antes de criptografar
                valor_str = str(usuario_copy[campo])
                valor_criptografado = cipher.encrypt(valor_str.encode('utf-8')).decode('utf-8')
                usuario_copy[campo] = valor_criptografado

        usuarios_criptografados.append(usuario_copy)

    return usuarios_criptografados
    

def carregar_acessos():
    """Carrega os acessos dos usuários a partir de um JSON e descriptografa os campos sensíveis."""
    cipher = carregar_chave()
    try:
        with open("user.json", "r", encoding="utf-8") as user_file:
            # Carrega os dados do arquivo JSON e retorna como um dicionário
            dados = json.load(user_file)

        if "usuarios" in dados and type(dados["usuarios"]) is list:
            dados["usuarios"] = [
                descriptografar_campos(usuario, campos_sensiveis, cipher)
                for usuario in dados["usuarios"]
            ]    
        else:
            print("Erro: A chave 'usuarios' não existe ou não contém uma lista.")
            # Retorna um dicionário vazio ou estrutura padrão em caso de erro na estrutura
            return {"usuarios": []} # Retorne uma estrutura válida para evitar erros posteriores

        return dados
    
    except FileNotFoundError:
        print("Erro: Arquivo 'user.json' não encontrado. Certifique-se de que ele existe.")
        return {"usuarios": []} # Retorna uma estrutura vazia para evitar erros
    except json.JSONDecodeError:
        print("Erro: O arquivo 'user.json' não é um JSON válido. Verifique o conteúdo.")
        return {"usuarios": []} # Retorna uma estrutura vazia para evitar erros
    
def salvar_usuario(usuario):
    cipher = carregar_chave()
    campos_sensiveis = ["firstName", "lastName", "idade"]
    dados = {"usuarios": []} # Inicializa com uma lista vazia de usuários por padrão

    # Verifica se o arquivo user.json existe e não está vazio
    if os.path.exists("user.json") and os.path.getsize("user.json") > 0:
        try:
            with open("user.json", "r", encoding="utf-8") as user_file:
                dados = json.load(user_file)
        except json.JSONDecodeError:
            print("Atenção: O arquivo 'user.json' está corrompido ou vazio. Criando um novo.")

    for campo in campos_sensiveis:
        if campo in usuario:
            valor = str(usuario[campo])
            usuario[campo] = cipher.encrypt(valor.encode('utf-8')).decode('utf-8')

    if "usuarios" not in dados:
        dados["usuarios"] = []

    dados["usuarios"].append(usuario)

    with open("user.json", "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def verificar_acesso(usuario, senha):
    """Verifica o login usando hash com bcrypt"""
    acessos = carregar_acessos()
    for u in acessos["usuarios"]:
        if u["username"] == usuario:
            senha_armazenada = u["password"]
            if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada.encode('utf-8')):
            # Retorna a role e o nome completo do usuário
                nome_completo = f"{u.get('firstName', '')} {u.get('lastName', '')}".strip()
                return u["role"], nome_completo
    return None, None  # Retorna None se o login ou senha estiverem incorretos

def cadastrar_usuario():
    usu = input("Digite o Usuario Escolhido Pelo o Aluno: ")
    nome = input("Digite o Primeiro Nome do Aluno: ")
    segundo = input("Digite o Ultimo Nome do Aluno: ")
    senha = input("Digite a Senha Escolhida do Aluno: ")
    curso = input("Digite o Curso Escolhido do Aluno: ")
    ra = input("Digite o RA do Aluno: ")
    idade = input("Digite a Idade do Aluno: ")

    consentimento = input("O aluno concorda com o termo de consentimento? (sim/não): ").strip().lower()
    if consentimento != "sim":
        print("Cadastro cancelado. É necessário o consentimento do aluno para prosseguir.")
        return
    consentimento = True

    if not all([nome, segundo, senha, curso, ra, idade]):
        print("Todos os campos são obrigatórios.")
        return

    senha_hash = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt()).decode("utf-8")

    usuario = {
        "username": usu,
        "password": senha_hash,
        "role": "aluno",
        "firstName": nome,
        "lastName": segundo,
        "ra": ra,
        "idade": idade,
        "acessos": 0,
        "cursos_concluidos": 0,
        "ultimo_curso": "Nenhum",
        "media_semanal": 0,
        "consentimento": consentimento,
    }

    salvar_usuario(usuario)
    print(f"Usuário {usu} cadastrado com sucesso!")


def registrar_log(usuario_logado):
    with open("acessos.log", "a", encoding="utf-8") as log:
        log.write(f"{datetime.now()} - Login: {usuario_logado}\n")

def esqueci_senha():
    """Função para solicitar com a recuperação de senha."""
    print("=== Recuperação de Senha ===")
    ra = input("Digite seu ra cadastrado: ").strip()
    if ra:
        print(f"O administrador foi acionado para realizar o reset da senha do RA: {ra}.")
    else:
        print("Este RA não está cadastrado. Tente novamente. \nCaso não tenha cadastro, entre em contato com o suporte.")

def menu_login():
    """Função para realizar o login do usuário e validar o tipo de acesso."""
    global usuario_logado, usuario_role
    while not usuario_logado:
        print("=== Página de Login ===")
        print("1. Fazer Login")
        print("2. Esqueci minha senha")
        print("0. Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            username = input("Digite seu login: ").strip()
            senha = input("Digite sua senha: ").strip()
            if not username or not senha:
                print("O login e a senha não podem estar vazios. Tente novamente.")
            else:
                # Verifica o login, senha e role do usuário
                role, nome_completo = verificar_acesso(username, senha)
                if role:
                    usuario_logado = nome_completo # Atualiza a variável global com o nome completo do usuário
                    usuario_role = role   
                    global usuario_logado_username
                    usuario_logado_username = username
                    print(f"Bem-vindo, {usuario_role}!")
                    #registrar logs de cada usuario logado
                    registrar_log(username)
                else:
                    print("Login ou senha incorretos. Tente novamente.")
        elif escolha == "2":
            esqueci_senha()
        elif escolha == "0":
            print("Saindo...")
            exit()
        else:
            print("Opção inválida. Tente novamente.")

def alterar_senha():
    """Função para alterar a senha de um usuário (apenas para admins)."""
    global usuario_role

    if usuario_role != "admin":
        print("Acesso negado. Apenas administradores podem alterar senhas.")
        return

    print("=== Alterar Senha de Usuário ===")
    username = input("Digite o nome de usuário para alterar a senha: ").strip()
    nova_senha = input("Digite a nova senha: ").strip()

    if len(nova_senha) < 6:
        print("A nova senha deve ter pelo menos 6 caracteres.")
        return

    if not username or not nova_senha:
        print("O nome de usuário e a nova senha não podem estar vazios.")
        return

    with open("user.json", "r", encoding="utf-8") as user_file:
        # Carrega os dados do arquivo JSON e retorna como um dicionário
        dados = json.load(user_file)
    

    for usuario in dados["usuarios"]:
        if usuario["username"] == username:
            senha_hash = bcrypt.hashpw(nova_senha.encode('utf-8'), bcrypt.gensalt())
            usuario["password"] = senha_hash.decode('utf-8')  # Atualizar a senha
            usuario_encontrado = True
            break

    if not usuario_encontrado:
        print("Usuário não encontrado.")
        return

    # 💾 Salva o JSON com os dados atualizados
    with open("user.json", "w", encoding="utf-8") as user_file:
        json.dump(dados, user_file, indent=4, ensure_ascii=False)

    print(f"A senha do usuário '{username}' foi alterada com sucesso.")


    
def front_end_curso(linhas_por_pagina=5):
    try:
        with open("cursos/front_end.txt", "r", encoding="utf-8") as f:
            print(f.read())
            linhas = f.readlines()
            total_linhas = len(linhas)
            pagina = 0
            while pagina * linhas_por_pagina < total_linhas:
                inicio = (pagina - 1)* linhas_por_pagina
                fim = min(inicio + linhas_por_pagina)
                for linha in linhas[inicio:fim]:
                    print(f"Página {pagina}", end='')
                pagina += 1
                if fim < total_linhas:
                    input("\nPressione Enter para continuar...")
                
    except FileNotFoundError:
        print("Arquivo de descrição do curso não encontrado.")

def python_curso():
    """Exibe o conteúdo de um arquivo .txt na tela."""
    try:
        with open("cursos/python.txt", "r", encoding="utf-8") as f:
            print(f.read())
    except FileNotFoundError:
        print("Arquivo de descrição do curso não encontrado.")

def listar_cursos():
    """Função para listar todos os cursos disponíveis."""
    while True:
        print("\n=== Listar Todos os Cursos ===")
        print("1. Curso de Python")
        print("2. Curso de Front-End")
        print("3. Curso de Banco de Dados")
        print("4. Curso de Desenvolvimento Web com Flask")
        print("0. Voltar ao Menu Principal")

        try: # caso o usuário digite algo que não seja um número, vamos capturar o erro e mostrar uma mensagem amigável, evitando que o programa trave.
            escolha = int(input("Escolha uma opção: ").strip())
        except ValueError:
            print("Entrada inválida. Por favor, digite um número.")
            continue
        if escolha == 1:
            print("\n=== Curso de Python: Aprenda a programar em Python do básico ao avançado. ===")
            python_curso()
        elif escolha == 2:
            print("\n=== Curso de Front-End: Crie interfaces modernas para sites e sistemas usando tecnologias essenciais do desenvolvimento web ===.")
            front_end_curso()
        elif escolha == 3:
            print("Curso de Banco de Dados: Aprenda a modelar, criar e manipular bancos de dados com SQL.")
        elif escolha == 4:
            print("Curso de Desenvolvimento Web com Flask: Crie sites e aplicações com o framework Flask, usando Python.")
        elif escolha == 0:
            print("Voltando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_cursos():
    """Função para exibir o submenu de cursos disponíveis."""
    while True:
        print("\n=== Menu de Cursos Disponíveis ===")
        print("1. Listar Todos os Cursos")
        print("2. Buscar Curso por Nome")
        print("0. Voltar ao Menu Principal")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            print("Listando todos os cursos disponíveis...")
            listar_cursos()
        elif escolha == "2":
            curso_nome = input("Digite o nome do curso que deseja buscar: ").strip()
            print(f"Buscando informações sobre o curso: {curso_nome}...")
        elif escolha == "0":
            print("Voltando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def cadastro_cursos():
    """Função para solicitar o cadastro de novos cursos."""
    print("=== Solicitar Cadastro de Cursos ===")
    while True: 
        curso_nome = input("Digite o nome do curso que deseja cadastrar: ").strip()
        if curso_nome:
            print(f"Solicitação de cadastro do curso '{curso_nome}' enviada com sucesso!")
            break
        else:
            print("O nome do curso não pode estar vazio. Tente novamente.")

def ultimo_curso_assistido():
    """Função para exibir o último curso assistido."""
    print("=== Último Curso Assistido ===")
    print("Nenhum curso assistido registrado.")


def menu_seguranca():
    while True:
        """Menu principal de segurança (LGPD)."""
        print("\n=== Menu de Segurança e Privacidade ===")
        print("1. Ver Informações sobre a LGPD")
        print("2. Perguntas Frequentes sobre LGPD")
        print("3. Seus Direitos como Usuário")
        print("4. Como proteger sua conta")
        print("5. Solicitar exclusão de dados")
        print("0. Voltar ao Menu Principal")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            pagina_lgpd()
        elif escolha == "2":
            perguntas_frequentes_lgpd()
        elif escolha == "3":
            print("Você tem direito de acessar, corrigir ou excluir seus dados pessoais, conforme a LGPD.")
        elif escolha == "4":
            print("\nPara proteger sua conta:\n- Use senhas diferentes em cada serviço.\n- Ative autenticação de dois fatores.\n- Evite clicar em links suspeitos.\n- Sempre saia da conta ao usar dispositivos públicos.")
        elif escolha == "5":
            ra = input("Digite seu usuario para solicitar a exclusão dos dados: ").strip()
            if ra:
                print(f"Sua solicitação de exclusão de dados para o Usuario {ra} foi registrada e será analisada pelo setor responsável ")
            else:
                print("RA inválido. Tente novamente.")
        elif escolha == "0":
            print("Voltando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def pagina_lgpd():
    """Página informativa da LGPD."""
    while True:
        print("=== Informações sobre a LGPD ===\n")
        print("Este sistema respeita a Lei Geral de Proteção de Dados (LGPD).")
        print("Seus dados pessoais estão protegidos e não serão compartilhados sem sua autorização.")
        print("Para mais informações, consulte nossa política de privacidade.")
        print("Caso tenha alguma dúvida, entre em contato com o suporte.")
        print("\n")
        print("A segurança de dados é essencial para proteger informações pessoais e acadêmicas em plataformas educacionais.")
        print("A LGPD regula o uso de dados pessoais, garantindo direitos como acesso, correção e exclusão de informações.")
        print("Ela exige que plataformas adotem medidas de segurança como criptografia e controle de acesso.")
        print("\nBoas práticas incluem:")
        print("- Uso de senhas fortes")
        print("- Autenticação de dois fatores (2FA)")
        print("- Não compartilhar credenciais")
        print("- Fazer logout em dispositivos públicos")
        print("- Evitar clicar em links suspeitos")
        print("- Ler políticas de privacidade antes de aceitar termos\n")
        print("A segurança é uma responsabilidade compartilhada entre usuários e instituições.")
        print("\n=== Fim das Informações sobre a LGPD ===")
        print("0. Voltar ao Menu de Segurança")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            break
        else:
            print("Opção inválida. Tente novamente.\n")

def perguntas_frequentes_lgpd():
    while True:
        """Função para exibir perguntas frequentes sobre LGPD."""
        print("=== Perguntas Frequentes sobre LGPD ===")
        print("1. O que é a LGPD?")
        print("2. Quais dados são coletados?")
        print("3. Como posso corrigir meus dados?")
        print("4. Como posso excluir meus dados?")
        print("0. Voltar ao Menu de Segurança")
        escolha = int(input("Escolha uma opção: ").strip())
        if escolha == 1:
            print("A LGPD é a Lei Geral de Proteção de Dados, que visa garantir a privacidade dos dados pessoais.")
        elif escolha == 2:
            print("Coletamos dados como nome, email, e outros dados necessários para prestar nossos serviços.")
        elif escolha == 3:
            print("Você pode corrigir seus dados entrando em contato com o suporte.")
        elif escolha == 4:
            print("Você pode solicitar a exclusão dos seus dados entrando em contato com o suporte.")
        elif escolha == 0:
            print("Voltando ao Menu de Segurança...")
            return  
        else: 
            print("Opção inválida. Tente novamente.")

def menu_estatisticas():
    while True:
        print("=== Estatísticas do Usuário  ===")
        print("1. Ver Estatísticas Gerais da Plataforma")
        print("2. Ver Meu Desempenho")
        print("0. Voltar ao Menu Principal")
        escolha = int(input("Escolha uma opção: ").strip())

        if escolha == 1:
            estatisticas_gerais()
        elif escolha == 2:
            estatisticas_usuario()
        elif escolha == 0:
            break
        else:
            print("Opção inválida. Tente novamente.")

def estatisticas_gerais():
    print("\n====== ESTATÍSTICAS GERAIS ======")

    if usuario_role not in ["admin","coordenacao","professor"]:
        print("Acesso negado. Apenas administradores e professores podem acessar as estatísticas gerais.")
        return

    acessos = carregar_acessos()

    # Filtra apenas alunos que deram consentimento e tem a chave 'role'
    alunos = [
        u for u in acessos["usuarios"]
        if u.get('role') == 'aluno' and u.get("consentimento") is True
    ]

    total_alunos = len(alunos)
    total_acessos = sum(u.get('acessos', 0) for u in alunos)
    media_acessos = total_acessos / total_alunos if total_alunos > 0 else 0

    total_cursos = sum(u.get('cursos_concluidos', 0) for u in alunos)
    media_cursos = total_cursos / total_alunos if total_alunos > 0 else 0

    aluno_mais_ativo = max(alunos, key=lambda u: u.get('acessos', 0), default=None)
    aluno_menos_ativo = min(alunos, key=lambda u: u.get('acessos', 0), default=None)

    if aluno_mais_ativo:
        print(f"Maior número de acessos por um aluno: {aluno_mais_ativo.get('acessos', 0)} acessos")
    else:
        print("Não há registros de acessos de alunos.")

    if aluno_menos_ativo:
         print(f"Menor número de acessos por um aluno: {aluno_menos_ativo.get('acessos', 0)} acessos")
    else:
        print("Não há registros de acessos de alunos.")

    print(f"Total de alunos: {total_alunos}")
    print(f"Total de acessos: {total_acessos}")
    print(f"Média de acessos por aluno: {media_acessos:.2f}")
    print(f"Total de cursos concluídos: {total_cursos}")
    print(f"Média de cursos concluídos por aluno: {media_cursos:.2f}")
    print("=================================")

def estatisticas_usuario():
    """Exibe as estatísticas do usuário atualmente logado. Os dados são carregados a partir do arquivo 'user.json'."""
    global usuario_logado, usuario_logado_username, usuario_role
        
    if 'usuario_logado' not in globals() or not usuario_logado:
        print("Nenhum usuário está logado.")
        return

    #Tenta abrir o arquivo JSON com os dados dos usuários
    dados_descriptografados = carregar_acessos()
    
    # Procura os dados do usuário logado no JSON
    for usuario in dados_descriptografados["usuarios"]:
        if usuario.get("username") == usuario_logado_username:
            print("\n=== Estatísticas do Usuário ===")
            print(f"Nome: {usuario_logado}")
            print(f"Idade: {usuario.get('idade', 'N/A')}")
            print(f"Acessos: {usuario.get('acessos', 'N/A')}")
            print(f"Cursos Concluídos: {usuario.get('cursos_concluidos', 'N/A')}")
            print(f"Tempo Médio de Estudo Semanal: {usuario.get('media_semanal', 'N/A')} Horas na Semana")
            return
    print("Usuário não encontrado no arquivo de estatísticas.")

    #função para gerar hash de cada senha



def exportar_dados_xlsx(campo, valor=None):
    """Exporta dados filtrados para um arquivo Excel (.xlsx) em local escolhido pelo usuário."""
    try:
        dados = carregar_acessos()
    except FileNotFoundError:
        print("Arquivo de dados não encontrado.")
        return

    encontrados = []
    for usuario in dados.get("usuarios", []):
        if valor is None or str(usuario.get(campo, "")).lower() == str(valor).lower():
            encontrados.append(usuario)

    if not encontrados:
        print("Nenhum usuário encontrado com esse critério.")
        return

    # Cria a planilha
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Usuários"

    # Cabeçalho
    ws.append(["Nome", "Sobrenome", "Idade", "RA"])

    # Dados
    for usuario in encontrados:
        ws.append([
            usuario.get('firstName', 'N/A'),
            usuario.get('lastName', 'N/A'),
            usuario.get('idade', 'N/A'),
            usuario.get('ra', 'N/A')
        ])

    # Abre janela para escolher onde salvar
    Tk().withdraw()  # Oculta a janela principal do Tkinter
    caminho = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Planilha Excel", "*.xlsx")],
        title="Salvar como"
    )
    if caminho:
        wb.save(caminho)
        print(f"Arquivo salvo em: {caminho}")
    else:
        print("Exportação cancelada.")

def exportar_alunos_xlsx():
    """Exporta dados de todos os usuários com role 'aluno' para um arquivo Excel (.xlsx) em local escolhido pelo usuário."""
    try:
        dados = carregar_acessos()
    except FileNotFoundError:
        print("Arquivo de dados não encontrado.")
        return

    alunos = [u for u in dados.get("usuarios", []) if u.get("role", "").lower() == "aluno"]

    if not alunos:
        print("Nenhum aluno encontrado.")
        return

    # Cria a planilha
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Alunos"

    # Cabeçalho
    ws.append(["Nome", "Sobrenome", "Idade", "RA"])
 
    # Dados
    for usuario in alunos:
        ws.append([
            usuario.get('firstName', 'N/A'),
            usuario.get('lastName', 'N/A'),
            usuario.get('idade', 'N/A'),
            usuario.get('ra', 'N/A')
        ])

    # Abre janela para escolher onde salvar
    Tk().withdraw()  # Oculta a janela principal do Tkinter
    caminho = filedialog.asksaveasfilename(
        defaultextension=".xlsx",
        filetypes=[("Planilha Excel", "*.xlsx")],
        title="Salvar como"
    )
    if caminho:
        wb.save(caminho)
        print(f"Arquivo salvo em: {caminho}")
    else:
        print("Exportação cancelada.")

def menu():
    """Função para exibir o menu principal."""
    global usuario_logado, usuario_role
    print(f"\nUsuário logado: {usuario_logado}")
    print("=== Menu Principal ===")
    print("1. Menu de Cursos Disponíveis")
    print("2. Segurança e Privacidade")
    print("3. Estatísticas Do Usuário")
    if usuario_role == "admin":
        print("4. Menu de Gerenciamento de Usuários")
    if usuario_role == "professor":
        print("4. Area do Professor")
    print("0. Sair")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        menu_cursos()
    elif escolha == "2":
        menu_seguranca()
    elif escolha == "3":
        menu_estatisticas()
    elif escolha == "4" and usuario_role == "admin":
        menu_admin()
        # Aqui você pode implementar a lógica para exportar as informações do usuário
    elif escolha == "4" and usuario_role == "professor":
        menu_professor()
        # Aqui você pode implementar a lógica para a área do professor
    elif escolha == "0":
        print("Saindo...")
        exit()
    else:
        print("Opção inválida ou acesso negado.")

def menu_admin():
    print("=== Menu Admin ===")
    print("1. Gerenciar Usuários")
    print("2. Alterar Senha de Usuário")
    print("3. Exportar informações do Usuário")
    print("4. Cadastrar Novo Aluno")
    escolha = input("Escolha uma opção: ")
    if escolha == "1" and usuario_role == "admin":
        print("Gerenciando Usuários...")
        # Aqui você pode implementar a lógica para gerenciar usuários
    elif escolha == "2"and usuario_role == "admin":
        alterar_senha()
    elif escolha == "3"and usuario_role == "admin":
        print("Exportando informações do usuário...")
        exportar_alunos_xlsx("username")
    elif escolha == "4" and usuario_role == "admin":
        cadastrar_usuario()
    elif escolha == "0":
        print("Voltando ao Menu Principal...")
    else:
        print("Opção inválida.")

def menu_professor():
    print("=== Menu Professor ===")
    print("1. Ver Estatísticas dos Alunos")
    print("2. Solicitar Exportação de Informações dos Alunos")
    print("3. Solicitar Cadastro de Cursos")
    print("0. Voltar ao Menu Principal")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        print("Exibindo estatísticas dos alunos...")
        # Aqui você pode implementar a lógica para exibir estatísticas dos alunos
    elif escolha == "2":
        print("Solicitando exportação de informações dos alunos...")
        print("Os administradores serão notificados para realizar a exportação.")
        # Aqui você pode implementar a lógica para solicitar exportação de informações
    elif escolha == "3":
        print("Solicitando cadastro de cursos...")
        print("Os administradores serão notificados para realizar o cadastro.")
        # Solicita o nome do curso
        curso_nome = input("Digite o nome do curso: ").strip()
        if curso_nome:
            # Cria a pasta cursos se não existir
            os.makedirs("cursos", exist_ok=True)
            # Cria o arquivo .txt com o nome do curso
            nome_arquivo = os.path.join("cursos", f"{curso_nome}.txt")
            with open(nome_arquivo, "w", encoding="utf-8") as f:
                f.write(f"Curso: {curso_nome}\nDescrição: (adicione aqui a descrição do curso)")
            print(f"Arquivo '{nome_arquivo}' criado com sucesso!")
        else:
            print("O nome do curso não pode estar vazio.")

        # Aqui você pode implementar a lógica para solicitar cadastro de cursos
        # Exemplo: salvar o nome do curso em um arquivo ou enviar para um administrador
    elif escolha == "0":
        print("Voltando ao Menu Principal...")
    elif escolha == "4":
        cadastrar_usuario()
    else:
        print("Opção inválida.")

def menu_aluno():
    print("=== Menu Aluno ===")
    print("1. Atividades complementares")
    print("2. Trabalhos em grupo")
    print("3. Trabalhos individuais")
    print("4. Provas")
    print("0. Voltar ao Menu Principal")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        print("Atividades complementares")
        try:
            with open("atividades/a1.txt", "r", encoding="utf-8") as f:
                print(f.read())
        except FileNotFoundError:
            print("Arquivo de atividades complementares não encontrado.")
        # Aqui você pode implementar a lógica para exibir atividades complementares
    elif escolha == "2":
        ultimo_curso_assistido()
    elif escolha == "3":
        exportar_dados_xlsx("username", usuario_logado_username)
    elif escolha == "0":
        print("Voltando ao Menu Principal...")
    else:
        print("Opção inválida.")
    

def main():
    """Função principal que controla o fluxo do programa."""
    menu_login()  # Exibe a página de login primeiro
    while True:
        menu()  # Exibe o menu após o login

if __name__ == "__main__":
    main()

