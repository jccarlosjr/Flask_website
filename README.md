# Flask Blog

Este é um projeto de blog desenvolvido com Flask e Python. Ele permite que os usuários criem contas, façam login, editem seus perfis e publiquem posts no blog. Além disso, os usuários podem visualizar posts de outros usuários e excluir posts próprios.

## Requisitos

Antes de começar, certifique-se de ter o seguinte instalado:

- Python 3.7 ou superior
- pip (gerenciador de pacotes do Python)
- Virtualenv (recomendado para criar um ambiente virtual isolado)

## Instalação

Siga as etapas abaixo para configurar o ambiente de desenvolvimento:

1. **Clone o repositório:**

   ```bash
   git clone https://github.com/jccarlosjr/Flask_website.git

2. **Navegue até o diretório do projeto:**

   ```bash
   cd flask-blog

3. **Crie e ative o ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use: venv\Scripts\activate

4. **Navegue até o diretório do projeto:**

   ```bash
   pip install -r requirements.txt

5. **Crie o banco de dados:**

   ```bash
   flask shell

6. **No prompt do Python, execute:**

   ```bash
   from comunidadeimpressionadora import database
   database.create_all()
   exit()


6. **Execute o projeto:**

   ```bash
   flask run

## Funcionalidades

- Cadastro e Login: Os usuários podem criar uma conta e fazer login.
- Edição de Perfil: Os usuários podem editar suas informações de perfil e foto.
- Criação e Edição de Posts: Os usuários podem criar e editar posts.
- Exclusão de Posts: Os usuários podem excluir seus próprios posts.
- Listagem de Usuários: Os usuários podem visualizar uma lista de todos os usuários cadastrados.
