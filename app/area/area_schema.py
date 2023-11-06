from pydantic import BaseModel


class AreaCreate(BaseModel):
    nome: str
    descricao: str
    iluminacao: str
    tipo_piso: str
    covered: str
    foto_url: str
    # usuario_id: int




class AreaBase(AreaCreate):
    id: int


class AreaList(BaseModel):
    areas: list[AreaBase]
