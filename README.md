
<h1 align="center">
  <a href="#">Projeto de Estudos com FASTAPI</a>
</h1>

<p align="center">
  <a href="#memo-requisitos">Requisitos</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#rocket-tecnologias">Tecnologias</a>&nbsp;&nbsp;&nbsp;|&nbsp;&nbsp;&nbsp;
  <a href="#information_source-como-usar">Como usar</a>
</p>

## :memo: Requisitos

| Ferramenta                                         | Versão  | Descrição                                   |
| -------------------------------------------------- | ------- | ------------------------------------------- |
| [Poetry](https://python-poetry.org/)               | -       | gerenciador dependências em projetos Python |
| [Python](https://www.python.org/)                  | -       | Linguagem de desenvolvimento                |
| [Git](https://git-scm.com)                         | -       | Controle de versões                         |
| [SQLite](https://sqlite.org/)                      | -       | Sistema de gerenciamento de banco de dados  |
| [Docker](https://sqlite.org/)                      | -       | Sistema de gerenciamento de banco de dados  |


## :rocket: Tecnologias

Este projeto está sendo desenvolvido com:

- Gerenciador: [Poetry](https://python-poetry.org/)
- Linguagem e ambiente: [Python](https://www.python.org/)
- Object-Relation-Mapper (ORM): [SQLAlchemy](https://www.sqlalchemy.org/)
- Banco de dados: [SQLite](https://sqlite.org/)


## :information_source: Como usar

```bash
# Clonar este repositório
$ git clone git@github.com:jvras58/FastAPi_estudos.git

# Ir para o repositório
$ cd back-fastapi  

# Criar o arquivo .env com os valores adequados ao ambiente. pasta .secrets precisa ter (TESTE_SECRET).
$ cp .env-semple .env

# Entre no ambiente virtual
$ poetry shell

# Instalar as dependências
$ poetry install

# Executar as migrations
  $ alembic upgrade head

# Executar a api
$ task run
```

- Endereço local: (http://localhost:8000)


---

### Docker & Docker-compose

O projeto possui um docker-compose.yml para o banco de dados, ambiente de desenvolvimento. Para utilizar basta ter o docker-compose instalado e seguir os seguintes comandos:

```bash
# Ativar o banco de dados pelo docker-compose (sem o -d [modo interativo])
$ docker compose up -d
# Desativar o banco de dados pelo docker-compose
$ docker compose down
```


## Para ativar o versionamento do banco com o alembic no docker:
Embora o docker-compose já tenha um comando explicito de subir a versão do banco por meio do alembic upgrade head as vezes é necessario modificar o versionamento na mão para isso é necessario executar o Alembic por meio do comando abaixo, você precisará executar comandos dentro do contêiner da sua aplicação. Você pode fazer isso usando o comando docker-compose exec. Por exemplo, para executar uma migração do Alembic, você pode usar o seguinte comando:

```bash
$ docker compose exec app poetry run alembic upgrade head
```

Neste comando, app é o nome do serviço da sua aplicação no arquivo docker-compose.yml, e poetry run alembic upgrade head é o comando que você quer executar dentro do contêiner.

Se você precisar gerar uma nova revisão de migração, você pode usar um comando semelhante:

```bash
$ docker compose exec app poetry run alembic revision -m "descrição_significativa"
```


