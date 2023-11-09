# Para subir a imagem do banco com o docker(puramente):

```
docker run -d -p 5439:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres postgres:latest
```

# Para aplicar as migrações ja feitas no alembic:

```
  alembic upgrade head
```

# para qualquer alteração dos modelos de Usuario/Reserva/Area é necessario criar uma nova migração no alembic:

```
  alembic revision --autogenerate -m "descrição_significativa"
```

- Gera automaticamente uma nova revisão/migração baseada nas diferenças detectadas entre o estado atual do banco de dados e os modelos declarativos(model).

# Para iniciar o servidor

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



---

> [!WARNING]
> FIXME: (ERRO expression 'TipoUser' failed to locate a name ('TipoUser'))