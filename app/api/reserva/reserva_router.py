from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.api.reserva.crud_reserva as crud_reserva
from app.api.auth.crud_auth import get_current_user, verify_permission
from app.api.reserva.reserva_model import Reservation
from app.api.reserva.reserva_schema import ReservationCreate, ReservationList
from app.api.usuario.usuario_model import Usuario
from app.config.config import get_settings
from app.database.get_db import get_db
from app.utils.Exceptions.exceptions import (
    ObjectNotFoundException,
    PermissionException,
    sem_permissao_exception,
)

router_reserva = APIRouter()

Session = Annotated[Session, Depends(get_db)]
Current_User = Annotated[Usuario, Depends(get_current_user)]


@router_reserva.post('/reservas')
def create_reserva(
    reserva: ReservationCreate,
    Current_User: Current_User,
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
    try:
        if Current_User[
            'user'
        ].id != reserva.usuario_id and not verify_permission(
            Current_User['permissions'], get_settings().ADMINISTRADOR
        ):
            raise PermissionException('Create Reserva')
    except PermissionException as ex:
        raise HTTPException(status_code=403, detail=ex.args[0]) from ex
    return crud_reserva.create_reservation(db=db, reservation=reserva)


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
    try:
        return crud_reserva.get_reservation_by_id(reservation_id, db)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex


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
    if reserva.usuario_id != current_user['user'].id and not verify_permission(
        current_user['permissions'], get_settings().ADMINISTRADOR
    ):
        raise sem_permissao_exception()
    try:
        updated_reserva = crud_reserva.update_reservation(
            reservation_id, reserva, db
        )
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex
    return updated_reserva


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
    try:
        db_reservation = crud_reserva.get_reservation_by_id(reservation_id, db)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex

    try:
        if current_user[
            'user'
        ].id != db_reservation.usuario_id and not verify_permission(
            current_user['permissions'], get_settings().ADMINISTRADOR
        ):
            raise PermissionException('user')
    except PermissionException as ex:
        raise HTTPException(status_code=403, detail=ex.args[0]) from ex

    crud_reserva.delete_reservation(reservation_id, db)
    return {'detail': 'Reserva deletada com sucesso'}


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
    try:
        reservations = crud_reserva.get_reservations_by_user_id(
            current_user['user'].id, db
        )
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex
    return reservations


@router_reserva.get('/usuario/reservas/{reservation_id}')
def get_reserva_usuario(
    reservation_id: int,
    current_user: Current_User,
    db: Session,
):
    """
    Obtém uma reserva específica pelo ID associada ao usuário atualmente autenticado.

    Args:
        reservation_id (str): O ID da reserva a ser obtida.
        current_user (Type, optional): O usuário atualmente autenticado. Obtido via Depends(crud_user.get_current_user).
        db (Session, optional): Uma sessão do banco de dados. obtida via Depends(get_db).

    Returns:
        Reservation: O objeto de reserva associado ao usuário, se encontrado.

    Raises:
        HTTPException(404): Se a reserva não for encontrada ou não estiver associada ao usuário atual.
    """
    try:
        db_reservation = crud_reserva.get_reservation_by_id(reservation_id, db)
    except ObjectNotFoundException as ex:
        raise HTTPException(status_code=404, detail=ex.args[0]) from ex
    try:
        if current_user[
            'user'
        ].id != db_reservation.usuario_id and not verify_permission(
            current_user['permissions'], get_settings().ADMINISTRADOR
        ):
            raise PermissionException('user')
    except PermissionException as ex:
        raise HTTPException(status_code=403, detail=ex.args[0]) from ex
    return db_reservation
