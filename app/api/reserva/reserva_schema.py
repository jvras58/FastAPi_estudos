from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ReservationCreate(BaseModel):
    reserva_data: datetime
    hora_inicio: datetime
    hora_fim: datetime
    justificacao: str
    reserva_tipo: str
    status: str
    area_id: int
    usuario_id: int
    model_config = ConfigDict(from_attributes=True)


class ReservationBase(ReservationCreate):
    id: int
    valor: int


class ReservationList(BaseModel):
    Reservation: list[ReservationBase]
