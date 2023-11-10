
---

# Testando as Rotas no Swagger - Reserva 

# garanta que ja tenha uma area criada é se possivel use o mesmo id

### 1. Criar uma Nova Reserva
Cria uma nova reserva com os detalhes fornecidos.

- **Método:** POST
- **Endpoint:** `/reservas`
- **Corpo da Requisição (JSON):** 

- adm:
```json
{
  "valor": 0,  /* O valor será calculado automaticamente com base nas horas de início e fim é necessario colocar um valor fake */
  "reserva_data": "2023-10-23T12:00:00",
  "hora_inicio": "2023-10-23T14:00:00",
  "hora_fim": "2023-10-23T16:00:00",
  "justificacao": "Jogo de Equipe",
  "reserva_tipo": "Jogo",
  "status": "Em análise",
  "area_id": 1,
  "usuario_id": 1
}
```
- cliente:
```json
{
  "valor": 0,  /* O valor será calculado automaticamente com base nas horas de início e fim é necessario colocar um valor fake */
  "reserva_data": "2023-10-23T12:00:00",
  "hora_inicio": "2023-10-23T14:00:00",
  "hora_fim": "2023-10-23T16:00:00",
  "justificacao": "Jogo de Equipe",
  "reserva_tipo": "Jogo",
  "status": "Em análise",
  "area_id": 1,
  "usuario_id": 2
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
  - Exemplo: `/reservas/1`

### 5. Atualizar os Detalhes de uma Reserva
Atualiza os detalhes de uma reserva existente.

- **Método:** PUT
- **Endpoint:** `/reservas/{reservation_id}`
- **Substituir `{reservation_id}` pelo ID da reserva a ser atualizada**
- **Corpo da Requisição (JSON):** 

- adm:
```json
{
  "valor": 0,  /* O valor será calculado automaticamente com base nas horas de início e fim é necessario colocar um valor fake */
  "reserva_data": "2023-10-23T12:00:00",
  "hora_inicio": "2023-10-23T14:00:00",
  "hora_fim": "2023-10-23T16:00:00",
  "justificacao": "Jogo de Equipe",
  "reserva_tipo": "Jogo",
  "status": "Em análise",
  "area_id": 1,
  "usuario_id": 1
}
```

- cliente:
```json
{
  "valor": 0,  /* O valor será calculado automaticamente com base nas horas de início e fim é necessario colocar um valor fake */
  "reserva_data": "2023-10-23T14:00:00",
  "hora_inicio": "2023-10-23T15:00:00",
  "hora_fim": "2023-10-23T16:00:00",
  "justificacao": "Jogo de queimado",
  "reserva_tipo": "Jogo",
  "status": "Em análise",
  "area_id": 1,
  "usuario_id": 2
}
```

### 6. Deletar uma Reserva
Deleta a reserva correspondente ao ID fornecido.

- **Método:** DELETE
- **Endpoint:** `/reservas/{reservation_id}`
- **Substituir `{reservation_id}` pelo ID da reserva a ser deletada**
  - Exemplo: `/reservas/1`

### 7. Visualizar Reservas do Usuário Atual
Retorna uma lista de todas as reservas associadas ao usuário autenticado.

- **Método:** GET
- **Endpoint:** `/usuario/reservas`

### 8. Visualizar Reserva do Usuário Atual Pelo ID
Retorna os detalhes da reserva associada ao usuário autenticado correspondente ao ID fornecido.

- **Método:** GET
- **Endpoint:** `/usuario/reservas/{reservation_id}`
- **Substituir `{reservation_id}` pelo ID da reserva desejada**
- Exemplo: `/usuario/reservas/1`

---