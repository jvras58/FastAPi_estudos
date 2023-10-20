# Para subir a imagem do banco com o docker(puramente):

```
docker run -d -p 5439:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres postgres:latest
```

# Para subir a imagem do banco com o docker mais utilizando task do poetry(não esta funcionando ainda):

```
task subirdocker
```

# Para aplicar as migrações ja feitas no alembic:

```
  alembic upgrade head
```

# Para iniciar o servidor

```
uvicorn app.main:app --reload  
```

# para qualquer alteração dos modelos de user/reserva/area é necessario criar uma nova migração no alembic:

```
  alembic revision --autogenerate -m "descrição_significativa"
```

- Gera automaticamente uma nova revisão/migração baseada nas diferenças detectadas entre o estado atual do banco de dados e os modelos declarativos(.model).

# Erros detectados nas rotas:

- Sem Erro detectado
