from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from app.area.crud_area import get_area_by_id
from app.reserva.reserva_model import Reservation
from app.reserva.reserva_schema import ReservationCreate
from app.usuario.crud_usuario import get_user_by_id
from database.get_db import get_db


def get_reservation_by_id(reservation_id: int, db: Session = Depends(get_db)):
    """
    Obtém uma reserva pelo seu ID.

    Args:
        reservation_id (int): O ID da reserva a ser obtida.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: A reserva encontrada com o ID correspondente, ou None se não encontrada.
    """
    return (
        db.query(Reservation).filter(Reservation.id == reservation_id).first()
    )


def get_reservations_by_user_id(user_id: int, db: Session = Depends(get_db)):
    """
    Obtém todas as reservas associadas a um usuário pelo seu ID.

    Args:
        user_id (str): O ID do usuário para o qual as reservas estão associadas.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Reservation]: Uma lista de reservas associadas ao usuário, ou uma lista vazia se não houver nenhuma.
    """
    return (
        db.query(Reservation).filter(Reservation.usuario_id == user_id).all()
    )


def get_all(db: Session = Depends(get_db)):
    """
    Obtém todas as reservas no banco de dados.

    Args:
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Area]: Uma lista de todas as reservas.
    """
    return db.query(Reservation).all()


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
        raise HTTPException(
            status_code=400,
            detail='Usuario não existe ou não está autenticado',
        )

    # Verifica se a área existe
    area = get_area_by_id(reservation.area_id, db)
    if not area:
        raise HTTPException(status_code=400, detail='Area não existe')

    # Verificar se há conflito de horários
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

    if reservas_conflito:
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


def update_reservation(
    reservation_id: int,
    reservation: ReservationCreate,
    db: Session = Depends(get_db),
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
        raise HTTPException(status_code=404, detail='Reservation not found')
    for key, value in reservation.model_dump().items():
        setattr(db_reservation, key, value)
    db.commit()
    return db_reservation


def delete_reservation1(db: Session, db_reservation: Reservation):
    """
    Exclui uma reserva existente.

    Args:
        db (Session): Uma sessão do banco de dados.
        db_reservation (Reservation): A reserva a ser excluída.

    Returns:
        dict: Um dicionário com uma mensagem indicando que a reserva foi excluída com sucesso.
    """
    db.delete(db_reservation)
    db.commit()


def delete_reservation(reservation_id: int, db: Session = Depends(get_db)):
    """
    Deleta uma área existente.

    Args:
        area_id (int): ID da área a ser deletada.
        db (Session, optional): Sessão do banco de dados. obtido via Depends(get_db).

    Raises:
        HTTPException: Retorna um erro HTTP 404 se a área não for encontrada.
    """
    db_reserva = get_reservation_by_id(reservation_id, db)
    if not db_reserva:
        raise HTTPException(status_code=404, detail='reserva not found')
    db.delete(db_reserva)
    db.commit()


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
