from pydantic import BaseModel
from typing import Annotated

class UsuarioBase(BaseModel):
    nome: str
    email: str
    senha: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
  
class UsuarioCreate(UsuarioBase):
    pass    