# instale o poetry:

https://python-poetry.org/


# comandos do poetry:
- ativa o ambiente virtual
```
poetry shell 
```
- instala as dependencias
```
poetry install 
```


# Para subir a imagem do banco com o docker:

```
task docker
```

# Para aplicar as migrações ja feitas no alembic(localhost favor usar o .env_exemplo como env):

```
  alembic upgrade head
```

# para qualquer alteração dos modelos de Usuario/Reserva/Area é necessario criar uma nova migração no alembic:

```
  alembic revision --autogenerate -m "descrição_significativa"
```

- Gera automaticamente uma nova revisão/migração baseada nas diferenças detectadas entre o estado atual do banco de dados e os modelos declarativos(model).

# Para iniciar o servidor((localhost favor usar o .env_exemplo como env))

```
uvicorn app.main:app --reload  
```

- link do servidor: http://127.0.0.1:8000/

# Etapas para testar rotas usando o swagger do FastApi:

1. Garanta que o servidor esteja rodando:

   - Entre no link: http://127.0.0.1:8000/docs:

   1. [Para testar as rotas de Usuario é necessario criar um tipo de usuario](test/swagger/tipo_usuario.md)
   2. [Para testar as rotas de Usuario](test/swagger/usuario.md)
   3. [Para testar as rotas de Area](test/swagger/area.md)
   4. [Para testar as rotas de Reserva](test/swagger/reserva.md)


# Dockerizando a aplicação(localhost favor usar o .env_exemplo_compose como env):
Para iniciar sua aplicação e o banco de dados PostgreSQL juntos usando o Docker Compose, você pode usar o seguinte comando no terminal:

```
docker-compose up

#ou se quiser executar em segundo plano:

docker-compose up -d
```
Este comando irá iniciar todos os serviços definidos no arquivo docker-compose.yml. O Docker Compose cuidará de iniciar os serviços na ordem correta, de acordo com as dependências definidas no arquivo. Neste caso, o serviço banco será iniciado antes do serviço app porque o serviço app depende do banco.

já para parar todos os serviços:
```
docker-compose down
```

## Para ativar o versionamento do banco com o alembic no docker:
Embora o docker-compose já tenha um comando explicito de subir a versão do banco por meio do alembic upgrade head as vezes é necessario modificar o versionamento na mão para isso é necessario executar o Alembic por meio do comando abaixo, você precisará executar comandos dentro do contêiner da sua aplicação. Você pode fazer isso usando o comando docker-compose exec. Por exemplo, para executar uma migração do Alembic, você pode usar o seguinte comando:

```
docker-compose exec app poetry run alembic upgrade head
```

Neste comando, app é o nome do serviço da sua aplicação no arquivo docker-compose.yml, e poetry run alembic upgrade head é o comando que você quer executar dentro do contêiner.

Se você precisar gerar uma nova revisão de migração, você pode usar um comando semelhante:
```
docker-compose exec app poetry run alembic revision -m "descrição_significativa"
```

---

