from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.area.crud_area import get_area_by_id
from app.api.reserva.reserva_model import Reservation
from app.api.reserva.reserva_schema import ReservationCreate
from app.api.usuario.crud_usuario import get_user_by_id
from app.database.get_db import get_db

Session = Annotated[Session, Depends(get_db)]


def get_reservation_by_id(reservation_id: int, db: Session):
    """
    Obtém uma reserva pelo seu ID.

    Args:
        reservation_id (int): O ID da reserva a ser obtida.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: A reserva encontrada com o ID correspondente, ou None se não encontrada.
    """
    reservas = (
        db.query(Reservation).filter(Reservation.id == reservation_id).first()
    )
    if not reservas:
        return None
    return reservas


def get_reservations_by_user_id(user_id: int, db: Session):
    """
    Obtém todas as reservas associadas a um usuário pelo seu ID.

    Args:
        user_id (str): O ID do usuário para o qual as reservas estão associadas.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Reservation]: Uma lista de reservas associadas ao usuário, ou None se não houver nenhuma.
    """
    reservations = (
        db.query(Reservation).filter(Reservation.usuario_id == user_id).all()
    )
    if not reservations:
        return None
    return reservations


def get_reservas(
    db: Session, skip: int = 0, limit: int = 100
) -> list[Reservation]:
    """
    Retorna uma lista de reservas a partir do banco de dados.

    Parâmetros:
    db (Session): Sessão do banco de dados.
    skip (int): Quantidade de reservas a serem ignorados.
    limit (int): Quantidade máxima de reservas a serem retornados.

    Retorna:
    list[reservas]: Lista de areas.
    """
    reservas = db.query(Reservation).offset(skip).limit(limit).all()
    if not reservas:
        return None
    return reservas


def create_reservation(db: Session, reservation: ReservationCreate):
    """
    Cria uma nova reserva no banco de dados.

    Args:
        db (Session): Sessão do banco de dados.
        reservation (ReservationCreate): Os dados da reserva a ser criada.

    Returns:
        Reservation: A reserva criada.
    """

    # Verifica se o usuário existe
    user = get_user_by_id(reservation.usuario_id, db)
    if not user:
        return None

    # Verifica se a área existe
    area = get_area_by_id(reservation.area_id, db)
    if not area:
        return None

    # Verificar se há conflito de horários
    if check_reservation_conflict(db, reservation):
        return None

    db_reservation = Reservation(**reservation.model_dump())
    valor = define_preco_por_hora(reservation)
    status = 'Em análise'
    db_reservation.valor = valor
    db_reservation.status = status

    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)

    return db_reservation


def check_reservation_conflict(
    db: Session, reservation: ReservationCreate
) -> bool:
    """
    Verifica se há conflito de horários entre as reservas.

    Args:
        db (Session): Sessão do banco de dados.
        reservation (ReservationCreate): Os dados da reserva a ser criada.

    Returns:
        bool: True se houver conflito de horários, False caso contrário.
    """
    inicio = reservation.hora_inicio
    fim = reservation.hora_fim

    reservas_conflito = (
        db.query(Reservation)
        .filter(
            Reservation.area_id == reservation.area_id,
            Reservation.reserva_data == reservation.reserva_data,
            Reservation.hora_inicio < fim,
            Reservation.hora_fim > inicio,
        )
        .all()
    )

    return bool(reservas_conflito)


def update_reservation(
    reservation_id: int,
    reservation: ReservationCreate,
    db: Session,
):
    """
    Atualiza os detalhes de uma reserva existente.

    Args:
        reservation_id (int): O ID da reserva a ser atualizada.
        reservation (ReservationCreate): Os novos detalhes da reserva.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Raises:
        HTTPException: Retorna um erro 404 se a reserva não for encontrada.

    Returns:
        Reservation: A reserva atualizada.
    """
    db_reservation = get_reservation_by_id(reservation_id, db)
    if not db_reservation:
        return None
    for dado, valor in reservation.model_dump().items():
        setattr(db_reservation, dado, valor)
    db_reservation.valor = define_preco_por_hora(reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def delete_reservation(reservation_id: int, db: Session):
    """
    Deleta uma área existente.

    Args:
        area_id (int): ID da área a ser deletada.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Raises:
        HTTPException: Retorna um erro HTTP 404 se a área não for encontrada.
    """
    db_reserva = get_reservation_by_id(reservation_id, db)
    db.delete(db_reserva)
    db.commit()
    return True


# FUNÇÃO OCIOSA NÃO UTLIZADA NO ENDPOINT DE RESERVA (IGNORAR NO COVERAGE)
def define_preco_por_hora(reservation: ReservationCreate):
    """
    Calcula o preço da reserva com base nas horas de início e fim.

    Args:
        reservation (ReservationCreate): Os detalhes da reserva.

    Returns:
        int: O preço da reserva.
    """
    horas = (
        reservation.hora_fim - reservation.hora_inicio
    ).total_seconds() / 3600

    if horas <= 0:
        return 10
    else:
        return int(horas) * 10
