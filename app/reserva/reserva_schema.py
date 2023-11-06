from datetime import datetime

from pydantic import BaseModel


class ReservationCreate(BaseModel):
    valor: int
    reserva_data: datetime
    hora_inicio: datetime
    hora_fim: datetime
    justificacao: str
    reserva_tipo: str
    status: str
    area_id: int
    usuario_id: int


class ReservationBase(ReservationCreate):
    id: int


class ReservationList(ReservationBase):
    Reservation: list[ReservationBase]
