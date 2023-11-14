from pydantic import BaseModel, ConfigDict


class UsuarioCreate(BaseModel):
    nome: str
    tipo_id: int
    email: str
    senha: str
    model_config = ConfigDict(from_attributes=True)


class UsuarioBase(UsuarioCreate):
    id: int


class UsuarioList(BaseModel):
    users: list[UsuarioBase]
