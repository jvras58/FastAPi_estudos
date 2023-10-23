
---

# Testando as Rotas no Swagger - Usuário


### **1. Criar um Novo Usuário**

- Clique na rota `POST /usuarios` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira os detalhes do novo usuário nos campos fornecidos. Exemplo de JSON:

```json
{
  "id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b",
  "nome": "Jonh test",
  // "tipo": "0", /* por algum motivo estou tendo erro em usar o tipo_id é a forma de passar pelo erro esta sendo aplicar o tipo diretamente dentro da entidade usuario */
  "tipo_id": "c1f949f1-3d6d-4cb1-9b0d-905b57c5e60b", /* ainda tenho que estudar como isso vai ser definido */
  "email": "john.test@example.com",
  "senha": "senha"
}
```

- Clique em "Execute" para enviar a requisição.

### **2. Obter um Usuário Pelo seu ID**

- Clique na rota `GET /usuarios/{user_id}` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira o ID do usuário que deseja obter nos campos fornecidos. Exemplo de JSON:

```json
{
  "user_id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b"
}
```

- Clique em "Execute" para enviar a requisição.

### **3. Atualizar um Usuário Existente**

- Clique na rota `PUT /usuarios/{user_id}` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira o ID do usuário que deseja atualizar nos campos fornecidos. Exemplo de JSON:

```json
{
  "user_id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b",
  "nome": "Jonh test Jr.",
  "email": "john.test.jr@example.com"
}
```

- Clique em "Execute" para enviar a requisição.

### **4. Deletar um Usuário Existente**

- Clique na rota `DELETE /usuarios/{user_id}` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira o ID do usuário que deseja deletar nos campos fornecidos. Exemplo de JSON:

```json
{
  "user_id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b"
}
```

- Clique em "Execute" para enviar a requisição.

### **5. Obter Todas as Reservas de um Usuário**

- Clique na rota `GET /usuarios/{user_id}/reservas` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira o ID do usuário que deseja obter as reservas nos campos fornecidos. Exemplo de JSON:

```json
{
  "user_id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b"
}
```

- Clique em "Execute" para enviar a requisição.

### **6. Obter Todas as Áreas de um Usuário**

- Clique na rota `GET /usuarios/{user_id}/areas` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira o ID do usuário que deseja obter as áreas nos campos fornecidos. Exemplo de JSON:

```json
{
  "user_id": "ff3be86a-5c09-4a02-a18f-94ab28e2c91b"
}
```

- Clique em "Execute" para enviar a requisição.

### **7. Atualizar a Senha do Usuário**

- Clique na rota `PUT /usuario/update_senha` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Forneça a senha atual e a nova senha nos campos fornecidos. Exemplo de JSON:

```json
{
  "new_password": "senha123",
  "old_password": "senha"
}
```

- Clique em "Execute" para enviar a requisição.

### **8. Deletar o Usuário Atualmente Autenticado**

- Clique na rota `DELETE /usuario/delete` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Clique em "Execute" para enviar a requisição.

---
