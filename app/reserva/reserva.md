
---

# Testando as Rotas no Swagger - Reserva 

# garanta que ja tenha uma area criada é se possivel use o mesmo id [ 0e398c13-163c-4939-a68b-39b21e10c2c7 ]

### 1. Criar uma Nova Reserva
Cria uma nova reserva com os detalhes fornecidos.

- **Método:** POST
- **Endpoint:** `/reservas`
- **Corpo da Requisição (JSON):** 
```json
{
  "id": "2c5f7a10-0d57-45b2-82da-df16d2075ef9",
  "valor": null,  /* O valor será calculado automaticamente com base nas horas de início e fim */
  "reserva_data": "2023-10-23T12:00:00",
  "hora_inicio": "2023-10-23T14:00:00",
  "hora_fim": "2023-10-23T16:00:00",
  "justificacao": "Jogo de Equipe",
  "reserva_tipo": "Jogo",
  "status": "Em análise",
  "area_id": "0e398c13-163c-4939-a68b-39b21e10c2c7",
  "usuario_id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b"
}
```

### 2. Visualizar Todas as Reservas
Retorna uma lista de todas as reservas.

- **Método:** GET
- **Endpoint:** `/reservas`

### 3. Visualizar Reservas Disponíveis
Retorna uma lista de todas as reservas disponíveis.

- **Método:** GET
- **Endpoint:** `/reservas/disponiveis`

### 4. Visualizar Reserva Pelo ID
Retorna os detalhes da reserva correspondente ao ID fornecido.

- **Método:** GET
- **Endpoint:** `/reservas/{reservation_id}`
- **Substituir `{reservation_id}` pelo ID da reserva desejada**
  - Exemplo: `/reservas/2c5f7a10-0d57-45b2-82da-df16d2075ef9`

### 5. Atualizar os Detalhes de uma Reserva
Atualiza os detalhes de uma reserva existente.

- **Método:** PUT
- **Endpoint:** `/reservas/{reservation_id}`
- **Substituir `{reservation_id}` pelo ID da reserva a ser atualizada**
- **Corpo da Requisição (JSON):** 
```json
{
  "id": "2c5f7a10-0d57-45b2-82da-df16d2075ef9",
  "valor": null,  /* O valor será calculado automaticamente com base nas horas de início e fim */
  "reserva_data": "2023-10-25T12:00:00",
  "hora_inicio": "2023-10-25T14:00:00",
  "hora_fim": "2023-10-25T16:00:00",
  "justificacao": "Jogo de Equipe Atualizada",
  "reserva_tipo": "Jogo",
  "status": "Confirmada", /* O status será definido automaticamente com base em que? */
  "area_id": "0e398c13-163c-4939-a68b-39b21e10c2c7",
  "usuario_id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b" /* O Usuario tbm não precisa ser o mesmo que criou area.*/
}
```

### 6. Deletar uma Reserva
Deleta a reserva correspondente ao ID fornecido.

- **Método:** DELETE
- **Endpoint:** `/reservas/{reservation_id}`
- **Substituir `{reservation_id}` pelo ID da reserva a ser deletada**
  - Exemplo: `/reservas/2c5f7a10-0d57-45b2-82da-df16d2075ef9`

### 7. Visualizar Reservas do Usuário Atual
Retorna uma lista de todas as reservas associadas ao usuário autenticado.

- **Método:** GET
- **Endpoint:** `/usuario/reservas`

### 8. Visualizar Reserva do Usuário Atual Pelo ID
Retorna os detalhes da reserva associada ao usuário autenticado correspondente ao ID fornecido.

- **Método:** GET
- **Endpoint:** `/usuario/reservas/{reservation_id}`
- **Substituir `{reservation_id}` pelo ID da reserva desejada

**
  - Exemplo: `/usuario/reservas/2c5f7a10-0d57-45b2-82da-df16d2075ef9`

---

<div style="color:red;">
<strong>Erros detectados:</strong> 

- 