from pydantic import BaseModel
from typing import Annotated


class AreaBase(BaseModel):
    id: str
    nome: str
    #disponivel: bool
    descricao: str
    iluminacao: str
    tipo_piso: str
    covered: str
    foto_url: str
    usuario_id: str

class AreaCreate(AreaBase):
    pass