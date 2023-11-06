from pydantic import BaseModel


class UsuarioCreate(BaseModel):
    nome: str
    tipo_id: int
    email: str
    senha: str


class UsuarioBase(UsuarioCreate):
    id: int


class UsuarioList(UsuarioBase):
    Usuario: list[UsuarioBase]


class Token(BaseModel):
    access_token: str
    token_type: str
