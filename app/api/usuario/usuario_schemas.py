from typing import Optional

from pydantic import BaseModel, ConfigDict


# TODO: Criado so para contemplar um teste de crud de usuario test_create_user_without_tipo_id
class UsuarioCreateWithoutTipoId(BaseModel):
    nome: str
    email: str
    senha: str


class UsuarioPublic(BaseModel):
    nome: str
    email: str


class UsuarioCreate(BaseModel):
    nome: str
    email: str
    senha: str
    tipo_id: Optional[int] = 2
    model_config = ConfigDict(from_attributes=True)


class UsuarioBase(UsuarioCreate):
    id: int


class UsuarioList(BaseModel):
    users: list[UsuarioBase]
