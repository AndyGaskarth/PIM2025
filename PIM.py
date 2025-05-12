import json

# Variável global para armazenar o login do usuário
usuario_logado = None
# Variável global para armazenar o tipo de acesso do usuário
usuario_role = None

def carregar_acessos():
    """Função para carregar os acessos dos usuários a partir de um arquivo JSON."""
    with open("user.json", "r", encoding="utf-8") as user_file:
        # Carrega os dados do arquivo JSON e retorna como um dicionário
            return json.load(user_file)
    
def verificar_acesso(usuario, senha):
    """Função para verificar o login, senha e retornar o tipo de acesso (role) e o nome completo do usuário."""
    acessos = carregar_acessos()
    for u in acessos["usuarios"]:
        if u["username"] == usuario and u["password"] == senha:
            # Retorna a role e o nome completo do usuário
            nome_completo = f"{u.get('firstName', '')} {u.get('lastName', '')}".strip()
            return u["role"], nome_completo
    return None, None  # Retorna None se o login ou senha estiverem incorretos
        
def cadastrar_usuario():
        """Função para informar sobre o processo de cadastro de um novo usuário."""
        print("=== Cadastro de Novo Usuário ===")
        print("Por gentileza, buscar a secretaria ou seu representante imediato para solicitar o registro de teu acesso.")

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
        print("0. Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            username = input("Digite seu login: ").strip()
            senha = input("Digite sua senha: ").strip()
            if not username or not senha:
                print("O login e a senha não podem estar vazios. Tente novamente.")
            else:
                # Verifica o login, senha e role do usuário
                usuario_role, nome_completo = verificar_acesso(username, senha)
                if usuario_role:
                    usuario_logado = nome_completo  # Armazena o nome completo do usuário
                    print(f"Bem-vindo, {usuario_logado}!")
                else:
                    print("Login ou senha incorretos. Tente novamente.")
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

    if not username or not nova_senha:
        print("O nome de usuário e a nova senha não podem estar vazios.")
        return

    # Carregar os dados do arquivo JSON
    acessos = carregar_acessos()

    # Procurar o usuário no JSON
    for usuario in acessos["usuarios"]:
        if usuario["username"] == username:
            usuario["password"] = nova_senha  # Atualizar a senha
            break
    else:
        print("Usuário não encontrado.")
        return

    # Salvar as alterações no arquivo JSON
    with open("user.json", "w", encoding="utf-8") as user_file:
        json.dump(acessos, user_file, indent=4, ensure_ascii=False)

    print(f"A senha do usuário '{username}' foi alterada com sucesso.")


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
            print("Curso de Python: Aprenda a programar em Python do básico ao avançado.")
        elif escolha == 2:
            print("Curso de Front-End: Crie interfaces modernas para sites e sistemas usando tecnologias essenciais do desenvolvimento web.")
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


def menu():
    """Função para exibir o menu principal."""
    global usuario_logado, usuario_role
    print(f"\nUsuário logado: {usuario_logado}")
    print("=== Menu Principal ===")
    print("1. Menu de Cursos Disponíveis")
    if usuario_role == "admin":
        print("2. Gerenciar Usuários")
        print("3. Alterar Senha de Usuário")
    print("0. Sair")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        menu_cursos()
    elif escolha == "2" and usuario_role == "admin":
        print("Acesso ao Gerenciamento de Usuários.")
    elif escolha == "3" and usuario_role == "admin":
        alterar_senha()
    elif escolha == "0":
        print("Saindo...")
        exit()
    else:
        print("Opção inválida ou acesso negado.")
    

def main():
    """Função principal que controla o fluxo do programa."""
    menu_login()  # Exibe a página de login primeiro
    while True:
        menu()  # Exibe o menu após o login

if __name__ == "__main__":
    main()


