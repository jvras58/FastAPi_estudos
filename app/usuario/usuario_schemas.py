from pydantic import BaseModel
from typing import Annotated

class UsuarioBase(BaseModel):
    id  : str
    nome: str
    # FIXME: teste para verificar o que esta acontecendo entre os relacionamentos...(onde eu crio no schema de usuario o tipo)
    # tipo: str
    tipo_id: str
    email: str
    senha: str
    
class Token(BaseModel):
    access_token: str
    token_type: str
    
class UsuarioCreate(UsuarioBase):
    pass    