from pydantic import BaseModel
from typing import Annotated
from datetime import datetime

class ReservationBase(BaseModel):
    id: str
    valor: int
    reserva_data: datetime
    hora_inicio: datetime
    hora_fim: datetime
    justificacao: str
    reserva_tipo: str
    status: str
    area_id: str
    usuario_id: str

class ReservationCreate(ReservationBase):
    pass