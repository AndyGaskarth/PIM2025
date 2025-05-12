

import json

# Variável global para armazenar o login do usuário
usuario_logado = None
# Variável global para armazenar o tipo de acesso do usuário
usuario_role = None

def carregar_acessos():
    """Função para carregar os acessos dos usuários a partir de um arquivo JSON."""
    with open("user.json", "r", encoding="utf-8") as user_file:
            acessos = json.load(user_file)
            return json.load(user_file)
    
def verificar_acesso(usuario):
    """Função para verificar o tipo de acesso do usuário."""
    acessos = carregar_acessos()
    for u in acessos["usuarios"]:
        if u["login"] == usuario:
            return u["tipo_acesso"]
        
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
    global usuario_logado, usuario_role
    while not usuario_logado:
        print("=== Página de Login ===")
        print("1. Fazer Login")
        print("0. Sair")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            usuario_logado = input("Digite seu login: ").strip()
            if not usuario_logado:
                print("O login não pode estar vazio. Tente novamente.")
            else:
                usuario_role = verificar_acesso(usuario_logado)
                if usuario_role:
                    print(f"Bem-vindo, {usuario_logado}! Seu papel é: {usuario_role}.")
                senha = input("Digite sua senha: ").strip()
                if not senha:
                    print("A senha não pode estar vazia. Tente novamente.")
                    usuario_logado = None
                else:
                    print("Usuário não encontrado. Tente novamente.")
                    usuario_logado = None
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
        print("2. Perguntas Frequentes sobre LGPD")
        print("0. Voltar ao Menu Principal")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == "1":
            security1()
        elif escolha == "2":
            security_faq()
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

def security_faq():
    while True:
        """Função para exibir perguntas frequentes sobre LGPD."""
        print("=== Perguntas Frequentes sobre LGPD ===")
        print("1. O que é a LGPD?")
        print("2. Quais dados são coletados?")
        print("3. Como posso corrigir meus dados?")
        print("4. Como posso excluir meus dados?")
        print("0. Voltar ao Menu de Segurança")
        escolha = input("Escolha uma opção: ").strip()
        if escolha == 1:
            print("A LGPD é a Lei Geral de Proteção de Dados, que visa garantir a privacidade dos dados pessoais.")
        elif escolha == 2:
            print("Coletamos dados como nome, email, e outros dados necessários para prestar nossos serviços.")
        elif escolha == 3:
            print("Você pode corrigir seus dados entrando em contato com o suporte.")
        elif escolha == 4:
            print("Você pode solicitar a exclusão dos seus dados entrando em contato com o suporte.")
        elif escolha == 5:
            print("Voltando ao Menu de Segurança...")


def menu():
    """Função para exibir o menu principal."""
    global usuario_logado, usuario_role
    print(f"\nUsuário logado: {usuario_logado}")
    print("=== Menu Principal ===")
    print("1. Menu de Cursos Disponíveis")
    if usuario_role == "admin":
        print("2. Gerenciar Usuários")
    print("0. Sair")
    escolha = input("Escolha uma opção: ")
    if escolha == "1":
        menu_cursos()
    elif escolha == "2" and usuario_role == "admin":
        print("Acesso ao Gerenciamento de Usuários.")
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


