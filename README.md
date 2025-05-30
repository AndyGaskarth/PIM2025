# 🌐 TecEducations – Plataforma de Ensino Digital Seguro

Bem-vindo ao repositório oficial do nosso Projeto Integrador Multidisciplinar (PIM) do curso de Análise e Desenvolvimento de Sistemas da UNIP (2025). Este projeto simula uma plataforma educacional voltada para ONGs, com foco em **inclusão digital**, **segurança da informação** e **proteção de dados conforme a LGPD**.

## 🎯 Objetivo

Criar uma plataforma em Python acessível, funcional e segura para auxiliar ONGs a oferecerem cursos online de forma prática e intuitiva, respeitando boas práticas de cibersegurança e a Lei Geral de Proteção de Dados (LGPD).

## 👥 Integrantes do grupo

- Anderson Souza Pimentel Novais
- Eloisa Morioka
- Matheus Costa Pontes de Almeida
- Cauã Bernardo Barbosa
- Paulo Cezar Silva dos Santos
- Pedro Henrique Honorato Lima D

## 🚀 Funcionalidades da Plataforma

- Cadastro e login com autenticação segura (`bcrypt`)
- Criptografia dos dados sensíveis (`Fernet`)
- Registro de acessos por log
- Sistema de cursos com visualização e progresso
- Estatísticas por usuário e gerais
- Exportação de dados para Excel (.xlsx)
- Menu interativo com interface Tkinter
- Menu de segurança digital e LGPD (com exclusão de dados)
- Sistema com diferentes níveis de acesso: aluno, professor e admin

## 🔐 Segurança e LGPD

- Senhas protegidas com hashing seguro (`bcrypt`)
- Dados como nome, idade e sobrenome criptografados antes do armazenamento
- Consentimento obrigatório para coleta de dados
- Visualização, correção e exclusão dos próprios dados
- Acesso aos logs e estatísticas limitado por nível de permissão

## 📁 Estrutura do Projeto

📦PIM2025/
 ┣ 📜PIM.py
 ┣ 📜usuarios.json
 ┣ 📜cursos/
 ┣ 📜acessos.log
 ┣ 📜chave.key
 ┣ 📜README.md
 ┗ 📁exportações/

## Aprendizados
Esse projeto foi fundamental para aplicar o que vimos nas aulas de programação, estatística, segurança e privacidade. Desenvolvemos tanto a parte técnica quanto a consciência sobre o uso responsável de dados.
