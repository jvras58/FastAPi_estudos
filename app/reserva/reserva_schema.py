from datetime import datetime

from pydantic import BaseModel


class ReservationCreate(BaseModel):
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
    valor: int


class ReservationList(ReservationBase):
    Reservation: list[ReservationBase]
