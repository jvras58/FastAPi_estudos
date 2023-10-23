from pydantic import BaseModel
from typing import Annotated

class UsuarioBase(BaseModel):
    id  : str
    nome: str
    tipo_id: str
    email: str
    senha: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class UsuarioCreate(UsuarioBase):
    pass    