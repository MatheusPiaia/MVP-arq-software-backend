# Índice

* [Instalação](#-instalação)
* [Descrição](#descrição)
* [Banco de Dados](#️-banco-de-dados)
* [Acessos](#-acessos)
* [Funcionalidades](#funcionalidades)
* [Tecnologias Utilizadas](#-tecnologias-utilizadas)
* [Autor](#autor)
# MVP-Arquitetura-de-Software

# 🎲 Instalação

Clonar o repositório do frontend e do backend na mesma pasta do computador utilizando
```
mkdir "meu-projeto"
cd meu-projeto
git clone https://github.com/MatheusPiaia/MVP-arq-software-frontend.git frontend
git clone https://github.com/MatheusPiaia/MVP-arq-software-backend.git backend
```
Garantir que o projeto fique no padrão:
```
meu-projeto/
├── backend/
└── frontend/
```
Acessar então a pasta frontend e executar:
```
cd frontend
docker compose up --build
```
Esse comando irá:
- Criar o banco PostgreSQL
- Executar as migrations
- Executar o seed inicial (roles + usuário admin)
- Subir a API Flask

Abra o http://localhost:5173 no navegador para acessar a homepage da aplicação. 

Abra o http://localhost:5000 no navegador para verificar a documentação da API em execução

Após a segunda execução seguir:
```
cd frontend
docker compose up -d
```

# Descrição
Aplicação backend desenvolvida em Flask como MVP para a Sprint de Arquitetura de Software.
Aplicação possui o objetivo de facilitar controle de estoque e de condicionais de uma loja de roupas online.
Abaixo segue arquitetura utilizada:
![arquitetura](https://github.com/user-attachments/assets/ff57b81d-75aa-4e95-8acb-358a5b94237a)

Foi utilizada a API externa da FakeStore para obter os produtos de exemplo da loja online

# 🗄️ Banco de Dados

- PostgreSQL: localhost:5432
- PgAdmin: http://localhost:5050
    Email: admin@admin.com
    Senha: admin

# 🌐 Acessos
-Frontend:
http://localhost:5173

-Backend (API):
http://localhost:5000

-Swagger:
http://localhost:5000/openapi/swagger#

-PgAdmin:
http://localhost:5050

# Funcionalidades
- [x] Cadastro de Clientes
- [x] Importação dos produtos pela FakeStore
- [x] Módulo de controle de estoque
- [x] Cadastro de condicionais
- [x] Adição de itens aos condicionais
- [x] Retorno dos condicionais, informando produtos devolvidos e comprados
- [x] Lógica controle de estoque para atualização em tempo real
- [x] Filtros dinâmicos
- [ ] Adição manual de novos produtos
- [ ] Autenticação

Após a Execução da API é possível acessar a documentação via Swagger e verificar/testar todas as funcionalidades da aplicação.

Abaixo segue todas as rotas da API
![rotas api](https://github.com/user-attachments/assets/b1f4d847-f235-4918-aef3-e1ddee91f871)
![rotas api](https://github.com/user-attachments/assets/d3350cfb-d894-4018-a82e-9bfefc5ecf27)

Utilizado Pydantic para padronizar as respostas pelos schemas, como o exemplo abaixo
![Schema Response](https://github.com/user-attachments/assets/4e2ad4ce-aafd-446d-a9e1-f5e38368d6c3)
![Schema Response](https://github.com/user-attachments/assets/f2e3a29b-e97d-4514-bffc-f97e4ca16d67)




# 🛠 Tecnologias utilizadas
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/)
- [Flask-Migrate (Alembic)](https://flask-migrate.readthedocs.io/en/latest/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [OpenAPI3](https://swagger.io/solutions/getting-started-with-oas/)

# Autor
---

<a href="https://github.com/MatheusPiaia">
 <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/185968337?s=400&u=b4f54f3c5ea4b83b959d508547adf7077fd2caf8&v=4" width="100px;" alt=""/>
 <br/></a> 

 [![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/MatheusPiaia)
 [![LinkedIn](https://img.shields.io/badge/LinkedIn-Matheus-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/matheus-piaia-231647144)
