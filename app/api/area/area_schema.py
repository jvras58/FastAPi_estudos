from pydantic import BaseModel, ConfigDict


class AreaCreate(BaseModel):
    nome: str
    descricao: str
    iluminacao: str
    tipo_piso: str
    covered: str
    foto_url: str
    model_config = ConfigDict(from_attributes=True)


class AreaPublic(AreaCreate):
    pass


class AreaBase(AreaCreate):
    id: int


class AreaList(BaseModel):
    areas: list[AreaBase]
