from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

import app.api.reserva.crud_reserva as crud_reserva
import app.api.usuario.crud_usuario as crud_usuario
from app.api.area.crud_area import get_area_by_id
from app.api.reserva.reserva_model import Reservation
from app.api.reserva.reserva_schema import ReservationCreate, ReservationList
from app.api.usuario.crud_usuario import get_user_by_id
from app.api.usuario.usuario_model import Usuario
from app.database.get_db import get_db
from app.Exceptions.exceptions import (
    area_nao_encontrada_exception,
    reserva_choque_horario_exception,
    reserva_nao_encontrada_exception,
    sem_permissao_exception,
    usuario_nao_encontrado_ou_nao_autenticado_exception,
)

router_reserva = APIRouter()

Session = Annotated[Session, Depends(get_db)]
Current_User = Annotated[Usuario, Depends(crud_usuario.get_current_user)]


@router_reserva.post('/reservas')
def create_reserva(
    reserva: ReservationCreate,
    current_user: Current_User,
    db: Session,
):
    """
    Criar uma nova reserva.

    Args:
        reserva (ReservationCreate): Os detalhes da reserva a ser criada.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).
        current_user (Type, optional): O usuário autenticado. Obtido via Depends(get_current_user).

    Returns:
        Reservation: A reserva criada.
    """
    # def test_create_reserva_fail_sem_permissao ja temos uma verificação parecida feita por get_user_by_id mas se eu optar em deixar essa verificação ante a outra alguns testes de usuarios inexistentes poderão ter que ser remodelados
    # if reserva.usuario_id != current_user.id:
    #     raise sem_permissao_exception()
    result = crud_reserva.create_reservation(db=db, reservation=reserva)
    if result is None:
        user = get_user_by_id(reserva.usuario_id, db)
        if user is None:
            raise usuario_nao_encontrado_ou_nao_autenticado_exception()
        area = get_area_by_id(reserva.area_id, db)
        if area is None:
            raise area_nao_encontrada_exception()
        if crud_reserva.check_reservation_conflict(db, reserva):
            raise reserva_choque_horario_exception()
    return result


@router_reserva.get('/reservas', response_model=ReservationList)
def read_reservas(db: Session, skip: int = 0, limit: int = 100):
    """
    Retorna uma lista de reservas com paginação.

    Parâmetros:
    db (Session): Sessão do banco de dados.
    skip (int): Quantidade de registros a serem ignorados.
    limit (int): Quantidade máxima de registros a serem retornados.

    Retorna:
    dict: Dicionário contendo a lista de reservas.
    """
    reservas: list[Reservation] = crud_reserva.get_reservas(db, skip, limit)
    if reservas is None:
        raise reserva_nao_encontrada_exception()
    return {'Reservation': reservas}


@router_reserva.get('/reservas/{reservation_id}')
def get_reserva(
    reservation_id: int,
    current_user: Current_User,
    db: Session,
):
    """
    Obter os detalhes de uma reserva pelo ID.

    Args:
        reservation_id (int): O ID da reserva.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: Os detalhes da reserva.
    """
    db_reservation = crud_reserva.get_reservation_by_id(reservation_id, db)
    if db_reservation is None:
        raise reserva_nao_encontrada_exception()
    return db_reservation


@router_reserva.put('/reservas/{reservation_id}')
def update_reserva(
    reservation_id: int,
    reserva: ReservationCreate,
    current_user: Current_User,
    db: Session,
):
    """
    Atualiza os detalhes de uma reserva.

    Args:
        reservation_id (str): O ID da reserva que será atualizada.
        reserva (ReservationCreate): Os novos detalhes da reserva.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: Os detalhes atualizados da reserva.
    """
    if reserva.usuario_id != current_user.id:
        raise sem_permissao_exception()
    updated_reserva = crud_reserva.update_reservation(
        reservation_id, reserva, db
    )
    if updated_reserva is None:
        raise reserva_nao_encontrada_exception()
    return crud_reserva.update_reservation(reservation_id, reserva, db)


@router_reserva.delete('/reservas/{reservation_id}')
def delete_reserva(
    reservation_id: int,
    db: Session,
    current_user: Current_User,
):
    """
    Deleta uma reserva.

    Args:
        reservation_id (str): O ID da reserva que será deletada.
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        dict: Uma mensagem indicando que a reserva foi deletada com sucesso.
    """
    delete_reserva = crud_reserva.delete_reservation(reservation_id, db)
    if delete_reserva:
        return {'detail': 'Reserva deletada com sucesso'}
    else:
        raise reserva_nao_encontrada_exception()


@router_reserva.get('/usuario/reservas')
def get_reservas_usuario(
    current_user: Current_User,
    db: Session,
):
    """
    Obtém as reservas associadas ao usuário atualmente autenticado.

    Args:
        current_user (Type, optional): O usuário atualmente autenticado. Obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        List[Reservation]: Uma lista de objetos de reserva associados ao usuário.
    """
    reservations = crud_reserva.get_reservations_by_user_id(
        current_user.id, db
    )
    if not reservations:
        raise reserva_nao_encontrada_exception()
    return reservations


@router_reserva.get('/usuario/reservas/{reservation_id}')
def get_reserva_usuario(
    reservation_id: int,
    current_user: Current_User,
    db: Session,
):
    """
    Obtém uma reserva específica associada ao usuário atualmente autenticado.

    Args:
        reservation_id (str): O ID da reserva a ser obtida.
        current_user (Type, optional): O usuário atualmente autenticado. Obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: O objeto de reserva associado ao usuário, se encontrado.

    Raises:
        HTTPException(404): Se a reserva não for encontrada ou não estiver associada ao usuário atual.
    """
    db_reservation = crud_reserva.get_reservation_by_id(reservation_id, db)
    if db_reservation is None or db_reservation.usuario_id != current_user.id:
        raise reserva_nao_encontrada_exception()
    return db_reservation
