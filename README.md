# planner-ness
Aplicação para organizar tarefas rotineiras familiar


## Instalação


Pré-requisitos:

* Python3 + pip instalados
* Ambiente virtual criado
* Django instalado - requirements.txt
* SQLite3 instalado - para usar outro banco, necessita configurar


Clone o projeto do github:

> git clone git@github.com:tsneu/planner-ness.git .

Crie as tabelas do banco de dados:

> python3 manage.py makemigrations

> python3 manage.py migrate

Crie um super usuário para acessar o ambiente admin:

> python3 manage.py createsuperuser

Rode o servidor:

> python3 manage.py runserver

