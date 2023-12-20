
---

# Testando as Rotas no Swagger - Usuário (Garanta que o banco ao Testar Esteja Vazio)


### **1. Criar um Novo Usuário**

- Clique na rota `POST /usuarios` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira os detalhes do novo usuário nos campos fornecidos. Exemplo de JSON:

- adm:
```json
{
  "nome": "adm test",
  "tipo_id": 1,
  "email": "adm.test@example.com",
  "senha": "senhaadm"
}
```

- cliente(por padrão o cliente é sempre tipo_id = 2 ):
```json
{
  "nome": "cliente test",
  "email": "cliente.test@example.com",
  "senha": "senhacliente"
}
```

- Clique em "Execute" para enviar a requisição.

### **2. Obter um Usuário Pelo seu ID**

- Clique na rota `GET /usuarios/{user_id}` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira o ID do usuário que deseja obter nos campos fornecidos. Exemplo de JSON:

- adm:
```json
{
  "user_id": 1
}
```
- cliente:
```json
{
  "user_id": 2
}
```
- Clique em "Execute" para enviar a requisição.

### **3. Atualizar um Usuário Existente**

- Clique na rota `PUT /usuarios/{user_id}` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira o ID do usuário que deseja atualizar nos campos fornecidos. Exemplo de JSON:

- adm:
```json
{
  "user_id": 1,
  "nome": "adm test Jr.",
  "email": "adm.test.jr@example.com"
}
```
- cliente:
```json
{
  "user_id": 2,
  "nome": "cliente test Jr.",
  "email": "cliente.test.jr@example.com"
}
```

- Clique em "Execute" para enviar a requisição.

### **4. Deletar um Usuário Existente**

- Clique na rota `DELETE /usuarios/{user_id}` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira o ID do usuário que deseja deletar nos campos fornecidos. Exemplo de JSON:

- adm
```json
{
  "user_id": 1
}
```
- cliente 
```json
{
  "user_id": 2
}
```

- Clique em "Execute" para enviar a requisição.

### **5. Obter Todas as Reservas de um Usuário**

- Clique na rota `GET /usuarios/{user_id}/reservas` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira o ID do usuário que deseja obter as reservas nos campos fornecidos. Exemplo de JSON:

- adm
```json
{
  "user_id": 1
}
```

- cliente 
```json
{
  "user_id": 2
}
```

- Clique em "Execute" para enviar a requisição.

### **6. Obter Todas as Áreas de um Usuário**

- Clique na rota `GET /usuarios/{user_id}/areas` para expandi-la.

- Em seguida, clique no botão "Try it out".

- Insira o ID do usuário que deseja obter as áreas nos campos fornecidos. Exemplo de JSON:

- adm
```json
{
  "user_id": 1
}
```

- cliente 
```json
{
  "user_id": 2
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
