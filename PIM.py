

import json

# Variável global para armazenar o login do usuário
usuario_logado = None

def carregar_acessos():
    """Função para carregar os acessos dos usuários a partir de um arquivo JSON."""
    with open("user.json", "r", encoding="utf-8") as arquivo:
            acessos = json.load(arquivo)
            return json.load(arquivo)
    
def verificar_acesso(usuario):
    """Função para verificar o tipo de acesso do usuário."""
    acessos = carregar_acessos()
    for u in acessos["usuarios"]:
        if u["login"] == usuario:
            return u["tipo_acesso"]

def login():
    """Função para realizar o login do usuário.
    Exibe a página de login e solicita o nome do usuário até que ele seja fornecido.
    também foi criado uma variavel para sempre que o usuario logar, o nome dele ser armazenado na variavel usuario_logado"""
    global usuario_logado
    print("=== Página de Login ===")
    while not usuario_logado:
        usuario_logado = input("Digite seu login: ").strip()
        if not usuario_logado:
            print("O login não pode estar vazio. Tente novamente.")
    print(f"Bem-vindo, {usuario_logado}!")

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
    """Função para realizar o login do usuário."""
    global usuario_logado
    while not usuario_logado:
        print("=== Página de Login ===")
        print("1. Fazer Login")
        print("2. Cadastrar Novo Usuário")
        print("3. Esqueci a Senha")
        print("0. Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            usuario_logado = input("Digite seu login: ").strip()
            if not usuario_logado:
                print("O login não pode estar vazio. Tente novamente.")
            else:
                print(f"Bem-vindo, {usuario_logado}!")
        elif escolha == "2":
            cadastrar_usuario()
        elif escolha == "3":
            esqueci_senha()
        elif escolha == "0":
            print("Saindo...")
            exit()
        else:
            print("Opção inválida. Tente novamente.")

def listar_cursos():
        """Função para listar todos os cursos disponíveis."""
        while True:
            print("\n=== Listar Todos os Cursos ===")
            print("1. Curso de Python")
            print("2. ")
            print("3. ")
            print("4. ")
            print("0. Voltar ao Menu Principal")
            escolha = input("Escolha uma opção: ").strip()
            if escolha == "1":
                print("Curso de Python: Aprenda a programar em Python do básico ao avançado.")
            elif escolha == "0":
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
    curso_nome = input("Digite o nome do curso que deseja cadastrar: ").strip()
    if curso_nome:
        print(f"Solicitação de cadastro do curso '{curso_nome}' enviada com sucesso!")
    else:
        print("O nome do curso não pode estar vazio. Tente novamente.")

def ultimo_curso_assistido():
    """Função para exibir o último curso assistido."""
    print("=== Último Curso Assistido ===")
    print("Nenhum curso assistido registrado.")

def security():
    while True:
        """Função para exibir informações de segurança (LGPD)."""
        print("=== Informações de Segurança (LGPD) ===")
        print("\n")
        print("Este sistema respeita a Lei Geral de Proteção de Dados (LGPD).")
        print("Seus dados pessoais estão protegidos e não serão compartilhados sem sua autorização.")
        print("Para mais informações, consulte nossa política de privacidade.")
        print("Caso tenha alguma dúvida, entre em contato com o suporte.")
        print("\n")
        print("=== Fim das Informações de Segurança (LGPD) ===")
        print("1. Próxima página")
        print("0. Voltar ao Menu Principal")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            security1()
        elif escolha == "0":
            print("Voltando ao Menu Principal...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def security1():
    while True:
        """Função para exibir informações de segurança (LGPD) - Página 1."""
        print("=== Informações de Segurança (LGPD) - Página 1 ===")
        print("\n")
        print("A segurança de dados é essencial para proteger informações pessoais e acadêmicas em plataformas educacionais. \nA LGPD (Lei Geral de Proteção de Dados) regula o uso de dados pessoais, garantindo direitos como acesso, correção e exclusão de informações.")
        print("A LGPD exige que plataformas adotem medidas de segurança, como criptografia e controle de acesso, para proteger os dados dos usuários. \nEssas práticas ajudam a criar um ambiente digital mais seguro e confiável.")
        print("Boas práticas incluem o uso de senhas fortes, autenticação de dois fatores (2FA) e evitar o compartilhamento de credenciais. \nAlém disso, é importante estar ciente de como os dados são coletados, armazenados e utilizados pelas instituições.")
        print("A segurança de dados é uma responsabilidade compartilhada entre usuários e instituições. \nMantenha-se informado sobre as melhores práticas e proteja suas informações pessoais.")
        print("Cuidado com ataques de phishing, evitando clicar em links suspeitos. Sempre faça logout em dispositivos compartilhados \ne leia as políticas de privacidade antes de aceitar termos.")
        print("\n")
        print("=== Fim das Informações de Segurança (LGPD) - Página 1 ===")
        print("0. Voltar ao Menu Principal")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "0":
            break
        else:
            print("Opção inválida. Tente novamente.")




def menu():
    """Função para exibir o menu principal."""
    global usuario_logado
    print(f"\nUsuário logado: {usuario_logado}")
    print("=== Menu Principal ===")
    print("1. Menu de Cursos Disponíveis")
    print("2. Solicitar Cadastro de Cursos")
    print("3. Último Curso Assistido")
    print("4. Informações de Segurança ( LGPD)")
    print("0. Sair")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        menu_cursos()
        print("Menu de Cursos Disponíveis")
    elif escolha == "2":
        cadastro_cursos()
    elif escolha == "3":
        ultimo_curso_assistido()
    elif escolha == "4":
        security()
    elif escolha == "0":
        print("Saindo...")
        exit()
    

def main():
    """Função principal que controla o fluxo do programa."""
    login()  # Exibe a página de login primeiro
    while True:
        menu()  # Exibe o menu após o login

if __name__ == "__main__":
    main()


