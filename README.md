# Índice

* [Instalação](#-instalação)
* [Descrição](#descrição)
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
```
cd frontend
docker compose up --build
```

Abra o http://localhost:5173 no navegador para acessar a homepage da aplicação. 
Abra o http://localhost:5000 no navegador para verificar a documentação da API em execução

# Descrição
Aplicação desenvolvida como MVP para a Sprint: 

E para avaliação foi utilizado o parâmetro de Acurácia, aonde o Random Forest (RF) se mostrou melhor, com 93,92% de acurácia.
O dataset utilizado foi retirado do site [Kagle](https://www.kagle.com/datasets/rakeshkapilavai/extrovert-vs-introvert-behavior-data)

# Funcionalidades
- [x] Cadastro de Usuário
- [x] Predição da personalidade (Introvertido/Extrovertido)

Após a Execução da API é possível acessar a documentação via Swagger e verificar/testar todas as funcionalidades da aplicação.
Abaixo segue todas as rotas da API
![rotas api](https://github.com/user-attachments/assets/f75eccdd-10c3-4d5f-991d-3cb3e9841f29)



# 🛠 Tecnologias utilizadas
- [Python](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/en/stable/)
- [Pydantic](https://docs.pydantic.dev/latest/)
- [OpenAPI3](https://swagger.io/solutions/getting-started-with-oas/)

# Autor
---

<a href="https://github.com/MatheusPiaia">
 <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/185968337?s=400&u=b4f54f3c5ea4b83b959d508547adf7077fd2caf8&v=4" width="100px;" alt=""/>
 <br/></a> 

 [![GitHub](https://badgen.net/badge/icon/github?icon=github&label)](https://github.com/MatheusPiaia)
 [![LinkedIn](https://img.shields.io/badge/LinkedIn-Matheus-blue?style=flat&logo=linkedin)](https://www.linkedin.com/in/matheus-piaia-231647144)
