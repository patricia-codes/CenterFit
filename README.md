🛍️ CenterFit

CenterFit é um projeto de loja virtual de roupas esportivas desenvolvido em grupo durante o curso Python II – Desenvolvendo Aplicações Web (SENAC).

O objetivo do projeto é aplicar os conceitos de Python, Django, HTML, CSS e banco de dados SQLite, criando uma aplicação web funcional e escalável.

Tecnologias utilizadas

Python
 🐍

Django
 🌐

SQLite
 🗄️

HTML5 & CSS3
 🎨

 JavaScript

Replit
 💻

 Funcionalidades

✔️ Cadastro e gerenciamento de produtos
✔️ Cadastro de marcas
✔️ Visualização dos itens disponíveis na loja
✔️ Estrutura inicial de e-commerce (frontend e backend)
✔️ Banco de dados integrado (SQLite)

📂 Estrutura do projeto
CenterFit/
│── centerfit/         # Aplicação principal
│── django_project/    # Configuração do projeto Django
│── marcas/            # App para cadastro de marcas
│── produtos/          # App para cadastro de produtos
│── db.sqlite3         # Banco de dados SQLite
│── manage.py          # Comando principal do Django
│── README.md          # Documentação do projeto

▶️ Como executar o projeto

Clone este repositório:

git clone https://github.com/patricia-codes/CenterFit.git


Acesse a pasta do projeto:

cd CenterFit


Crie um ambiente virtual e instale as dependências:

python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
pip install -r requirements.txt


(Se não houver requirements.txt, instalar manualmente django)

pip install django


Rode as migrações:

python manage.py migrate


Inicie o servidor:

python manage.py runserver


👩‍💻 Autores

Este projeto foi desenvolvido em grupo como parte do curso do SENAC – Python II - Desenvolvendo Aplicações Web.

Integrantes:

Patrícia de Oliveira da Silva Rocha,
Laís Regina de Oliveira Silva,
Fabiano Reis Touro e 
André Manteiga de Souza.

📜 Licença

Este projeto foi criado para fins educacionais e não possui fins comerciais.
