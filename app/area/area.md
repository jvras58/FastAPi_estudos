# Testando as Rotas no Swagger - Reserva

# garanta que ja tenha um usuario criado


### 1. Criar uma Nova Área
Cria uma nova área com os detalhes fornecidos.

- **Método:** POST
- **Endpoint:** `/areas`
- **Corpo da Requisição (JSON):** 
```json
{
  "id": "0e398c13-163c-4939-a68b-39b21e10c2c7",
  "nome": "Quadra de volei",
  "descricao": "Uma quadra de volei espaçosa",
  "iluminacao": "LED",
  "tipo_piso": "Liso",
  "covered": "Sim",
  "foto_url": "https://example.com/quadra_volei.jpg",
  "usuario_id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b"
}
```

### 2. Visualizar Todas as Áreas
Retorna uma lista de todas as áreas.

- **Método:** GET
- **Endpoint:** `/areas`

### 3. Visualizar Área Pelo Nome
Retorna a área correspondente ao nome fornecido.

- **Método:** GET
- **Endpoint:** `/areas/nome/{nome}`
- **Substituir `{nome}` pelo nome da área desejada**
  - Exemplo: `/areas/nome/Quadra%20de%20volei`

### 4. Visualizar Todas as Áreas Disponíveis
Retorna uma lista de todas as áreas disponíveis.

- **Método:** GET
- **Endpoint:** `/areas/disponiveis`

### 5. Visualizar Área Pelo ID
Retorna os detalhes da área correspondente ao ID fornecido.

- **Método:** GET
- **Endpoint:** `/areas/{area_id}`
- **Substituir `{area_id}` pelo ID da área desejada**
  - Exemplo: `/areas/0e398c13-163c-4939-a68b-39b21e10c2c7
0e398c13-163c-4939-a68b-39b21e10c2c7`

### 6. Atualizar os Detalhes de uma Área
Atualiza os detalhes de uma área existente.

- **Método:** PUT
- **Endpoint:** `/areas/{area_id}`
- **Substituir `{area_id}` pelo ID da área a ser atualizada**
- **Corpo da Requisição (JSON):** 
```json
{
  "id": "0e398c13-163c-4939-a68b-39b21e10c2c7",
  "nome": "Quadra de volei",
  "descricao": "Uma quadra de volei pequena",
  "iluminacao": "LED Inteligente",
  "tipo_piso": "Cimento",
  "covered": "Sim",
  "foto_url": "https://example.com/quadra_volei.jpg",
  "usuario_id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b"
}
```

### 7. Deletar uma Área
Deleta a área correspondente ao ID fornecido.

- **Método:** DELETE
- **Endpoint:** `/areas/{area_id}`
- **Substituir `{area_id}` pelo ID da área a ser deletada**
  - Exemplo: `/areas/0e398c13-163c-4939-a68b-39b21e10c2c7`


- ERROS DETECTADOS NAS ROTAS DE AREA:

1 - /areas/{area_id} [update] (# FIXME: ESSA ROTA NÃO TA BEM COM UM PROBLEMA KK (TIPO ELA TA PEGANDO MAS NO RESPONSE BODY DEPOIS DO EXECUTE ELA NÃO MOSTRA O QUE FOI MUDADO MOSTRA UM {} SÓ...))

2- ROTA DESATIVADA: /areas/disponiveis [get] (# FIXME: FOI RETIRADO ESSA COLUNA CHAMADA DISPONIVEL... não temos o que fazer com ela pq não tem nada parecido com algo que diga que está disponivel....)