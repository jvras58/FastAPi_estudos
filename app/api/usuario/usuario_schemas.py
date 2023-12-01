from typing import Optional

from pydantic import BaseModel, ConfigDict


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
