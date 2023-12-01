from pydantic import BaseModel


class TipoUserBase(BaseModel):
    id: int
    tipo: str


class TipoUserCreate(TipoUserBase):
    pass


class TipoList(BaseModel):
    tipos: list[TipoUserBase]
