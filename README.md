# Para subir a imagem do banco( eu tive que trocar para a porta 5439 pois meu pc ja tem um banco com 5438 ):

docker run -d -p 5439:5432 -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=postgres postgres:latest

# para aplicar as migrações ja feitas no alembic:
  ```
  alembic upgrade head
  ```

# para criar uma nova migração no alembic:
  ```
  alembic revision --autogenerate -m "descrição_significativa"
  ```
Gera automaticamente uma nova revisão/migração baseada nas diferenças detectadas entre o estado atual do banco de dados e os modelos declarativos(model).

# Etapas para testar algumas rota usando o Postman:

1. **Rota POST /usuarios para criar um usuário**:
    - Defina o método HTTP como POST.
    - Insira a URL: `http://localhost:8000/usuarios`
    - Na guia "Body", selecione "raw" e "JSON", e insira o corpo da solicitação. Por exemplo:
    ```json
    {
        "id": "123e4567-e89b-12d3-a456-426614174000",
        "nome": "teste",
        "email": "teste@email.com",
        "senha": "senha"
    }
    ```
    - Clique em "Send" para enviar a solicitação.

2. **Rota POST /token para obter um token de acesso**:
    - Defina o método HTTP como POST.
    - Insira a URL: `http://localhost:8000/token`
    - Na guia "Body", selecione "x-www-form-urlencoded", e insira o nome de usuário e a senha. Por exemplo:
        - Key: `username`, Value: `teste@email.com`
        - Key: `password`, Value: `senha`
    - Clique em "Send" para enviar a solicitação. Copie o token de acesso da resposta.

3. **Rota POST /areas para criar uma área**:
    - Defina o método HTTP como POST.
    - Insira a URL: `http://localhost:8000/areas`
    - Na guia "Headers", insira o cabeçalho de autorização. Key: `Authorization`, Value: `Bearer COLE_AQUI_SEU_TOKEN`
    - Na guia "Body", selecione "raw" e "JSON", e insira o corpo da solicitação. Por exemplo:
    ```json
    {
        "id": "223e4567-e89b-12d3-a456-426614174000",
        "nome": "Area 1",
        "disponivel": true,
        "descricao": "Descricao da area",
        "iluminacao": "boa",
        "tipo_piso": "concreto",
        "covered": "sim",
        "foto_url": "url_da_foto"
    }
    ```
    - Clique em "Send" para enviar a solicitação.

4. **Rota GET /areas/{area_id} para obter uma área**:
    - Defina o método HTTP como GET.
    - Insira a URL, substituindo `{area_id}` pelo ID da área que você criou: `http://localhost:8000/areas/223e4567-e89b-12d3-a456-426614174000`
    - Clique em "Send" para enviar a solicitação.

5. **Rota PUT /areas/{area_id} para atualizar uma área**:
    - Defina o método HTTP como PUT.
    - Insira a URL, substituindo `{area_id}` pelo ID da área que você criou: `http://localhost:8000/areas/223e4567-e89b-12d3-a456-426614174000`
    - Na guia "Headers", insira o cabeçalho de autorização. Key: `Authorization`, Value: `Bearer COLE_AQUI_SEU_TOKEN`
    - Na guia "Body", selecione "raw" e "JSON", e insira o corpo da solicitação com os novos valores para a área.
    - Clique em "Send" para enviar a solicitação.

6. **Rota DELETE /areas/{area_id} para deletar uma área**:
    - Defina o método HTTP como DELETE.
    - Insira a URL, substituindo `{area_id}` pelo ID da área que você criou: `http://localhost:8000/areas/223e4567-e89b-12d3-a456-426614174000`
    - Na guia "Headers", insira o cabeçalho de autorização. Key: `Authorization`, Value: `Bearer COLE_AQUI_SEU_TOKEN`
    - Clique em "Send" para enviar a solicitação.


7. **Rota POST /reservas para criar uma reserva**:
    - Defina o método HTTP como POST.
    - Insira a URL: `http://localhost:8000/reservas`
    - Na guia "Headers", insira o cabeçalho de autorização. Key: `Authorization`, Value: `Bearer COLE_AQUI_SEU_TOKEN`
    - Na guia "Body", selecione "raw" e "JSON", e insira o corpo da solicitação. Por exemplo:
    ```json
    {
        "id": "323e4567-e89b-12d3-a456-426614174000",
        "valor": 100,
        "reserva_data": "2023-12-01T00:00:00Z",
        "hora_inicio": "2023-12-01T08:00:00Z",
        "hora_fim": "2023-12-01T10:00:00Z",
        "justificacao": "Justificativa da reserva",
        "reserva_tipo": "Tipo da reserva",
        "status": "Ativa",
        "area_id": "223e4567-e89b-12d3-a456-426614174000",
        "usuario_id": "123e4567-e89b-12d3-a456-426614174000"
    }
    ```
    - Clique em "Send" para enviar a solicitação.

8. **Rota GET /reservas/{reservation_id} para obter uma reserva**:
    - Defina o método HTTP como GET.
    - Insira a URL, substituindo `{reservation_id}` pelo ID da reserva que você criou: `http://localhost:8000/reservas/323e4567-e89b-12d3-a456-426614174000`
    - Clique em "Send" para enviar a solicitação.

9. **Rota PUT /reservas/{reservation_id} para atualizar uma reserva**:
    - Defina o método HTTP como PUT.
    - Insira a URL, substituindo `{reservation_id}` pelo ID da reserva que você criou: `http://localhost:8000/reservas/323e4567-e89b-12d3-a456-426614174000`
    - Na guia "Headers", insira o cabeçalho de autorização. Key: `Authorization`, Value: `Bearer COLE_AQUI_SEU_TOKEN`
    - Na guia "Body", selecione "raw" e "JSON", e insira o corpo da solicitação com os novos valores para a reserva.
    - Clique em "Send" para enviar a solicitação.

10. **Rota DELETE /reservas/{reservation_id} para deletar uma reserva**:
    - Defina o método HTTP como DELETE.
    - Insira a URL, substituindo `{reservation_id}` pelo ID da reserva que você criou: `http://localhost:8000/reservas/323e4567-e89b-12d3-a456-426614174000`
    - Na guia "Headers", insira o cabeçalho de autorização. Key: `Authorization`, Value: `Bearer COLE_AQUI_SEU_TOKEN`
    - Clique em "Send" para enviar a solicitação.

