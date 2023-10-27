from pydantic import BaseModel

class TipoUserBase(BaseModel):
    id: str
    tipo: str

class TipoUserCreate(TipoUserBase):
    pass
